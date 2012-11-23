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

@app.route('/api/post/', methods = ['GET'], defaults = {'page': 1})
@app.route('/api/post/page/<int:page>')
@crossdomain(origin = '*')
def api_view_page(page):
    posts = Post.get_visible_posts()[20 * (page - 1):20 * page]
    post_list = []
    for post in posts:
        post_list.append(post.rep_as_dict())
    status = 'ok' if len(post_list) > 0 else 'notfound'
    return standardize_json({'posts': post_list, 'page': page}, status)
