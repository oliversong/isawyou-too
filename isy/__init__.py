#===============================================================================
# This is the main entry point for the application.
#
# In order to keep this file readable, though, we want to use this file simply
# for the basic setup. Import the app object from this file, and import the view
# file that you write here.
# 
# If you want cross-domain requests (useful for API stuff!), make sure to import
# crossdomain from this file as well.
#===============================================================================

from datetime import timedelta
from flask import *
from functools import update_wrapper
from model import *

app = Flask(__name__)

def crossdomain(origin = None, methods = None, headers = None,
                max_age = 21600, attach_to_all = True,
                automatic_options = True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def standardize_json(data, status = 'ok'):
    d = {}
    d['status'] = status
    d['data'] = data
    if g.athena is None:
        d['authed'] = ''
    else:
        d['authed'] = g.athena
    return jsonify(d)

@app.before_request
def before_request():
    if app.debug:
        user = 'stum@MIT.EDU'
    else:
        try:
            user = request.environ.get('SSL_CLIENT_S_DN_Email')
        except:
            user = None
    if user is not None:
        g.athena = user.split('@')[0]
    else:
        g.athena = None

