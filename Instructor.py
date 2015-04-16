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

    def show_assignments(self, cid):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        cur.execute("SELECT assignment_id, file_path_assignment FROM assigns2 WHERE course_id= '" + cid + "';")
        assignment_list = cur.fetchall()
        print assignment_list
        cur.close()
        conn.close()
        return assignment_list

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

    def show_resources(self, cid):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        cur.execute("SELECT resource_name, file_path_resource FROM resources WHERE course_id= '" + cid + "';")
        resource_list = cur.fetchall()
        print resource_list
        cur.close()
        conn.close()
        return resource_list

    def show_submissions(self, cid):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        cur.execute("SELECT id, first_name,last_name, assignment_id, file_path_submission, submission_grade "
                    "FROM submits1 NATURAL JOIN submits2 NATURAL JOIN submits3 WHERE course_id= '" + cid + "';")
        submission_list = cur.fetchall()
        print submission_list
        cur.close()
        conn.close()
        return submission_list



