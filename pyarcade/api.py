from flask import request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from typing import List
from pyarcade.input_system import InputSystem

input_system = InputSystem()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'd9eae96b0e36281c7de5759e5d1aa7740426000710b2db47'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@db:3306/pyarcadedb'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    """ A SQLAlchemy Model used to store information about a user. This only
    needs to have a collection of class variables that are of type db.Column.
    """
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    passwd = db.Column(db.String(255), unique=False, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserListResource(Resource):
    """ A Resource is a collection of routes (think URLs) that map to these functions.
    For a REST API, we have GET, PUT, POST, PATCH, DELETE, etc. Here we just define
    functions that map to the REST API verbs, later we map this to a specific URL
    with api.add_resource
    """

    def get(self) -> List[dict]:
        """Responds to http://[domain or IP]:[port (default 5000)]/users

        Returns:
            List of dictionaries describing all users in the database. We should only include some information if
            passwords or other personal information is involved.
        """
        return [{"username": user.username, "id": user.id} for user in User.query.all()]

    def post(self) -> dict:
        """Responds to http://[domain or IP]:[port (default 5000)]/users.

        Adds a new user to the database.

        Returns:
            Dictionary describing user that was just created.
        """
        new_user = User(username=request.json['username'], passwd=request.json['password'])
        db.session.add(new_user)
        db.session.commit()
        return {"username": request.json["username"]}


class UserResource(Resource):
    """ UserResource is slightly different from UserListResource as these functions will only respond
    to Responds to http://[domain or IP]:[port (default 5000)]/users/<user_id> so these are always
    executed in the context of a specific user.

    """

    def get(self, user_id):
        """Responds to http://[domain or IP]:[port (default 5000)]/users/<user_id>

        Returns:
            Dictionary describing user by user_id
        """
        user = User.query.get_or_404(user_id)
        return {"id": user.id, "username": user.username}

    def patch(self, user_id):
        """Responds to http://[domain or IP]:[port (default 5000)]/users/<user_id>

        This is used to update an existing user.

        Returns:
           Dictionary describing user that was changed.
        """
        user = User.query.get_or_404(user_id)

        if 'username' in request.json:
            user.username = request.json['username']

        db.session.commit()
        return {"id": user.id, "username": user.username}

    def delete(self, user_id):
        """Responds to http://[domain or IP]:[port (default 5000)]/users/<user_id>

        This is used to delete an existing user

        Returns:
           Dictionary describing user that was changed.
        """
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

class Game(db.Model):
    __tablename__ = 'GameDB'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, primary_key=True)
    save_name = db.Column(db.String(128), unique=True, nullable=False)
    save = db.Column(db.BLOB, unique=False, nullable=False)

class GameListResource(Resource):
    """ A Resource is a collection of routes (think URLs) that map to these functions.
    For a REST API, we have GET, PUT, POST, PATCH, DELETE, etc. Here we just define
    functions that map to the REST API verbs, later we map this to a specific URL
    with api.add_resource
    """

    def get(self) -> List[dict]:
        """Responds to http://[domain or IP]:[port (default 5000)]/game

        Returns:
            List of dictionaries describing all games in the database.
        """
        return [{"save_name": game.save_name, "id": game.id} for game in Game.query.all()]

    def post(self) -> dict:
        """Responds to http://[domain or IP]:[port (default 5000)]/games.

        Adds a new game to the database.

        Returns:
            Dictionary describing game that was just created.
        """
        new_save = Game(player_id=request.json['player_id'], save_name=request.json['save_name'],
                        save=request.json['save'])
        db.session.add(new_save)
        db.session.commit()
        return {"save_name": request.json["save_name"]}


class GameResource(Resource):
    """ GameResource is slightly different from GameListResource as these functions will only respond
    to Responds to http://[domain or IP]:[port (default 5000)]/games/<game_id> so these are always
    executed in the context of a specific game.

    """

    def get(self, game_id):
        """Responds to http://[domain or IP]:[port (default 5000)]/games/<game_id>

        Returns:
            Dictionary describing user by game_id
        """
        game = Game.query.get_or_404(game_id)
        return {"id": game.id, "save_name": game.save_name}

    def patch(self, game_id):
        """Responds to http://[domain or IP]:[port (default 5000)]/games/<game_id>

        This is used to update an existing game.

        Returns:
           Dictionary describing game that was changed.
        """
        game = Game.query.get_or_404(game_id)

        if 'save_name' in request.json:
            game.save_name = request.json['save_name']

        db.session.commit()
        return {"id": game.id, "save_name": game.save_name}

    def delete(self, game_id):
        """Responds to http://[domain or IP]:[port (default 5000)]/games/<game_id>

        This is used to delete an existing game

        Returns:
           Dictionary describing game that was changed.
        """
        game = Game.query.get_or_404(game_id)
        db.session.delete(game)
        db.session.commit()
        return '', 204


api.add_resource(GameListResource, '/games')
api.add_resource(GameResource, '/games/<int:game_id>')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class GameForm(FlaskForm):
    input = StringField()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mastermind', methods=['GET', 'POST'])
def mastermind():
    form = GameForm()

    user_input = "New Game"
    if request.method == "POST":
        if form.validate_on_submit():
            user_input = form.input.data
            output_lines = input_system.handle_game_input('mastermind', user_input).splitlines(False)
            return render_template('mastermind.html', form=form, output_lines=output_lines)
        else:
            game_option = request.form["option"]
            if game_option == "Quit":
                return redirect(url_for('dashboard'))
            else:
                output_lines = input_system.handle_game_input('mastermind', game_option.lower()).splitlines(False)
                return render_template('mastermind.html', form=form, output_lines=output_lines)

    output_lines = input_system.handle_game_input('mastermind', user_input).splitlines(False)
    return render_template('mastermind.html', form=form, output_lines=output_lines)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.passwd == form.password.data:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already in use. Please choose another.', 'danger')
            return render_template('signup.html', form=form)

        new_user = User(username=form.username.data, passwd=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def create_app():
    """ This is used as a factory function for creating the entire application instance
    when the application is first run. Best practices for FLASK is to allow creating an
    application instance ONLY using this function for very good reasons, but this
    is good enough to use for now.
    """
    db.create_all()
    return app


if __name__ == "__main__":
    app.run(debug=True)
