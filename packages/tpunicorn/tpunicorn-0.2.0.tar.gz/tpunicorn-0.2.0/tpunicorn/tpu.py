from six.moves import shlex_quote as shellquote
from subprocess import check_output
import json
import re
import ring
import os
import logging
import threading

logger = logging.getLogger('tpunicorn')

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s', datefmt='%m-%d-%Y %I:%M:%S%p %Z')
ch.setFormatter(formatter)
logger.addHandler(ch)

def ero(x):
  logger.info('%s', x)
  return x

def build_opt(k, v):
  k = k.replace('_', '-').replace('--', '_')
  if v is True:
    return '--' + k
  if v is False:
    return '--no-' + k
  return '--{} {}'.format(k, shellquote(v))

def build_commandline(cmd, *args, **kws):
  return ' '.join([cmd] + [shellquote(x) for x in args] + [build_opt(k, v) for k, v in kws.items() if v is not None])

def system(cmd, *args, **kws):
  command = build_commandline(cmd, *args, **kws)
  os.system(command)

def run(cmd, *args, **kws):
  command = build_commandline(cmd, *args, **kws)
  out = check_output(ero(command), shell=True)
  if isinstance(out, bytes):
    out = out.decode('utf8')
  return out

def parse_tpu_project(tpu):
  fqn = tpu if isinstance(tpu, str) else tpu['name']
  return fqn.split('/')[-5]

def parse_tpu_zone(tpu):
  fqn = tpu if isinstance(tpu, str) else tpu['name']
  return fqn.split('/')[-3]

def parse_tpu_id(tpu):
  fqn = tpu if isinstance(tpu, str) else tpu['name']
  return fqn.split('/')[-1]

def parse_tpu_index(tpu):
  fqn = tpu if isinstance(tpu, str) else tpu['name']
  idx = re.findall(r'([0-9]+)$', fqn)
  if len(idx) <= 0:
    idx = -1
  else:
    idx = int(idx[0])
  return idx

def parse_tpu_network(tpu):
  net = tpu if isinstance(tpu, str) else tpu['network']
  return net.split('/')[-1]

@ring.lru(expire=3600) # cache tpu zones for an hour
def get_tpu_zones():
  out = run("gcloud compute tpus locations list", format="json")
  zones = json.loads(out)
  return [zone['locationId'] for zone in zones]


# Python 3.5 backport. Is there a more elegant way to get a nullcontext?
import abc


class AbstractContextManager(abc.ABC):
  """An abstract base class for context managers."""

  def __enter__(self):
    """Return `self` upon entering the runtime context."""
    return self

  @abc.abstractmethod
  def __exit__(self, exc_type, exc_value, traceback):
    """Raise any exception triggered within the runtime context."""
    return None


class nullcontext(AbstractContextManager):
    """Context manager that does no additional processing.
    Used as a stand-in for a normal context manager, when a particular
    block of code is only sometimes used with a normal context manager:
    cm = optional_cm if condition else nullcontext()
    with cm:
        # Perform operation, using optional_cm if condition is True
    """

    def __init__(self, enter_result=None):
        self.enter_result = enter_result

    def __enter__(self):
        return self.enter_result

    def __exit__(self, *excinfo):
        pass


def click_context():
  try:
    import click
    ctx = click.get_current_context(silent=True)
  except:
    ctx = None
  if ctx is None:
    ctx = nullcontext()
  return ctx

@ring.lru(expire=15) # cache tpu info for 15 seconds
def fetch_tpus(zone=None):
  if zone is None:
    zones = get_tpu_zones()
  if isinstance(zone, str):
    zones = zone.split(',')
  tpus = []
  ctx = click_context()
  def fetch(zone):
    with ctx:
      more = list_tpus(zone)
      tpus.extend(more)
  threads = [threading.Thread(target=fetch, args=(zone,), daemon=True) for zone in zones]
  for thread in threads:
    thread.start()
  for thread in threads:
    thread.join()
  return tpus

def list_tpus(zone):
  out = run("gcloud compute tpus list", format="json", zone=zone)
  tpus = json.loads(out)
  return list(sorted(tpus, key=parse_tpu_index))

