from pyarcade.base import Base
from pyarcade.user import User
from pyarcade.gamedb import GameDB
from typing import Optional
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import pickle


# TODO: logically split the app. This is the model?


class Controller():
    """[summary]
    """

    def __init__(self):
        # Create the engine. echo=(True|False) reflects the state of SQLAlchemy logging.
        # TODO: fix password security issues.
        self.engine = sqlalchemy.create_engine('mysql+pymysql://root@db:3306/pyarcadedb',
                                               echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    #
    # HELPERS
    #
    def __sanitize(self, ip: str) -> str:
        """Guard against dangerous user input.

        Args:
            ip (String): user input string

        Returns:
            str: 'safe' user input string
        """
        # TODO: use a whitelist to only allow acceptable inputs.
        return ip

    #
    # ACCESS
    #
    def authenticate(self, username: str, passwd: str) -> bool:
        """Authenticate user login information.

        Args:
            username (String): username of the user to be logged in
            passwd (String): password corresponding to the user

        Returns:
            bool: whether the user was logged in successfully
        """
        safe_username = self.__sanitize(username)
        safe_passwd = self.__sanitize(passwd)

        # Query the database for a user that has the username and password.
        user = self.__get_user(safe_username, safe_passwd)

        # Return whether the login was successful.
        return bool(user)

    #
    # USER
    #
    def register(self, username: str, passwd: str, confirm: str) -> bool:
        """Register a user account with the app.

        Args:
            username (str): username of the user
            passwd (str): password
            confirm (str): confirm password field

        Returns:
            bool: whether the user was registered successfully
        """
        safe_username = self.__sanitize(username)
        safe_passwd = self.__sanitize(passwd)

        if safe_passwd != confirm or self.__get_user(safe_username):
            return False

        user = User(username=safe_username, passwd=safe_passwd)
        self.session.add(user)
        self.session.commit()
        return True

    def __get_user(self, username: str, passwd: Optional[str] = None) -> User:
        """Get a registered user.

        Args:
            username (str): username of the user
            passwd (Optional[str], optional): password of the user. Defaults to
            None.

        Returns:
            User: user data for the user with username
        """
        safe_username = self.__sanitize(username)
        if passwd:
            safe_passwd = self.__sanitize(passwd)

        user = None
        if passwd:
            user = self.session.query(User) \
                .filter(User.username == safe_username) \
                .filter(User.passwd == safe_passwd) \
                .first()
        else:
            # Note that usernames should be unique.
            user = self.session.query(User) \
                .filter(User.username == safe_username) \
                .first()
        return user

    def save_game_with_username(self, game_object, save_name, username):
        user_id = self.__get_user(username)
        return self.save_game(game_object, save_name, user_id.id)

    def save_game(self, game_object, save_name: str, user_id: int):
        file_name = "data/" + save_name + "_" + str(user_id) + ".gs"
        with open(file_name, 'wb') as file_descriptor:
            pickle.dump(game_object, file_name)

        game = GameDB(player_id=user_id, save_name=save_name, save_game_path=file_name)
        self.session.add(game)
        self.session.commit()


    def load_game(self, save_name: str, user_id: int):
        file_name = "data/" + save_name + "_" + str(user_id) + ".gs"
        with open(file_name, 'rb') as game_save:
            game_object = pickle.load(game_save)
        return game_object

    def list_saves(self, user_id: str):
        save_list = self.session.query(GameDB).filter(GameDB.player_id == user_id).all()
        return save_list

    def delete_save(self, save_name: str, user_id: int):
        pass
