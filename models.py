from flask.ext.login import UserMixin
import psycopg2

# Take care of User model
class UserNotFoundException(Exception):
    pass

class User(UserMixin):
    """
    Provides a User model for Flask-Login authentication
    """

    # Main connection to the database
    # Fetch usernames, passwords, and account types
    CONN = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
    CUR = CONN.cursor()
    CUR.execute('SELECT id, pwd FROM users')
    USERS = dict(CUR.fetchall()) # [id: password, id2: password, ...]
    CUR.execute('SELECT id, account_type FROM users')
    ACCOUNT_TYPES = dict(CUR.fetchall()) # [id: account_type, id2: account_type2, ...]
    CUR.close()
    CONN.close()

    def __init__(self, id):
        if id not in self.USERS or id not in self.ACCOUNT_TYPES:
            raise UserNotFoundException
        self.id = id
        self.password = self.USERS[id]
        self.account_type = self.ACCOUNT_TYPES[id]

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_role(self):
        return self.account_type

    @classmethod
    def get(cls, id):
        """
        Returns the password associated with the given username if the account exists
        """
        try:
            return cls.USERS[id]
        except KeyError:
            return None