def get_tpus(zone=None):
  tpus = fetch_tpus(zone=zone)
  if zone is None:
    return tpus
  else:
    return [tpu for tpu in tpus if '/{}/'.format(zone) in tpu['name']]

def get_tpu(tpu, zone=None, silent=False):
  if isinstance(tpu, dict):
    tpu = parse_tpu_id(tpu)
  if isinstance(tpu, str) and re.match('^[0-9]+$', tpu):
    tpu = int(tpu)
  if isinstance(tpu, int):
    which = 'index'
    tpus = [x for x in get_tpus(zone=zone) if parse_tpu_index(x) == tpu]
  else:
    which = 'id'
    tpus = [x for x in get_tpus(zone=zone) if parse_tpu_id(x) == tpu]
  if len(tpus) > 1:
    raise ValueError("Multiple TPUs matched {} {!r}. Try specifying --zone".format(which, tpu))
  if len(tpus) <= 0:
    if silent:
      return None
    raise ValueError("No TPUs matched {} {!r}".format(which, tpu))
  return tpus[0]

from string import Formatter

class NamespaceFormatter(Formatter):
  def __init__(self, namespace={}):
    Formatter.__init__(self)
    self.namespace = namespace

  def get_value(self, key, args, kwds):
    if isinstance(key, str):
      try:
        # Check explicitly passed arguments first
        return kwds[key]
      except KeyError:
        return self.namespace[key]
    else:
      return Formatter.get_value(key, args, kwds)

from collections import defaultdict

@ring.lru(expire=1) # seconds
def format_widths():
  headers = format_headers()
  tpus = get_tpus()
  r = defaultdict(int)
  for tpu in tpus:
    args = _format_args(tpu)
    for k, v in args.items():
      s = '{}'.format(v)
      r[k+'_w'] = max(r[k+'_w'], len(s) + 1, len(headers[k]) + 1)
  return r

def _normalize_tpu_isodate(iso):
  r = re.findall('(.*[.][0-9]{6})[0-9]*Z', iso)
  if len(r) > 0:
    return r[0] + 'Z'
  raise ValueError("Could not parse TPU date {!r}".format(iso))

import moment
import datetime
import time

def get_timestamp(timestamp=None, utc=True):
  if timestamp is None:
    timestamp = time.time()
  # https://stackoverflow.com/a/52606421/9919772
  #dt = datetime.datetime.fromtimestamp(timestamp).astimezone()
  dt = moment.unix(timestamp, utc=utc)
  dt = dt.timezone(current_tzname())
  return dt.strftime("%m-%d-%Y %I:%M:%S%p %Z")

def current_timezone():
  if time.daylight:
    return datetime.timezone(datetime.timedelta(seconds=-time.altzone),time.tzname[1])
  else:
    return datetime.timezone(datetime.timedelta(seconds=-time.timezone),time.tzname[0])

def current_tzname():
  return current_timezone().tzname(None)

def since(iso):
  dt = moment.utcnow() - moment.utc(_normalize_tpu_isodate(iso), "%Y-%m-%dT%H:%M:%S.%fZ")
  return dt.total_seconds()

def minutes_since(iso):
  return since(iso) / 60

def hours_since(iso):
  return since(iso) / 3600

def days_since(iso):
  return since(iso) / 86400

