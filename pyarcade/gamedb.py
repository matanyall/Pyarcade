from pyarcade.base import Base
from sqlalchemy import Column, Integer, String, BLOB


class GameDB(Base):
    """game class that represents the model to create a game resource. Primarily represents a game and its
    save state

    Args:
        id (int): primary key that uniquely identifies a save 
        player_id (int): key that uniquely identifies a user and is associated with this save
        save_name (str): name of the save
        save (BLOB): game object being saved
    """
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
