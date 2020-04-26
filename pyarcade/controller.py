import pickle
from typing import Optional

import sqlalchemy
from pyarcade.base import Base
from pyarcade.gamedb import GameDB
from pyarcade.user import User
from sqlalchemy.orm import sessionmaker


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
        # root = Path(".")
        # file_name = save_name + "_" + str(user_id) + ".gs"
        # path = root / 'pyarcade_extension/' / 'pyarcade' / 'data/' / file_name
        # Path(path).touch()
        # path_name_2 = "/home/matanya/Documents/SPRING2020/CMSC435/FinalPyarcadeExtension/pyarcade_extension/pyarcade/data/"
        # path_name_2 = path_name_2 + file_name
        # print(os.getcwd())
        # path = Path(".")
        # path = path / 'test_file.gs'

        # open(path_name, 'wb') as file_descriptor:

        # with path.open('wb') as file_descriptor:
        #     pickle.dump(game_object, file_descriptor)
        # print(path.cwd())

        game_pickle = pickle.dumps(game_object)

        game = GameDB(player_id=user_id, save_name=save_name, save=game_pickle)
        self.session.add(game)
        self.session.commit()

    def load_game(self, save_name: str, username: int):
        user_id = self.__get_user(username)
        game = self.session.query(GameDB).filter(GameDB.player_id == user_id.id).filter(
            GameDB.save_name == save_name).first()
        result = pickle.loads(game.saved)
        return result
        # root = os.getcwd()
        # file_name = save_name + "_" + str(user_id) + ".gs"
        # path_name = root + "/data/" + file_name
        # path_name_2 = "/home/matanya/Documents/SPRING2020/CMSC435/FinalPyarcadeExtension/pyarcade_extension/pyarcade/data/"
        # path_name_2 = path_name_2 + file_name
        # with open(path_name, 'rb') as game_save:
        #     game_object = pickle.load(game_save)
        # return game_object

    def list_saves(self, username: str):
        user_id = self.__get_user(username)
        save_list = self.session.query(GameDB).filter(GameDB.player_id == user_id.id).all()
        return save_list

    def get_save(self, save_name: str, username: str):
        user_id = self.__get_user(username)
        save = self.session.query(GameDB).filter(GameDB.player_id == user_id.id).filter(
            GameDB.save_name == save_name).first()
        return save

    def delete_save(self, save_name: str, user_id: int):
        pass
