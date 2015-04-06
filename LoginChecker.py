import psycopg2
import hashlib
import uuid

class LoginChecker:
    """ Checks login credentials against the RDS PostgreSQL instance and logs the user in
    """

    def __init__(self):
        self.conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")

    def check_login(self, username, password):
        """Check credentials against database and return the result"""
        cur = self.conn.cursor()
        cur.execute('SELECT *'
                    'FROM users')
        all_credentials = cur.fetchall()
        print all_credentials


    def __check_password(self, password):
        hashed_password = self.__hash_password(password)
        cur = self.conn.cursor()
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + password.encode()).hexdigest()


    def __hash_password(self, password):
        """Used for account creation -- not necessarily relevant here"""
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    def func(self):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM users')
        print cur.fetchall()



x = LoginChecker()
x.check_login('username', 'password')