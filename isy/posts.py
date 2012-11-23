'''
Created on Nov 22, 2012

@author: stum
'''

from isy import app, crossdomain, standardize_json
from isy.model import *

@app.route('/api/post/<int:post_id>')
@crossdomain(origin = '*')
def api_view_post(post_id):
    p = Post.get_by_id(post_id)
    if p is None:
        return standardize_json({}, 'notfound')
    if not p.is_visible:
        return standardize_json({}, 'notfound')
    return standardize_json(p.rep_as_dict())