def nice_since(iso):
  t = int(since(iso))
  s = t % 60
  m = (t // 60) % 60
  h = (t // 3600) % 24
  d = (t // 86400)
  r = []
  out = False
  if d > 0 or out:
    out = True
    r += ['{:02d}d'.format(d)]
  else:
    r += ['   ']
  if h > 0 or out:
    out = True
    r += ['{:02d}h'.format(h)]
  else:
    r += ['   ']
  if m > 0 or out:
    out = True
    r += ['{:02d}m'.format(m)]
  else:
    r += ['   ']
  # if s > 0 or out:
  #   out = True
  #   r += ['{:02d}s'.format(s)]
  return ''.join(r)

def format_headers():
  return {
    'kind': 'header',
    'project': 'PROJECT',
    'zone': 'ZONE',
    'id': 'ID',
    'fqn': 'FQN',
    'ip': 'IP',
    'port': 'PORT',
    'master': 'MASTER',
    'range': 'RANGE',
    'type': 'TYPE',
    'created': 'CREATED',
    'age': 'AGE',
    'preemptible': 'PREEMPTIBLE?',
    'status': 'STATUS',
    'health': 'HEALTH',
    'index': 'INDEX',
    'version': 'VERSION',
    'network': 'NETWORK',
  }

def _format_args(tpu):
  return {
    'kind': 'tpu',
    'project': parse_tpu_project(tpu),
    'zone': parse_tpu_zone(tpu),
    'id': parse_tpu_id(tpu),
    'fqn': tpu['name'],
    'ip': parse_tpu_ip(tpu),
    'port': tpu['port'],
    'master': parse_tpu_master(tpu),
    'range': parse_tpu_range(tpu),
    'type': parse_tpu_type(tpu),
    'created': tpu['createTime'],
    'age': nice_since(tpu['createTime']),
    'preemptible': 'yes' if parse_tpu_preemptible(tpu) else 'no',
    'status': tpu['state'],
    'health': tpu.get('health', 'UNKNOWN'),
    'index': parse_tpu_index(tpu),
    'version': parse_tpu_version(tpu),
    'network': parse_tpu_network(tpu),
  }

def parse_tpu_preemptible(tpu):
  return tpu.get('schedulingConfig', {'preemptible': False}).get('preemptible', False)

def parse_tpu_ip(tpu):
  return tpu.get('ipAddress', '')

def parse_tpu_master(tpu):
  return '{}:{}'.format(tpu.get('ipAddress',''), tpu.get('port', 8470))

def parse_tpu_range(tpu):
  return tpu['cidrBlock']

def parse_tpu_version(tpu):
  return tpu['tensorflowVersion']

def parse_tpu_type(tpu):
  return tpu['acceleratorType']

def parse_tpu_description(tpu):
  return tpu.get('description', None)

def format_args(tpu):
  r = _format_args(tpu)
  r.update(format_widths())
  return r

def get_default_format_specs(thin=False):
  specs = [
    "{zone:{zone_w}}",
    "{index:<{index_w}}",
    "{type:{type_w}}",
    "{age:{age_w}}",
    "{id:{id_w}}",
    "{status:{status_w}}",
    "{health:{health_w}}",
    "{version:{version_w}}",
    "{network:{network_w}}",
    "{master:{master_w}}",
    "{range:{range_w}}",
    "{preemptible!s:{preemptible_w}}",
  ]
  if thin:
    return ['{' + re.findall('{([^:]+)[:]', x)[0] + '}' for x in specs]
  else:
    return specs

def get_default_format_spec(thin=False):
  return ' '.join(get_default_format_specs(thin=thin))

def format(tpu, spec=None, formatter=NamespaceFormatter):
  if tpu.get('kind', 'tpu') == 'tpu':
    args = format_args(tpu)
  else:
    args = {}
    args.update(tpu)
    args.update(format_widths())
  fmt = formatter(args)
  if spec is None:
    spec = get_default_format_spec(thin=len(format_widths()) == 0)
  return fmt.format(spec)

def create_tpu_command(tpu, zone=None, version=None, description=None, preemptible=None):
  if zone is None:
    zone = parse_tpu_zone(tpu)
  if version is None:
    version = parse_tpu_version(tpu)
  if description is None:
    description = parse_tpu_description(tpu)
  if preemptible is None:
    preemptible = True if parse_tpu_preemptible(tpu) else None
  return build_commandline("gcloud compute tpus create",
                           parse_tpu_id(tpu),
                           zone=zone,
                           network=parse_tpu_network(tpu),
                           range=parse_tpu_range(tpu),
                           version=version,
                           accelerator_type=parse_tpu_type(tpu),
                           preemptible=preemptible,
                           description=description,
                           )

def delete_tpu_command(tpu, zone=None):
  if zone is None:
    zone = parse_tpu_zone(tpu)
  return build_commandline("gcloud compute tpus delete",
                           parse_tpu_id(tpu),
                           zone=zone,
                           quiet=True,
                           )

def reimage_tpu_command(tpu, version=None):
  if version is None:
    version = parse_tpu_version(tpu)
  return build_commandline("gcloud compute tpus reimage",
                           parse_tpu_id(tpu),
                           zone=parse_tpu_zone(tpu),
                           version=version,
                           quiet=True,
                           )
