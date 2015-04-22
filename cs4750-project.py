from flask import Flask, render_template, redirect, url_for, request, get_flashed_messages
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from login_utilities import check_login, create_user, delete_user
from models import User
from functools import wraps
from Instructor import Instructor
from Admin import Admin
from Student import Student
from TA import TA

# Begin Flask run

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SUPER SECRET KEY'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    hashed_pwd = User.get(id)
    if hashed_pwd is not None:
        return User(id)
    return None

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.get_role() not in roles:
                return login_manager.unauthorized()
            return f(*args, **kwargs)
        return wrapped
    return wrapper

@app.route('/hello_world')
def hello_world():
    return 'Hello World!'

@app.route('/control/admin')
@login_required
@requires_roles('admin')
def admin_cp():
    user = current_user
    username = user.get_id()
    admin = Admin(username)
    user_list = admin.show_all_users()
    course_data = admin.show_courses()
    return render_template('admin_cp.html', user=user, course_data = course_data, user_list = user_list)

@app.route('/control/admin/export_users')
@login_required
@requires_roles('admin')
def export_data():
    username = current_user.get_id()
    admin = Admin(username)
    user_list = admin.show_all_users()
    data = ''
    for tuple in user_list:
        data += tuple[0] + "," # id
        data += tuple[1] + "," # first name
        data += tuple[2] + "," # last name
        data += tuple[3] + "<br>" # account type
    return data

