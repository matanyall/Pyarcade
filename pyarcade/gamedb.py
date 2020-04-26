from pyarcade.base import Base
from sqlalchemy import Column, Integer, String, BLOB


class GameDB(Base):
    __tablename__ = 'GameDB'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    # TODO: fix the security!
    save_name = Column(String(255))
    save = Column(BLOB)

    def __repr__(self):
        return '<GameDB(id={0}, player_id="{1}", save_name="{2}", save="{3}")>'.format(self.id,
                                                                                       self.player_id,
                                                                                       self.save_name,
                                                                                       self.save)
