'''
Created on Nov 22, 2012

@author: stum
'''
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table, create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.exc import NoResultFound

from datetime import datetime
from time import mktime

Base = declarative_base()
engine = create_engine('sqlite:///local.db')
Session = scoped_session(sessionmaker(bind=engine))

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
        return str(self.__class__)+"!!"
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

