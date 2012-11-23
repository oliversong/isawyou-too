'''
Created on Nov 22, 2012

@author: stum
'''

from flask import abort
from flask.globals import request, g
from isy import app, crossdomain, standardize_json, moderators
from isy.model import Post

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

@app.route('/api/post/', methods = ['POST'])
@crossdomain(origin = '*')
def api_create_post():
    if request.form['sawGender'] not in Post.allowed_genders or request.form['authorGender'] not in Post.allowed_genders:
        abort(400)
    p = Post(request.form['title'], request.form['body'], request.remote_addr, request.form['authorGender'], request.form['sawGender'])
    if 'sign' in request.form and request.form['sign'] == 'true':
        if g.athena is None:
            abort(400)
        p.author = g.athena
        if request.form['replies'] == 'true':
            p.replies_enabled = True
    if 'sticky' in request.form and request.form['sticky'] == 'true' and g.athena in moderators:
        p.sticky = True

    #save the post and return its id
    p.add()
    return standardize_json({'id': p.id})
