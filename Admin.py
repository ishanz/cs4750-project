import psycopg2

class Admin:

    def __init__(self, username):
        self.username = username

    def show_courses(self):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        cur.execute("SELECT course_id, credits, course_name FROM teaches2;")
        course_data = cur.fetchall()
        print course_data
        cur.close()
        conn.close()
        return course_data

    def show_all_users(self):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        cur.execute("SELECT id, first_name, last_name, account_type FROM users;")
        user_list = cur.fetchall()
        print user_list
        cur.close()
        conn.close()
        return user_list

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

    def show_professor(self, cid):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        cur.execute("SELECT id, first_name, last_name FROM teaches1 NATURAL JOIN teaches2 "
                    "WHERE course_id ='" + cid + "';")
        professor = cur.fetchall()
        print professor
        cur.close()
        conn.close()
        return professor

    def show_tas(self, cid):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        cur.execute("SELECT id, first_name,last_name FROM assists1 NATURAL JOIN assists3 WHERE course_id= '" + cid + "';")
        ta_list = cur.fetchall()
        print ta_list
        cur.close()
        conn.close()
        return ta_list

    def create_course(self, course_id, credits, course_name, id):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        add_course = ("INSERT INTO teaches2 "
                        " (course_id, credits, course_name, id) "
                            "VALUES (%(cid)s, %(cred)s, %(cname)s, %(ide)s)")
        data = {'cid':course_id, 'cred':credits, 'cname':course_name, 'ide':id}
        cur.execute(add_course, data)
        cur.close()
        conn.close()


