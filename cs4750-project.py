from flask import Flask, render_template, redirect, url_for, request, get_flashed_messages
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from login_utilities import check_login
import psycopg2

# Take care of User model
class UserNotFoundException(Exception):
    pass

class User(UserMixin):
    """
    Provides a User model for Flask-Login authentication
    """

    # Main connection to the database
    CONN = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
    CUR = CONN.cursor()
    CUR.execute('SELECT id, pwd FROM users')
    USERS = dict(CUR.fetchall()) # [id: password, id2: password, ...]

    def __init__(self, id):
        if id not in self.USERS:
            raise UserNotFoundException
        self.id = id
        self.password = self.USERS[id]

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @classmethod
    def get(cls, id):
        """
        Returns the password associated with the given username if the account exists
        """
        try:
            return cls.USERS[id]
        except KeyError:
            return None

# Begin Flask run

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SUPER SECRET KEY'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    hashed_pwd = User.get(id)
    if hashed_pwd is not None:
        return User(id)
    return None


@app.route('/')
def hello_world():
    return 'Hello World!'

@login_required
@app.route('/admin')
def admin_cp():
    return render_template('admin_cp.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Validate credentials
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pwd = User.get(username)
        if hashed_pwd and check_login(username, password):
            user = User(username)
            login_user(user)
            return redirect(url_for('admin_cp'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('loggedout.html')

# Variable rules example
@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username

if __name__ == '__main__':
    app.run(debug=True)
