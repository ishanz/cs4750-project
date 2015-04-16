import psycopg2

class Instructor:
    """ Contains database logic for Instructor functions
    """

    def __init__(self, username):
        self.username = username


    def show_courses(self):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        cur.execute("SELECT course_id, credits, course_name FROM teaches2 "
                    "WHERE id ='" + self.username + "';")
        course_data = cur.fetchall()
        print course_data
        cur.close()
        conn.close()
        return course_data

    def show_students(self, cid):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        cur.execute("SELECT id, first_name, last_name, course_grade FROM takes1 NATURAL JOIN takes3 "
                    "WHERE course_id ='" + cid + "';")
        student_list = cur.fetchall()
        print student_list
        cur.close()
        conn.close()
        return student_list


