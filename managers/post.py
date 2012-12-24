'''
Created on Dec 23, 2012

@author: stum
'''
from flask.ext.script import Command, Option
from isy.models import Post

class PostManager(Command):
    "Administer/view a post"
    option_list = (
       Option('post_id', type = int, help = "Post ID to administer or view"),
       Option('-d' , '--delete', action = 'store_true', dest = 'delete', help = "Delete (takedown) a post")
    )

    def run(self, post_id, delete = False):
        print "Looking up post %s..." % post_id,
        p = Post.get_by_id(post_id)
        if p is None:
            print "Not found!"
            return
        print "\n"

        if delete:
            if not p.is_visible and p.been_moderated:
                print "Already deleted!"
                return
            p.is_visible = False
            p.been_moderated = True
            print '"Deleted" %s' % p.title
            return

        print_post(p)

def print_post(p):
    print p.title
    if p.sticky:
        print "STICKY"
    if not p.is_visible:
        print "DELETED"
    if not p.been_moderated:
        print "UNMODERATED"
    print "%s spotting %s on %s" % (p.author_gender, p.saw_gender, p.post_date)
    print "Authored by: %s (%s)" % (p.author, p.ip)
    if p.replies_enabled:
        print "Replies Enabled (%s replies)" % p.num_contacts
    print "", p.body
