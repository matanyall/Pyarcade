from pyarcade.base import Base
from sqlalchemy import Column, Integer, String


class GameDB(Base):
    __tablename__ = 'GameDB'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    # TODO: fix the security!
    save_name = Column(String(255))
    saved_game_path = Column(String)

    def __repr__(self):
        return '<GameDB(id={0}, player_id="{1}", save_name="{2}", saved_game_path="{3}")>'.format(self.id,
                                                                                                  self.player_id,
                                                                                                  self.save_name,
                                                                                                  self.saved_game_path)
