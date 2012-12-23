'''
Created on Dec 23, 2012

@author: stum
'''
from datetime import datetime
from isy.models import Base, StdMixin, Session
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Text, Boolean, DateTime, Enum, Integer
from time import mktime

class Post(StdMixin, Base):
    title = Column(String(50))
    body = Column(Text)
    author = Column(String(8))
    replies_enabled = Column(Boolean)
    post_date = Column(DateTime)
    author_gender = Column(Enum('M', 'F', 'O'))
    saw_gender = Column(Enum('M', 'F', 'O'))
    is_visible = Column(Boolean)
    been_moderated = Column(Boolean)
    ip = Column(String(15))
    num_contacts = Column(Integer)
    sticky = Column(Boolean)

    comments = relationship('Comment', backref = 'post')

    allowed_genders = ('M', 'F', 'O')

    def __init__(self, title, body, ip, author_gender, saw_gender):
        self.title = title
        self.body = body
        self.ip = ip
        self.author_gender = author_gender
        self.saw_gender = saw_gender
        self.num_contacts = 0
        self.been_moderated = False
        self.is_visible = False
        self.post_date = datetime.now()
        self.replies_enabled = False
        self.sticky = False

    def __str__(self):
        return "Post <%s>" % (self.title)

    def num_comments(self):
        return len(self.comments)

    @staticmethod
    def get_by_id(post_id):
        s = Session()
        try:
            return s.query(Post).filter(Post.id == post_id).one()
        except NoResultFound:
            return None

    def rep_as_dict(self):
        d = {}
        d['id'] = self.id
        d['title'] = self.title
        d['body'] = self.body
        d['authorGender'] = self.author_gender
        d['sawGender'] = self.saw_gender
        d['commentCount'] = self.num_comments()
        d['postDate'] = int(mktime(self.post_date.timetuple()))
        d['replies'] = self.replies_enabled
        return d

    @staticmethod
    def get_visible_posts():
        s = Session()
        return s.query(Post).filter(Post.is_visible == True).\
            order_by(Post.post_date.desc())
