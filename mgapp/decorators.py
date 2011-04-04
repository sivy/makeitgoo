import stats_util as stats
from functools import wraps
from datetime import datetime

def jsonp(f):
    """Wrap a json response in a callback, and set the mimetype (Content-Type) header accordingly 
    (will wrap in text/javascript if there is a callback). If the "callback" or "jsonp" paramters 
    are provided, will wrap the json output in callback({thejson})
    
    Usage:
    
    @jsonp
    def my_json_view(request):
        d = { 'key': 'value' }
        return HTTPResponse(json.dumps(d), content_type='application/json')
    
    """
    @wraps(f)
    def jsonp_wrapper(request, *args, **kwargs):
        resp = f(request, *args, **kwargs)
        if resp.status_code != 200:
            return resp
        if 'callback' in request.GET:
            callback= request.GET['callback']
            resp['Content-Type']='text/javascript; charset=utf-8'
            resp.content = "%s(%s)" % (callback, resp.content)
            return resp
        elif 'jsonp' in request.GET:
            callback= request.GET['jsonp']
            resp['Content-Type']='text/javascript; charset=utf-8'
            resp.content = "%s(%s)" % (callback, resp.content)
            return resp
        else:
            return resp                
                
    return jsonp_wrapper

def recordstats(stat_prefix=None):
    """Record that this function was called, with duration
    
    Usage:
    
    @recordstats('stats_prefix')
    def my_view(request):
        return HTTPResponse(the_content)
    
    This will send a metric to statsd with the name 'stats_prefix.my_view'. Omitting the
    argument to recordstats() will result in a metric simply named after the wrapped 
    function, in this case 'my_view'.
    
    This will also send a time metric to statsd with the name 'stats_prefix.my_view' (or
    'my_view') with the duration of the call.
    
    """
    def stat_name_wrapper(*args, **kwargs):
        f = args[0]
        def stat_wrapper(*args, **kwargs):
            if stat_prefix:
                stat_name = "%s.%s" % (stat_prefix, f.__name__)
            else:
                stat_name = f.__name__
            
            start = datetime.now()
            
            print "incrstat: " + stat_name
            stats.incrstat("%s.hits" % stat_name)
            result = f(*args, **kwargs)
        
            end = datetime.now()
            millis = (end - start).microseconds/1000
            
            print "timestat: %s %sm" % (stat_name, millis)
            stats.timestat(stat_name, millis)

            return result
        
        return wraps(f)(stat_wrapper)
    return stat_name_wrapper