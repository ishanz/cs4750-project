import psycopg2

class Student:
    """ Handles Student interactions with the database instance
    """

    def __init__(self, username):
        self.username = username

    def show_courses(self):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        cur.execute("SELECT course_id, course_name, id, course_grade FROM takes3 NATURAL JOIN takes2 "
                    "WHERE id ='" + self.username + "';")
        course_data = cur.fetchall()
        print course_data
        cur.close()
        conn.close()
        return course_data

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
        cur.execute("SELECT assignment_id, file_path_submission, submission_grade "
                    "FROM submits1 NATURAL JOIN submits2 NATURAL JOIN submits3 WHERE course_id= '" + cid +
                    " AND id = " + self.username + "';")
        submission_list = cur.fetchall()
        print submission_list
        cur.close()
        conn.close()
        return submission_list

    def submit_assignment(self, assignment_id, file_path_submission):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        submit_ass = "INSERT INTO submits3(id, assignment_id, file_path_submission, submission_grade) " \
                     "VALUES (%s, %s, %s, %s)"
        cur.execute(submit_ass, (self.username, assignment_id, file_path_submission, 100.0))
        conn.commit()
        cur.close()
        conn.close()

