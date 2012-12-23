from isy.entro import DB_USER, DB_PWD, DB_HOST, DB_NAME
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer

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
    def __str__(self):  # to prevent programmer mistakes causing infinite recursion
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
    def __tablename__(cls):  # @NoSelf
        return cls.__name__.lower()
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column(Integer, primary_key = True)

# import the actual models here
from post import Post
from comment import Comment
from vote import Vote
