'''
Created on Dec 23, 2012

@author: stum
'''
from isy.models import Base, StdMixin
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Enum, String

class Vote(StdMixin, Base):
    comment_id = Column(Integer, ForeignKey('comment.id'))
    direction = Column(Enum('UP', 'DOWN'))
    voter = Column(String(8))

    def __init__(self, comment, direction, voter):
        self.comment = comment
        self.direction = direction
        self.voter = voter

    def __str__(self):
        return "%s vote by %s on comment %s" % (self.direction, self.voter, self.comment_id)
