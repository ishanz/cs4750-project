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

     def grade_submission(self, id, assignment_id, file_path, submission_grade, course_id):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()

        # Update the row that the student has already inserted with the submission grade
        update_grade = "UPDATE submits3 " \
                       "SET submission_grade = %s " \
                       "WHERE id = %s and assignment_id = %s and file_path_submission = %s"
        cur.execute(update_grade, (submission_grade, id, assignment_id, file_path))
        conn.commit()

        # Update the course grade
        get_student_grades = "SELECT submission_grade FROM submits1 NATURAL JOIN submits3 " \
                             "WHERE course_id = %s AND id = %s;"
        cur.execute(get_student_grades, (course_id, id))
        student_grades = cur.fetchall() # [(num1,), (num2,), ...]
        sum = 0
        num_grades = len(student_grades)
        average_grade = 0.0
        for grade_tuple in student_grades:
            grade = grade_tuple[0]
            sum += grade
        average_grade = sum/num_grades
        update_course_grade = "UPDATE takes3 " \
                              "SET course_grade = %s " \
                              "WHERE course_id = %s AND id = %s"
        cur.execute(update_course_grade, (average_grade, course_id, id))
        conn.commit()

        cur.close()
        conn.close()

     def remove_submission(self, id, assignment_id, course_id):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()

        delete_sub = "DELETE FROM submits3 WHERE id = %s AND assignment_id = %s"
        cur.execute(delete_sub, (id, assignment_id))
        conn.commit()

        # Update the course grade
        get_student_grades = "SELECT submission_grade FROM submits1 NATURAL JOIN submits3 " \
                             "WHERE course_id = %s AND id = %s;"
        cur.execute(get_student_grades, (course_id, id))
        student_grades = cur.fetchall() # [(num1,), (num2,), ...]
        sum = 0
        num_grades = len(student_grades)
        average_grade = 0.0
        for grade_tuple in student_grades:
            grade = grade_tuple[0]
            sum += grade
        if num_grades > 0:
            average_grade = sum/num_grades
        else:
            average_grade = 100
        update_course_grade = "UPDATE takes3 " \
                              "SET course_grade = %s " \
                              "WHERE course_id = %s AND id = %s"
        cur.execute(update_course_grade, (average_grade, course_id, id))
        conn.commit()

        cur.close()
        conn.close()

     def create_resource(self, course_id, resource_name, file_path):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()

        create_res = "INSERT INTO resources(course_id, resource_name, file_path_resource) VALUES(%s, %s, %s)"
        cur.execute(create_res, (course_id, resource_name, file_path))
        conn.commit()

        cur.execute("SELECT * FROM resources")
        print cur.fetchall()

        cur.close()
        conn.close()

     def get_course_data(self, cid):
        conn = psycopg2.connect("dbname='ClassManagementSystem' user='username' "
                                     "host='cs4750.cq8mqtnic7zz.us-west-2.rds.amazonaws.com' password='password'")
        cur = conn.cursor()
        cur.execute("SELECT course_id, credits, course_name FROM teaches2 "
                    "WHERE course_id ='" + cid + "';")
        course_data = cur.fetchall()
        course_data = course_data[0]
        cur.close()
        conn.close()
        return course_data

