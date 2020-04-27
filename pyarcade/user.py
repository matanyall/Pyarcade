from pyarcade.base import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    # TODO: fix the security!
    passwd = Column(String(255))

    def __repr__(self):
        return '<User(id={0}, username="{1}", password="{2}")>'.format(self.id,
                                                                       self.username, self.passwd)
