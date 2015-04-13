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
    CUR.execute('SELECT id, password FROM users')
    USERS = dict(CUR.fetchall()) # [id: password, id2: password, ...]

    def __init_(self, id):
        if not id in self.USERS:
            raise UserNotFoundException
        self.id = id
        self.password = self.USERS[id]

    @classmethod
    def get(self_class, id):
        """
        Returns a user instance of id or None if doesn't exist
        """
        try:
            return self_class(id)
        except UserNotFoundException:
            return None