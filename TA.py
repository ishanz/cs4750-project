import psycopg2

class TA:

     def __init__(self, username):
         self.username = username

    def show_courses(self):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        cur.execute("SELECT course_id, credits, course_name FROM assists2 natural join assists3 "
                    "WHERE id ='" + self.username + "';")
        course_data = cur.fetchall()
        print course_data
        cur.close()
        conn.close()
        return course_data



