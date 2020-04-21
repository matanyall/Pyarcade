from pyarcade.base import Base
from pyarcade.user import User
import sqlalchemy
from sqlalchemy.orm import sessionmaker


class Controller():
    """[summary]
    """
    def __init__(self):
        # TODO: fix credentials!!!
        self.engine = sqlalchemy.create_engine('mysql+pymysql://root@db:3306/pyarcadedb',
                echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    # 
    # HELPERS
    # 
    def sanitize(ip: str):
        # TODO: fix this NOW!
        return ip

    # 
    # ACCESS
    # 
    def authenticate(username: str, passwd: str):
        """Authenticate user login information.
        
        Args:
            username (String): username of the user to be logged in
            passwd (String): password corresponding to the user
        """
        # Query the database for a user that has the username and password.

        # Return whether the login was successful.

    # 
    # USER
    # 
    def register(username: str, passwd: str, confirm: str) -> bool:
        """Register a user account with the app.
        
        Args:
            username (str): username of the user
            passwd (str): password
            confirm (str): confirm password field
        
        Returns:
            bool: whether the user was registered successfully
        """
        if passwd != confirm or not get_user(username):
            return False

        safe_username = sanitize(username)
        safe_passwd = sanitize(passwd)

        user = User(username=safe_username, passwd=safe_passwd)
        self.session.add(user)
        self.session.commit()

    def get_user(username: str) -> User:
        """Get a registered user.
        
        Args:
            username (str): username of the user
        
        Returns:
            User: user data for the user with username
        """
        safe_username = sanitize(username)

        # Note that usernames should be unique.
        user = session.query(User).filter(User.username==safe_username).first()
        return user
