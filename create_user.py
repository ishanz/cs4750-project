import psycopg2
import bcrypt

# Contains a list of useful functions for manual account creation

def get_hash(pwd):
    return bcrypt.hashpw(pwd, bcrypt.gensalt())

def check_pwd(plaintext, hashed):
    """
    :param plaintext: the plaintext password the user has entered
    :param hashed: the hashed password retrieved from the database
    :return: if the user's entered password matches the one in the database
    """
    return bcrypt.hashpw(plaintext, hashed) == hashed

def create_user(username, password, account_type):
    """
    :param username
    :param password
    """

    # Hash the plaintext password
    h = bcrypt.hashpw(password, bcrypt.gensalt())

    # Connect to the database
    conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
    cur = conn.cursor()

    # Execute the insertion query and commit the changes
    cur.execute("INSERT INTO users VALUES ('" + username + "', '" + h + "', '" + account_type + "');")
    conn.commit()

    # Check the result
    cur.execute("SELECT * FROM users")
    print cur.fetchall()

    # Close the connection
    cur.close()
    conn.close()

def check_login(username, password):
    """
    Checks the login credentials against the database with hashing
    :param username:
    :param password:
    :return: True if the parameterized credentials are valid
    """

    authorized_login = False # Are the credentials valid?

    # Connect to the database
    conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
    cur = conn.cursor()

    # Grab entry from database with username
    cur.execute("SELECT * FROM users \n"
                "WHERE id = '" + username + "';")
    results = cur.fetchall() # Returns an array of tuples (id, hashed_pwd, account_type)
    cur.close()
    conn.close()

    # Check entered credentials against database entry
    if len(results) == 0:
        print 'Found no results.'
    else:
        user = results[0]
        hashed_pwd = user[1]
        authorized_login = check_pwd(password, hashed_pwd)

    return authorized_login


# create_user('admin', 'password', 'admin')
print check_login('admin', 'password')