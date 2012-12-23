'''
Created on Dec 23, 2012

@author: stum
'''
from isy.models import Base, StdMixin, Session
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, DateTime, Text, Enum, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from isy.models.vote import Vote

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

    @staticmethod
    def get_by_id(comment_id):
        s = Session()
        try:
            return s.query(Comment).filter(Comment.id == comment_id).one()
        except NoResultFound:
            return None

    def __str__(self):
        c = (self.body[:10] + '...') if len(self.body) > 10 else self.body
        return "Comment <%s> on %s" % (c, self.post)

    def upvote(self, voter):
        vote = Vote(self, 'UP', voter)
        vote.add()

    def downvote(self, voter):
        vote = Vote(self, 'DOWN', voter)
        vote.add()
