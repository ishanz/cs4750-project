from flask import Flask, render_template, redirect, url_for, request, get_flashed_messages
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from login_utilities import check_login
from models import User
from functools import wraps

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

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.get_role() not in roles:
                return login_manager.unauthorized()
            return f(*args, **kwargs)
        return wrapped
    return wrapper

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/control/admin')
@login_required
@requires_roles('admin')
def admin_cp():
    return render_template('admin_cp.html')

@app.route('/control/student')
@login_required
@requires_roles('student')
def student_cp():
    return render_template('student_cp.html')

@app.route('/control/ta')
@login_required
@requires_roles('ta')
def ta_cp():
    return render_template('ta_cp.html')

@app.route('/control/instructor_cp')
@login_required
@requires_roles('instructor')
def instructor_cp():
    return render_template('instructor_cp.html')


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
            if user.get_role() == 'admin':
                return redirect(url_for('admin_cp'))
            elif user.get_role() == 'student':
                return redirect(url_for('student_cp'))
            elif user.get_role() == 'ta':
                return redirect(url_for('ta_cp'))
            elif user.get_role() == 'instructor':
                return redirect(url_for('instructor_cp'))
            else:
                return redirect(url_for('hello_world'))
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
