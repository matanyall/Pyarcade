from typing import Optional
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import pickle

from pyarcade.base import Base
from pyarcade.user import User
from pyarcade.gamedb import GameDB


class Model():
    """Class to create the database and interact with it
    """
    def __init__(self):
        """ instantiates the database and creates the session
        """
        # Create the engine. echo=(True|False) reflects the state of SQLAlchemy logging.
        # TODO: Fix password security issues.
        self.engine = sqlalchemy.create_engine('mysql+pymysql://root@db:3306/pyarcadedb',
                echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def begin_nested(self) -> None:
        """Issue a new SAVEPOINT for rollbacks.
        """
        self.session.begin_nested()

    def rollback(self) -> None:
        """Roll back the session to the last SAVEPOINT.
        """
        self.session.rollback()

    def _sanitize(self, ip: str) -> str:
        """Guard against dangerous user input.

        Args:
            ip (String): user input string

        Returns:
            str: 'safe' user input string
        """
        # TODO: Use a whitelist to only allow acceptable inputs.
        return ip

    def add_user(self, username: str, passwd: str, confirm: str) -> bool:
        """Add a user account to the app.

        Args:
            username (str): username of the user
            passwd (str): password
            confirm (str): password confirmation

        Returns:
            bool: whether the user was registered successfully
        """
        safe_username = self._sanitize(username)
        safe_passwd = self._sanitize(passwd)

        if safe_passwd != confirm or self._get_user(safe_username):
            return False

        user = User(username=safe_username, passwd=safe_passwd)
        self.session.add(user)
        self.session.commit()
        return True

    def _get_user(self, username: str, passwd: Optional[str] = None) -> User:
        """Get a registered user.

        Args:
            username (str): username of the user
            passwd (Optional[str], optional): password of the user. Defaults to
            None.

        Returns:
            User: user data for the user with username (and passwd, if included)
        """
        safe_username = self._sanitize(username)
        if passwd:
            safe_passwd = self._sanitize(passwd)

        user = None
        if passwd:
            user = self.session.query(User)\
                    .filter(User.username == safe_username)\
                    .filter(User.passwd == safe_passwd)\
                    .first()
        else:
            # Note that usernames should be unique.
            user = self.session.query(User)\
                    .filter(User.username == safe_username)\
                    .first()
        return user

    def authenticate_user(self, username: str, passwd: str) -> bool:
        """Authenticate user login information.

        Args:
            username (String): username of the user to be logged in
            passwd (String): password corresponding to the user

        Returns:
            bool: whether the user was logged in successfully
        """
        safe_username = self._sanitize(username)
        safe_passwd = self._sanitize(passwd)

        # Query the database for a user that has the username and password.
        user = self._get_user(safe_username, safe_passwd)

        # Return whether the login was successful.
        return bool(user)

    def delete_user(self, username: str) -> None:
        """Delete a user by dropping their data.

        Args:
            username (str): username of user to be deleted
        """
        pass

    def save_game(self, game_object, save_name: str, user_id: int):
        """Saves a game object through pickling

        Args: 
            game_object (BLOB): game object to be pickled and saved in database
            save_name (str): name of the save for later reference
            user_id (int): unique identifier associated with user
        
        returns:
            None
        """
        game_pickle = pickle.dumps(game_object)
        game = GameDB(player_id=user_id, save_name=save_name, save=game_pickle)
        self.session.add(game)
        self.session.commit()

    def save_game_by_username(self, game_object, save_name, username):
        """saves a game and associates it with a given username, this takes the place of userid

        Args:
            game_object (BLOB): game object to be pickled and saved in database
            save_name (str): name of the save for later reference
            username (str): username to be associated with game save 
        
        Returns:
            None
        """
        user_id = self._get_user(username)
        return self.save_game(game_object, save_name, user_id.id)

    def load_game(self, save_name: str, username: int):
        """retrieves game save from database

        Args: 
            save_name (str): name of the save to query database with
            username (str): name of user to query database with
        
        Return:
            game object: game object that is unpickled 
        """
        user_id = self._get_user(username)
        game = self.session.query(GameDB).filter(GameDB.user_id == user_id.id).filter(
            GameDB.save_name == save_name).first()
        result = pickle.loads(game.save)
        return result

    def list_saves(self, username: str):
        """ returns list of saves associated with user id

        Args:
            username (str): used to query database for save list
        
        Returns:
            List: list of saves associated with user
        """
        user_id = self._get_user(username)
        save_list = self.session.query(GameDB).filter(GameDB.user_id == user_id.id).all()
        return save_list

    def get_save(self, save_name: str, username: str):
        """ returns save object
        
        Args:
            save_name (str) : name associated with save
            username (str): used to query database for save list
            
        
        Returns:
            BLOB: save object 
        """
        user_id = self._get_user(username)
        save = self.session.query(GameDB).filter(GameDB.user_id == user_id.id).filter(
            GameDB.save_name == save_name).first()
        return save

    def delete_save(self, save_name: str, user_id: int):
        """deletes a save 
        
        Args:
            save_name (str): name of the save
            user_id (int): unique id of user
        """
        pass
