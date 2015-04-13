from flask.ext.login import UserMixin
import psycopg2

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
    CUR.execute('SELECT * FROM users')
    USERS = CUR.fetchall() # schema [id, pwd, account_type]

    def __init_(self, id):
        if not id in self.USERS:
            raise UserNotFoundException
        self.id = id
        self.password = self.USERS[pwd]