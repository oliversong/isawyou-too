'''
Created on Nov 22, 2012

@author: stum
'''
from datetime import datetime
from entro import DB_USER, DB_PWD, DB_HOST, DB_NAME
from sqlalchemy import Column, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.types import Text, Integer, String, DateTime, Enum, Boolean

# entro is a file that defines the database values. you should create it.

Base = declarative_base()
engine = create_engine('mysql://%s:%s@%s/%s' % (DB_USER, DB_PWD, DB_HOST, DB_NAME))
Session = scoped_session(sessionmaker(bind = engine))

def save_all_changes():
    s = Session()
    s.commit()

def rollback():
    s = Session()
    s.rollback()

class Common(object):
    def __repr__(self):
        return str(self)
    def __str__(self): #to prevent programmer mistakes causing infinite recursion
        return str(self.__class__) + "!!"
    def delete(self):
        s = Session()
        s.delete(self)
    def add(self):
        sess = Session()
        sess.add(self)
        sess.commit()

class StdMixin(Common):
    @declared_attr
    def __tablename__(cls): #@NoSelf
        return cls.__name__.lower()
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column(Integer, primary_key = True)

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

    def num_comments(self):
        return len(self.comments)

    @staticmethod
    def get_by_id(post_id):
        s = Session()
        try:
            return s.query(Post).filter(Post.id == post_id).one()
        except NoResultFound:
            return None

class Comment(StdMixin, Base):
    post_id = Column(Integer, ForeignKey('post.id'))
    post_date = Column(DateTime)
    body = Column(Text)
    author_gender = Column(Enum('M', 'F', 'O'))
    ip = Column(String(15))
    is_visible = Column(Boolean)
    author = Column(String(8))
    replies_enabled = Column(Boolean)
    num_contacts = Column(Integer)

    votes = relationship('Vote', backref = 'comment')

    def __init__(self, post, body, ip, author_gender):
        self.post = post
        self.body = body
        self.ip = ip
        self.author_gender = author_gender
        self.is_visible = False

class Vote(StdMixin, Base):
    comment_id = Column(Integer, ForeignKey('comment.id'))
    direction = Column(Enum('UP', 'DOWN'))
    voter = Column(String(8))
