from flask import request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required,\
        logout_user, current_user
from typing import List
from pyarcade.input_system import InputSystem
import pickle

input_system = InputSystem()
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    high_scores = db.relationship('HighScore', backref='user', lazy=True)


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
    __tablename__ = 'Games'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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


class HighScore(db.Model):
    __tablename__ = 'HighScores'

    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(32), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)


class HighScoreListResource(Resource):
    """Respond to REST API requests GET and POST at the generic URL /high_scores.
    """

    def get(self) -> List[dict]:
        """Get all high scores.

        Returns:
            List[dict]: all high scores
        """
        return [{
                "id": high_score.id,
                "game_name": high_score.game_name,
                "score": high_score.score,
                "user_id": high_score.user_id
                } for high_score in HighScore.query.all()]

    def post(self) -> dict:
        """Add a high score.

        Returns:
            dict: high score that is created
        """
        new_high_score = HighScore(
                game_name=request.json["game_name"],
                score=request.json["score"],
                user_id=request.json["user_id"
                ])
        db.session.add(new_high_score)
        db.session.commit()
        return {
                "id": new_high_score.id,
                "game_name": new_high_score.game_name,
                "score": new_high_score.score,
                "user_id": new_high_score.user_id
                }


class HighScoreResource(Resource):
    """Respond to REST API requests GET, PATCH, and DELETE at the specific URL
    /high_scores/<int:high_score_id>.
    """

    def get(self, high_score_id: int) -> dict:
        """Get a high score specified by high_score_id.

        Args:
            high_score_id (int): ID of the high score to get

        Returns:
            dict: information associated with the specified high score
        """
        high_score = HighScore.query.get_or_404(high_score_id)
        return {
                "game_name": high_score.game_name,
                "score": high_score.score,
                "user_id": high_score.user_id
                }

    def patch(self, high_score_id: int) -> dict:
        """Update an existing high score.

        Args:
            high_score_id (int): ID of the high score to update

        Returns:
           dict: information associated with the updated high score
        """
        high_score = HighScore.query.get_or_404(high_score_id)
        high_score.score = request.json['score']
        db.session.commit()
        return {
                "game_name": high_score.game_name,
                "score": high_score.score,
                "user_id": high_score.user_id
                }

    def delete(self, high_score_id: int) -> dict:
        """Delete an existing high score.

        Args:
            high_score_id (int): ID of the high score to delete

        Returns:
           dict: information associated with the deleted high score
        """
        high_score = HighScore.query.get_or_404(high_score_id)
        db.session.delete(high_score)
        db.session.commit()
        return {
                "game_name": high_score.game_name,
                "score": high_score.score,
                "user_id": high_score.user_id
                }, 204


# General high score requests can be made at /high_scores.
api.add_resource(HighScoreListResource, '/high_scores')
# Specific high score requests can be made using a high score ID.
api.add_resource(HighScoreResource, '/high_scores/<int:high_score_id>')


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')


class RegisterForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=8, max=80)])
    confirm = PasswordField('Confirm Password:', validators=[
            InputRequired(), EqualTo('password', message='Passwords must match')])


class GameForm(FlaskForm):
    input = StringField()


class SaveForm(FlaskForm):
    save_name = StringField(validators=[InputRequired(), Length(min=2, max=15)])


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


# Note that /games is already mapped to issue HTTP responses so we can't use
# /games/* here.
@app.route('/game')
@login_required
def game():
    """Serve as a placeholder to display the game selection menu.
    """
    return redirect(url_for('dashboard'))


@app.route('/game/<game>')
@login_required
def game_menu(game):
    """Render a custom game menu for all games.

    Args:
        game (str): URL extension for the game to display the menu of
    """
    game_subdir = game

    # Redirect users to the game selection menu.
    if game_subdir not in input_system.get_supported_games().keys():
        return redirect(url_for('dashboard'))

    return render_template('game_menu.html',
            game_name=input_system.get_supported_games().get(game_subdir),
            game_subdir=game_subdir
            )


