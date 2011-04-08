from django.conf import settings
from pystatsd import Client
import logging

log = logging.getLogger('stats_util')

stats_ns = ''
if (hasattr(settings,'STATS_NAMESPACE')):
    stats_ns = settings.STATS_NAMESPACE

backend = 'statsd'
if (hasattr(settings, 'STATS_BACKEND')):
    backend = settings.STATS_BACKEND

def _statname(stat):
    return "%s.%s" % (stats_ns, stat)

def _is_setup():
    return hasattr(settings,'STATSD_HOST') and \
        hasattr(settings,'STATSD_PORT')
    
def incrstat(stat, count=1):
    if not _is_setup():
        log.info('STATSD_HOST or STATSD_PORT not set up')
        return
    client = Client(settings.STATSD_HOST, settings.STATSD_PORT)
    client.increment(_statname(stat), count)
    log.info('incrstat: %s %s' % (_statname(stat), count))

def decrstat(stat, count=1):
    if not _is_setup():
        log.info('STATSD_HOST or STATSD_PORT not set up')
        return
    client = Client(settings.STATSD_HOST, settings.STATSD_PORT)
    client.decrement(_statname(stat), count)
    log.info('decrstat: %s %s' % (_statname(stat), count))

def timestat(stat, millis):
    if not _is_setup():
        log.info('STATSD_HOST or STATSD_PORT not set up')
        return
    client = Client(settings.STATSD_HOST, settings.STATSD_PORT)
    client.timing(_statname(stat), millis)
    log.info('timestat: %s %sm' % (_statname(stat), millis))

def addstat(stat, n):
    if not _is_setup():
        log.info('STATSD_HOST or STATSD_PORT not set up')
        return
    client = Client(settings.STATSD_HOST, settings.STATSD_PORT)
    client.update_stats(_statname(stat), n)
    log.info('addstat: %s %s' % (_statname(stat), n))
    