@app.route('/control/admin/add_user', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def admin_add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        account = request.form['account']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password.encode('utf-8')
        if len(username) > 0:
            create_user(username, password, account, first_name, last_name)
            return redirect(url_for('admin_cp'))
    return render_template('admin_add_user.html')

@app.route('/control/admin/add_course', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def admin_add_course():
    user = current_user
    username = user.get_id()
    admin = Admin(username)
    user_list = admin.show_all_users()
    user_ids = []
    for user_id in user_list:
        user_ids.append(user_id[0])

    course_list = admin.show_courses()
    course_ids = []
    for course in course_list:
        course_ids.append(course[0])

    if request.method == 'POST':
        course_id = request.form['course_id']
        credits = request.form['credits']
        course_name = request.form['course_name']
        id = request.form['id']
        if id in user_ids and course_id not in course_ids:
            admin.create_course(course_id,credits,course_name,id)
            return redirect(url_for('admin_cp'))
    return render_template('admin_add_course.html')

@app.route('/control/admin/remove_user_with_button/')
@login_required
@requires_roles('admin')
def remove_user_with_button():
    if request.method == 'GET':
        username = request.args.get('id')
        if username is not None:
            delete_user(username)
            return 'User ' + username + ' deleted.'
    return 'Error in delete request.'

@app.route('/control/admin/modify_instructor/', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def admin_modify_instructor():
    course_id = request.args.get('cid')
    user = current_user
    username = user.get_id()
    admin = Admin(username)
    user_list = admin.show_all_users()
    user_ids = []
    for user_id in user_list:
        user_ids.append(user_id[0])

    if request.method == 'POST':
        id = request.form['id']
        if len(id) > 0 and id in user_ids:
            admin.mod_instructor(id, course_id)
            return redirect(url_for('admin_cp'))
    return render_template('admin_modify_instructor.html', user=user, course_id=course_id)


# @app.route('/control/admin/remove_user/', methods=['GET', 'POST'])
# @login_required
# @requires_roles('admin')
# def admin_remove_user():
#     if request.method == 'POST':
#         username = request.form['username']
#         delete_user(username)
#         return redirect(url_for('admin_cp'))
#     return render_template('admin_remove_user.html')

@app.route('/control/student')
@login_required
@requires_roles('student')
def student_cp():
    user = current_user
    username = user.get_id()
    student = Student(username)
    course_data = student.show_courses()
    return render_template('student_cp.html', user=user, course_data=course_data)

@app.route('/control/student/view_course/')
@login_required
@requires_roles('student')
def view_course():
    # URL requested will look like /control/instructor_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    user = current_user
    username = user.get_id()
    student = Student(username)
    course_data = student.get_course_data(course_id)
    assignment_list = student.show_assignments(course_id)
    resource_list = student.show_resources(course_id)
    submission_list = student.show_submissions(course_id)

    if course_id is not None:
        return render_template('student_view_course.html', user=user, course_data=course_data,course_id=course_id, assignment_list=assignment_list,
                               resource_list=resource_list, submission_list=submission_list)
    return 'Error: No query string.'

@app.route('/control/student/submit_assignment/', methods=['GET', 'POST'])
@login_required
@requires_roles('student')
def submit_assignment():
    # URL requested will look like /control/instructor_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    user = current_user
    username = user.get_id()
    student = Student(username)
    course_data = student.get_course_data(course_id)
    assign_list = student.show_assignments(course_id)
    assign_ids = []
    for assign in assign_list:
        assign_ids.append(assign[0])

    if request.method == 'POST':
        assignID = request.form['assignID']
        filepath = request.form['filepath']
        assignID = int(assignID)
        
        if assignID in assign_ids:
            student.submit_assignment(assignID,filepath)
            return redirect(url_for('student_cp'))
        else:
            return redirect(url_for('student_cp'))
    return render_template('student_submit_assignment.html')

@app.route('/control/ta')
@login_required
@requires_roles('ta')
def ta_cp():
    user = current_user
    username = user.get_id()
    ta = TA(username)
    course_data = ta.show_courses()
    return render_template('ta_cp.html', user=user, course_data=course_data)

@app.route('/control/instructor_cp')
@login_required
@requires_roles('instructor')
def instructor_cp():
    user = current_user
    username = user.get_id()
    instructor = Instructor(username)
    course_data = instructor.show_courses() # Can use this to show course data for instructor
    #student_list = instructor.show_students('cid1')
    #assignment_list = instructor.show_assignments('cid1')
    #ta_list = instructor.show_tas('cid1')
    #resource_list = instructor.show_resources('cid1')
    # submission_list = instructor.show_submissions('cid1')
    return render_template('instructor_cp.html', user=user, course_data = course_data)

@app.route('/control/instructor_cp/modify_course/')
@login_required
@requires_roles('instructor')
def modify_course():
    # URL requested will look like /control/instructor_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    user = current_user
    username = user.get_id()
    instructor = Instructor(username)
    course_data = instructor.get_course_data(course_id)
    student_list = instructor.show_students(course_id)
    ta_list = instructor.show_tas(course_id)
    assignment_list = instructor.show_assignments(course_id)
    resource_list = instructor.show_resources(course_id)
    submission_list = instructor.show_submissions(course_id)

    if course_id is not None:
        return render_template('instr_view_course.html', user=user, course_id=course_id, course_data=course_data,
                               student_list=student_list, ta_list=ta_list, assignment_list=assignment_list,
                               resource_list=resource_list, submission_list=submission_list)
    return 'Error: No query string.'

@app.route('/control/ta_cp/modify_course/')
@login_required
@requires_roles('ta')
def ta_modify_course():
    # URL requested will look like /control/instructor_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    user = current_user
    username = user.get_id()
    ta = TA(username)
    course_data = ta.get_course_data(course_id)
    student_list = ta.show_students(course_id)
    assignment_list = ta.show_assignments(course_id)
    resource_list = ta.show_resources(course_id)
    submission_list = ta.show_submissions(course_id)

    if course_id is not None:
        return render_template('ta_view_course.html', user=user, course_id=course_id, course_data=course_data,
                               student_list=student_list, assignment_list=assignment_list,
                               resource_list=resource_list, submission_list=submission_list)
    return 'Error: No query string.'

@app.route('/control/instructor_cp/enroll_student/', methods=['GET', 'POST'])
@login_required
@requires_roles('instructor')
def enroll_student():
    # URL requested will look like /control/instructor_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    user = current_user
    username = user.get_id()

    user2 = current_user
    username2 = user2.get_id()
    admin = Admin(username2)

    instructor = Instructor(username)
    course_data = instructor.get_course_data(course_id)
    student_list = instructor.show_students(course_id)
    student_ids = []
    for student in student_list:
        student_ids.append(student[0])

    user_list = admin.show_all_users()
    user_ids = []
    for use in user_list:
        user_ids.append(use[0])

    if request.method == 'POST':
        studID = request.form['studID']
        if studID not in student_ids and len(studID) < 7 and studID in user_ids:
            instructor.enroll_student_in_course(studID, course_id)
            return redirect(url_for('instructor_cp'))
        else:
            return redirect(url_for('instructor_cp'))
    return render_template('instr_enroll_student.html')

@app.route('/control/instructor_cp/unenroll_student/')
@login_required
@requires_roles('instructor')
def unenroll_student():
    # URL requested will look like /control/instructor_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    student_id = request.args.get('id')
    user = current_user
    username = user.get_id()
    instructor = Instructor(username)
    course_data = instructor.get_course_data(course_id)
    student_list = instructor.show_students(course_id)
    student_ids = []
    for student in student_list:
        student_ids.append(student[0])

    if student_id in student_ids:
        instructor.unenroll_student_in_course(student_id, course_id)
        return redirect(url_for('instructor_cp'))
    else:
        return redirect(url_for('instructor_cp'))
    return render_template('instructor_cp.html', user=user, course_data = course_data)

@app.route('/control/instructor_cp/enroll_ta/', methods=['GET', 'POST'])
@login_required
@requires_roles('instructor')
def enroll_ta():
    # URL requested will look like /control/instructor_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    user = current_user
    username = user.get_id()
    instructor = Instructor(username)

    user2 = current_user
    username2 = user2.get_id()
    admin = Admin(username2)

    course_data = instructor.get_course_data(course_id)
    ta_list = instructor.show_tas(course_id)
    ta_ids = []
    for ta in ta_list:
        ta_ids.append(ta[0])

    user_list = admin.show_all_users()
    user_ids = []
    for use in user_list:
        user_ids.append(use[0])

    if request.method == 'POST':
        taID = request.form['taID']
        if taID not in ta_ids and len(taID) < 7 and taID in user_ids:
            instructor.enroll_ta_in_course(taID, course_id)
            return redirect(url_for('instructor_cp'))
        else:
            return redirect(url_for('instructor_cp'))
    return render_template('instr_enroll_ta.html')

@app.route('/control/instructor_cp/unenroll_ta/')
@login_required
@requires_roles('instructor')
def unenroll_ta():
    # URL requested will look like /control/instructor_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    ta_id = request.args.get('id')
    user = current_user
    username = user.get_id()
    instructor = Instructor(username)
    course_data = instructor.get_course_data(course_id)
    ta_list = instructor.show_tas(course_id)
    ta_ids = []
    for ta in ta_list:
        ta_ids.append(ta[0])

    if ta_id in ta_ids:
        instructor.unenroll_ta_in_course(ta_id, course_id)
        return redirect(url_for('instructor_cp'))
    else:
        return redirect(url_for('instructor_cp'))
    return render_template('instructor_cp.html', user=user, course_data = course_data)

@app.route('/control/instructor_cp/add_assignment/', methods=['GET', 'POST'])
@login_required
@requires_roles('instructor')
def add_assignment():
    # URL requested will look like /control/instructor_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    user = current_user
    username = user.get_id()
    instructor = Instructor(username)
    course_data = instructor.get_course_data(course_id)
    assign_list = instructor.show_assignments(course_id)
    assign_ids = []
    for assign in assign_list:
        assign_ids.append(assign[0])

    if request.method == 'POST':
        assignID = request.form['assignID']
        filepath = request.form['filepath']
        if assignID not in assign_ids:
            instructor.create_assignment(assignID,course_id,filepath)
            return redirect(url_for('instructor_cp'))
        else:
            return redirect(url_for('instructor_cp'))
    return render_template('instr_add_assignment.html')

@app.route('/control/instructor_cp/add_resource/', methods=['GET', 'POST'])
@login_required
@requires_roles('instructor')
def add_resource():
    # URL requested will look like /control/instructor_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    user = current_user
    username = user.get_id()
    instructor = Instructor(username)
    course_data = instructor.get_course_data(course_id)
    res_list = instructor.show_resources(course_id)
    res_ids = []
    for res in res_list:
        res_ids.append(res[0])

    if request.method == 'POST':
        resName = request.form['resName']
        filepath = request.form['filepath']
        if resName not in res_ids:
            instructor.create_resource(course_id,resName,filepath)
            return redirect(url_for('instructor_cp'))
        else:
            return redirect(url_for('instructor_cp'))
    return render_template('instr_add_resource.html')

@app.route('/control/ta_cp/add_resource/', methods=['GET', 'POST'])
@login_required
@requires_roles('ta')
def ta_add_resource():
    # URL requested will look like /control/instructor_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    user = current_user
    username = user.get_id()
    ta = TA(username)
    course_data = ta.get_course_data(course_id)
    res_list = ta.show_resources(course_id)
    res_ids = []
    for res in res_list:
        res_ids.append(res[0])

    if request.method == 'POST':
        resName = request.form['resName']
        filepath = request.form['filepath']
        if resName not in res_ids:
            ta.create_resource(course_id,resName,filepath)
            return redirect(url_for('ta_cp'))
        else:
            return redirect(url_for('ta_cp'))
    return render_template('ta_add_resource.html')

@app.route('/control/instructor_cp/edit_grade/', methods=['GET', 'POST'])
@login_required
@requires_roles('instructor')
def edit_grade():
    # URL requested will look like /control/instructor_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    id = request.args.get('id')
    assign_id = request.args.get('assign_id')
    file_path = request.args.get('file_path')
    user = current_user
    username = user.get_id()
    instructor = Instructor(username)

    if request.method == 'POST':
        grade = request.form['grade']
        if grade > 0:
            instructor.grade_submission(id,assign_id,file_path,grade,course_id)
            return redirect(url_for('instructor_cp'))
        else:
            return redirect(url_for('instructor_cp'))
    return render_template('instr_edit_grade.html')

@app.route('/control/ta_cp/edit_grade/', methods=['GET', 'POST'])
@login_required
@requires_roles('ta')
def ta_edit_grade():
    # URL requested will look like /control/ta_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    id = request.args.get('id')
    assign_id = request.args.get('assign_id')
    file_path = request.args.get('file_path')
    user = current_user
    username = user.get_id()
    ta = TA(username)

    if request.method == 'POST':
        grade = request.form['grade']
        if grade > 0:
            ta.grade_submission(id,assign_id,file_path,grade,course_id)
            return redirect(url_for('ta_cp'))
        else:
            return redirect(url_for('ta_cp'))
    return render_template('ta_edit_grade.html')

@app.route('/control/instructor_cp/remove_submission/')
@login_required
@requires_roles('instructor')
def remove_submission():
    # URL requested will look like /control/instructor_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    id = request.args.get('id')
    assign_id = request.args.get('assign_id')
    assign_id = int(assign_id)
    user = current_user
    username = user.get_id()
    instructor = Instructor(username)
    course_data = instructor.get_course_data(course_id)
    sub_list = instructor.show_submissions(course_id)
    sub_ids = []
    for sub in sub_list:
        sub_ids.append(sub[3])

    student_list = instructor.show_students(course_id)
    student_ids = []
    for student in student_list:
        student_ids.append(student[0])

    if sub_ids.__contains__(assign_id) and student_ids.__contains__(id):
        instructor.remove_submission(id,assign_id,course_id)
        return redirect(url_for('instructor_cp'))
    else:
        return redirect(url_for('instructor_cp'))
    return render_template('instructor_cp.html', user=user, course_data = course_data)

@app.route('/control/ta_cp/remove_submission/')
@login_required
@requires_roles('ta')
def ta_remove_submission():
    # URL requested will look like /control/ta_cp/modify_course/?cid=some-value
    course_id = request.args.get('cid')
    id = request.args.get('id')
    assign_id = request.args.get('assign_id')
    assign_id = int(assign_id)
    user = current_user
    username = user.get_id()
    ta = TA(username)
    course_data = ta.get_course_data(course_id)
    sub_list = ta.show_submissions(course_id)
    sub_ids = []
    for sub in sub_list:
        sub_ids.append(sub[3])

    student_list = ta.show_students(course_id)
    student_ids = []
    for student in student_list:
        student_ids.append(student[0])

    if sub_ids.__contains__(assign_id) and student_ids.__contains__(id):
        ta.remove_submission(id,assign_id,course_id)
        return redirect(url_for('ta_cp'))
    else:
        return redirect(url_for('ta_cp'))
    return render_template('ta_cp.html', user=user, course_data = course_data)

@app.route('/', methods=['GET', 'POST'])
def login():
    # Ensure the current user's not authenticated and redirect appropriately if so
    if current_user is not None and current_user.is_authenticated():
        role = current_user.get_role()
        if role == 'admin':
            return redirect(url_for('admin_cp'))
        elif role == 'instructor':
            return redirect(url_for('instructor_cp'))
        elif role == 'ta':
            return redirect(url_for('ta_cp'))
        elif role == 'student':
            return redirect(url_for('student_cp'))
        else:
            return "Everybody's special."

    # Validate credentials
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pwd = User.get(username)
        if hashed_pwd and check_login(username, password):
            user = User(username)
            login_user(user)
            if user.get_role() == 'admin':
                return redirect(url_for('admin_cp'))
            elif user.get_role() == 'student':
                return redirect(url_for('student_cp'))
            elif user.get_role() == 'ta':
                return redirect(url_for('ta_cp'))
            elif user.get_role() == 'instructor':
                return redirect(url_for('instructor_cp'))
            else:
                return redirect(url_for('hello_world'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('loggedout.html')

if __name__ == '__main__':
    app.run(debug=True)