"""
@app.route('/minesweeper', methods=['GET', 'POST'])
def minesweeper():
    form = GameForm()

    user_input = "New Game"
    output_lines = ""
    if input_system.get_current_game():
        input_system.game_to_load = input_system.current_game
        user_input = "Continue"

    if request.method == "POST":
        if form.validate_on_submit():
            user_input = form.input.data
            output_lines = input_system.handle_game_input('minesweeper', user_input)
        else:
            game_option = request.form["option"]
            if game_option == "Quit":
                input_system.set_current_game(None)
                return redirect(url_for('dashboard'))
            elif game_option == "Save":
                return redirect(url_for('save'))
            elif game_option == "Help":
                flash(input_system.handle_game_input('minesweeper', game_option.lower()), 'info')
                return redirect(url_for('minesweeper'))
            else:
                output_lines = input_system.handle_game_input('minesweeper', game_option.lower())

    if user_input == "New Game":
        output_lines = input_system.handle_game_input('minesweeper', user_input)

    grid = input_system.minesweeper_game.hidden_grid
    output_grid = [['-'] * (len(grid) + 1) for _ in range(len(grid) + 1)]
    for row_idx in range(len(grid) + 1):
        for col_idx in range(len(grid) + 1):
            if row_idx == 0 and col_idx == 0:
                output_grid[row_idx][col_idx] = " "
            elif row_idx == 0 and col_idx > 0:
                output_grid[row_idx][col_idx] = str(col_idx - 1)
            elif row_idx > 0 and col_idx == 0:
                output_grid[row_idx][col_idx] = str(row_idx - 1)
            elif row_idx > 0 and col_idx > 0:
                if input_system.minesweeper_game.game_state != "Game over." and grid[row_idx - 1][col_idx - 1] == '*':
                    output_grid[row_idx][col_idx] = " - "
                else:
                    output_grid[row_idx][col_idx] = grid[row_idx - 1][col_idx - 1]

    output_lines = output_lines.splitlines()
    output = ""
    if len(output_lines) > 0:
        if len(output_lines) == 1 or output_lines[0] == "Game reset":
            output = output_lines[0]
        elif "===" not in output_lines[len(output_lines)-1]:
            output = output_lines[len(output_lines)-1]

    return render_template('minesweeper.html', form=form, output_grid=output_grid, game_status=output)
"""


@app.route('/game/<game>/play', methods=['GET', 'POST'])
@login_required
def play(game):
    game_subdir = game  # alias for clarity
    form = GameForm()

    user_input = "New Game"
    if input_system.get_current_game():
        input_system.game_to_load = input_system.current_game
        user_input = "Continue"

    curr_game_name = input_system.get_supported_games().get(game_subdir)
    if request.method == "POST":
        if form.validate_on_submit():
            user_input = form.input.data
            output_lines = input_system\
                    .handle_game_input(curr_game_name, user_input)\
                    .splitlines(False)

            return render_template(f'{game_subdir}.html',
                    game_name=curr_game_name,
                    game_subdir=game_subdir,
                    form=form,
                    output_lines=output_lines
                    )
        else:
            game_option = request.form["option"]
            if game_option == "Quit":
                input_system.set_current_game(None)
                return redirect(url_for('dashboard'))
            elif game_option == "Save":
                return redirect(url_for('save', game=game_subdir))
            elif game_option == "Help":
                flash(input_system.handle_game_input(curr_game_name, game_option.lower()), 'info')
                return redirect(url_for('play', game=game_subdir))
            else:
                output_lines = input_system\
                        .handle_game_input(curr_game_name, game_option.lower())\
                        .splitlines(False)

                return render_template(f'{game_subdir}.html',
                        game_name=curr_game_name,
                        game_subdir=game_subdir,
                        form=form,
                        output_lines=output_lines
                        )

    output_lines = input_system.handle_game_input(curr_game_name, user_input)\
            .splitlines(False)

    return render_template(f'{game_subdir}.html',
            game_name=curr_game_name,
            game_subdir=game_subdir,
            form=form,
            output_lines=output_lines
            )


# TODO: Add global and user high score filters.
@app.route('/game/<game>/high_scores')
@login_required
def high_scores(game):
    """Display the high scores for a game.

    Args:
        game (str): game to display high scores for
    """
    # Display the global high scores for now. Only display the top 10.
    curr_game_name = input_system.get_supported_games().get(game)
    scores = HighScore.query.filter_by(game_name=curr_game_name).limit(10).all()
    return render_template('high_scores.html',
            game_name=curr_game_name,
            high_scores=scores
            )


@app.route('/game/<game>/save', methods=['GET', 'POST'])
@login_required
def save(game):
    form = SaveForm()

    if form.validate_on_submit():
        save = Game.query.filter_by(save_name=form.save_name.data).first()
        if save and save.player_id == current_user.id:
            flash('Save name already exists. Please choose another', 'danger')
            return render_template('save.html', form=form)

        current_game = input_system.get_current_game()
        game_pickle = pickle.dumps(current_game)
        new_save = Game(player_id=current_user.id, save_name=form.save_name.data,
                        save=game_pickle)

        db.session.add(new_save)
        db.session.commit()

        flash(f'{form.save_name.data} successfully saved!', 'success')
        return redirect(url_for('play', game=game))

    return render_template('save.html', game_subdir=game, form=form)


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
        login_user(new_user)

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('dashboard'))

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
