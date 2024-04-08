from flask import Blueprint,redirect,url_for,render_template,request,flash,session,abort,jsonify
from database import execute_query
from sendmail import send_email
from key import salt,salt2
import werkzeug.security as bcrypt
from ctokens import create_token,verify_token
from key import add_verify_details,update_verify_details

admin_bp = Blueprint('admin',__name__,url_prefix='/admin')

@admin_bp.route('/dashboard')   
def dashboard():
    if session.get('role') == 'Admin':
        return render_template('admin/dashboard.html')
    else:
        return redirect(url_for('auth.login'))

@admin_bp.route('/view_departments')
def view_departments():
    if session.get('role') == 'Admin':
        query = """
        SELECT d.department_id, d.department_name
        FROM departments d
        """
        departments_details = execute_query(query)
        return render_template('admin/view_departments.html', departments_details=departments_details)
    else:
        flash('Please Login to Continue!')
        return redirect(url_for('auth.login'))

@admin_bp.route('/view_courses')
def view_courses():
    if session.get('role') == 'Admin':
        query = """
        SELECT c.course_id, c.course_name, d.department_name, c.course_target, CONCAT(u1.name, ' (', u1.role, ')') AS added_by, CONCAT(u2.name, ' (', u2.role, ')') AS updated_by FROM courses c JOIN departments d ON c.department_id = d.department_id LEFT JOIN users u1 ON c.target_added_by = u1.user_id LEFT JOIN users u2 ON c.target_updated_by = u2.user_id
        """
        course_details = execute_query(query)
        return render_template('admin/view_courses.html', course_details=course_details)
    else:
        flash('Please Login to Continue!')
        return redirect(url_for('auth.login'))

@admin_bp.route('/add_departments', methods=['GET', 'POST'])
def add_departments():
    if session.get('role') == 'Admin':
        if request.method == 'POST':
            dept_name = request.form.get('dept_name').strip()

            if dept_name:
                existing_dept = execute_query("SELECT COUNT(*) as count FROM departments WHERE department_name = %s", (dept_name,),fetch_one=True)
                if existing_dept['count'] == 1:
                    flash('Department name already exists.')
                    return redirect(url_for('admin.add_departments'))
                execute_query("INSERT INTO departments (department_name) VALUES (%s)", (dept_name,), commit=True)
                
                flash('Department added successfully.')
                return redirect(url_for('admin.view_departments'))
            else:
                flash('Department name is required.')
                return redirect(url_for('admin.add_departments'))
        return render_template('admin/add_departments.html')
    else:
        flash('Please Login to Continue.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/add_courses', methods=['GET', 'POST'])
def add_courses():
    if session.get('role') == 'Admin':
        departments = execute_query("SELECT department_id, department_name FROM departments")
        if request.method == 'POST':
            course_name = request.form.get('course_name').strip()
            dept_id = request.form.get('dept_id',type=int)
            course_target = request.form.get('course_target','Null')
            start_date = request.form.get('start_date')
            if not course_name:
                flash('Course name is required.')
                return redirect(url_for('admin.add_courses'))

            if not dept_id:
                flash('Valid department is required.')
                return redirect(url_for('admin.add_courses'))

            existing_course = execute_query("SELECT COUNT(*) as count FROM courses WHERE course_name = %s AND department_id = %s", (course_name, dept_id),fetch_one=True)
            
            if existing_course['count'] == 1:
                flash('Course already exists in the selected department.')
                return redirect(url_for('admin.add_courses'))

            execute_query("INSERT INTO courses (course_name, department_id,course_target,target_added_by,start_date) VALUES (%s, %s,%s,%s,%s)", (course_name, dept_id,course_target,session.get('user_id'),start_date), commit=True)
            flash('Course added successfully.')
            return redirect(url_for('admin.view_courses'))
        
        return render_template('admin/add_courses.html', departments=departments)
    else:
        flash('Please Login to Continue.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/update_department/<int:dept_id>', methods=['GET', 'POST'])
def update_department(dept_id):
    if session.get('role') == 'Admin':
        dept_details = execute_query("SELECT department_id, department_name FROM departments WHERE department_id = %s", (dept_id,), fetch_one=True)
        if request.method == 'POST':
            dept_name = request.form.get('dept_name').strip()
            if not dept_name:
                flash('Department name is required.')
                return render_template('admin/update_department.html', dept_details=dept_details)
            existing_dept = execute_query("SELECT COUNT(*) as count FROM departments WHERE department_name = %s", (dept_name,),fetch_one=True)
            if existing_dept['count'] == 1:
                flash('Department name already exists.')
                return redirect(url_for('admin.add_departments'))

            # Update department name and incharge
            execute_query("UPDATE departments SET department_name = %s WHERE department_id = %s", (dept_name, dept_id), commit=True)

            flash('Department updated successfully.')
            return redirect(url_for('admin.view_departments'))
        
        return render_template('admin/update_department.html', dept_details=dept_details)
    else:
        flash('Please Login to Continue.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/update_course/<int:course_id>', methods=['GET', 'POST'])
def update_course(course_id):
    if session.get('role') == 'Admin' or session.get('role')=='Faculty':
        course_details = execute_query("SELECT c.course_id, c.course_name, d.department_name,d.department_id, c.course_target,c.start_date, CONCAT(u1.name, ' (', u1.role, ')') AS added_by, CONCAT(u2.name, ' (', u2.role, ')') AS updated_by FROM courses c JOIN departments d ON c.department_id = d.department_id LEFT JOIN users u1 ON c.target_added_by = u1.user_id LEFT JOIN users u2 ON c.target_updated_by = u2.user_id where course_id=%s", (course_id,), fetch_one=True)
        departments = execute_query("SELECT department_id, department_name FROM departments")

        if request.method == 'POST':
            course_name = request.form.get('course_name').strip()
            dept_id = request.form.get('dept_id',type=int)
            course_target = request.form.get('course_target','Null')
            start_date = request.form.get('start_date')
            print(request.form)
            if session.get('role')=='Faculty':
                dept_id = course_details['department_id']
            if not course_name:
                flash('Course name is required.')
                return render_template('admin/update_course.html', course_details=course_details, departments=departments)

            if not dept_id:
                flash('Valid department is required.')
                return render_template('admin/update_course.html', course_details=course_details, departments=departments)
            
            check_added_by = execute_query("select count(*) as count from courses where course_id=%s and target_added_by is null",(course_id,),fetch_one=True)['count']
            if check_added_by==1:
                # Update the course details
                execute_query("UPDATE courses SET course_name = %s, department_id = %s,course_target=%s,target_added_by=%s,start_date=%s WHERE course_id = %s", (course_name, dept_id,course_target,session.get('user_id'),start_date, course_id), commit=True)  
            else:
                # Update the course details
                execute_query("UPDATE courses SET course_name = %s, department_id = %s,course_target=%s,target_updated_by=%s,start_date=%s WHERE course_id = %s", (course_name, dept_id,course_target,session.get('user_id'),start_date, course_id), commit=True)
            flash('Course updated successfully.')
            if session.get('role')=='Faculty':
                return redirect(url_for("faculty.View_course_target"))
            return redirect(url_for('admin.view_courses'))
        
        return render_template('admin/update_course.html', course_details=course_details, departments=departments)
    else:
        flash('Please Login to Continue.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/view_faculty')
def view_faculty():
    if session.get('role') == 'Admin':
        query = """
        SELECT f.faculty_id, u.name, u.email, u.gender, u.mobileno, u.role, d.department_name, c.course_name,c.course_id
        FROM faculty f
        JOIN users u ON f.user_id = u.user_id
        LEFT JOIN departments d ON f.department_id = d.department_id
        LEFT JOIN courses c ON f.course_id = c.course_id;
        """
        faculty_details = execute_query(query)
        return render_template('admin/view_faculty.html', faculty_details=faculty_details)
    else:
        flash('Please Login to Continue!')
        return redirect(url_for('auth.login'))

@admin_bp.route('/view_student')
def view_student():
    if session.get('role') == 'Admin':
        query = """
        SELECT s.student_id, u.name, u.email, u.gender, u.mobileno, u.role, d.department_name, c.course_name,c.course_id
        FROM students s
        JOIN users u ON s.user_id = u.user_id
        LEFT JOIN departments d ON s.department_id = d.department_id
        LEFT JOIN courses c ON s.course_id = c.course_id;
        """
        student_details = execute_query(query)
        return render_template('admin/view_student.html', student_details=student_details)
    else:
        flash('Please Login to Continue!')
        return redirect(url_for('auth.login'))



@admin_bp.route('/dept_course/<int:dept_id>')
def get_courses_by_department(dept_id):
    if session.get('role') == 'Admin' or session.get('role')=='Faculty':
        courses = execute_query("SELECT course_id, course_name FROM courses WHERE department_id = %s", (dept_id,))
        return jsonify([{'course_id': course['course_id'], 'course_name': course['course_name']} for course in courses])
    else:
        return abort(403, 'Unauthorized access')
       
@admin_bp.route('/add_details', methods=['GET', 'POST'])
def add_details():
    if session.get('role') == 'Admin' or session.get('role')=='Faculty':
        departments = execute_query("SELECT department_id, department_name FROM departments")
        if request.method == 'POST':
            name = request.form.get('name', 'None').strip()
            email = request.form.get('email', "None").strip()
            gender = request.form.get('gender','None').strip()
            mobileno = request.form.get('mobile','None').strip()
            role = request.form.get('role', 'None').strip()
            department = request.form.get('department_id',type=int)
            course = request.form.get('course_id',type=int)
            hashed_password = bcrypt.generate_password_hash('asdf1234', method='pbkdf2:sha256', salt_length=16)

            if role=='Faculty' and session.get('role')=='Faculty':
                flash("You're not allowed to Add Faculty!")
                return redirect(url_for("faculty.dashboard"))

            email_count = execute_query("SELECT COUNT(*) as count FROM users WHERE email=%s", (email,), fetch_one=True)['count']
            if email_count== 1:
                flash('Email Already Exists!')
                return redirect(url_for('admin.add_details'))
                
            data = {'Name': name, 'Email': email, 'Password': hashed_password, 'Role': role,'Department_id': department, 'Course_id': course,'Mobileno':mobileno,'Gender':gender}

            
            token = create_token(data, salt=add_verify_details)
            verify_url = url_for('admin.add_verify', token=token, _external=True)
            subject = 'Activate Your Account'
            body = f"Dear {name},\n\nYour account has been created with the temporary password: asdf1234\n\nPlease activate your account and set your own password by clicking the following link:\n{verify_url}"
            send_email(receiver_email=email, subject=subject, body=body)

            flash(f"{data['Role']} added and verification email sent.")
            if session.get('role')=='Faculty':
                return redirect(url_for('faculty.dashboard'))
            return redirect(url_for(f"admin.view_{data['Role'].lower()}"))

        return render_template('admin/add_details.html', departments=departments)
    else:
        flash('Please Login to Continue.')
        return redirect(url_for('auth.login'))
    
@admin_bp.route('/add_verify/<token>', methods=['GET', 'POST'])
def add_verify(token):
    data = verify_token(token, salt=add_verify_details, expiration=86400)  # 24 hours for token expiration
    if data:
        user_exists = execute_query("SELECT COUNT(*) as count FROM users WHERE email = %s", (data['Email'],),fetch_one=True)['count']
        if user_exists ==1:
            flash('User Already Registered! Please Login.')
            return redirect(url_for('auth.login'))

        # Insert into users table
        execute_query("INSERT INTO users (name, email, gender, mobileno, password_hash, role) VALUES (%s, %s, %s, %s,%s,%s)", (data['Name'], data['Email'],data['Gender'],data['Mobileno'], data['Password'], data['Role']), commit=True)

        user_id = execute_query("SELECT user_id FROM users WHERE email=%s", (data['Email'],), fetch_one=True)['user_id']

        # Handle Department Incharge and Faculty specific actions
        if data['Role'] == 'Faculty':
            # Insert into faculty table
            execute_query("INSERT INTO faculty (user_id,department_id,course_id) VALUES (%s,%s,%s)", (user_id,data['Department_id'],data['Course_id']), commit=True)

        if data['Role'] == 'Student':
            execute_query("INSERT INTO students (user_id,department_id,course_id) VALUES (%s,%s,%s)", (user_id,data['Department_id'],data['Course_id']), commit=True)
            student_id = execute_query("Select student_id from students where user_id=%s",(user_id,),fetch_one=True)['student_id']
            execute_query("INSERT INTO course_enrollment (student_id,course_id) VALUES (%s,%s,%s)", (student_id,data['Course_id']), commit=True)

        flash(f"You've successfully registered as {data['Role']}")
        return redirect(url_for('auth.login'))
    else:
        flash('Verification link expired or invalid.')
        return redirect(url_for('admin.add_details'))

@admin_bp.route('/update_details/<int:update_id>/<role>', methods=['GET', 'POST'])
def update_details(update_id,role):
    if session.get('role') == 'Admin' or session.get('role') == 'Faculty':
        if role=="Faculty":
            if session.get('role')=='Faculty':
                flash("You're Not Allowed to change Faculty Details")
                return redirect(url_for('faculty.dashboard'))
            details = execute_query("SELECT f.faculty_id, u.name,u.user_id, u.email, u.gender, u.mobileno, u.role, d.department_name, c.course_name,c.course_id,f.department_id,f.course_id FROM faculty f JOIN users u ON f.user_id = u.user_id LEFT JOIN departments d ON f.department_id = d.department_id LEFT JOIN courses c ON f.course_id = c.course_id where faculty_id=%s", (update_id,), fetch_one=True)
        if role=="Student":
            details = execute_query("SELECT s.student_id, u.name,u.user_id, u.email, u.gender, u.mobileno, u.role, d.department_name, c.course_name,c.course_id,s.department_id,s.course_id FROM students s JOIN users u ON s.user_id = u.user_id LEFT JOIN departments d ON s.department_id = d.department_id LEFT JOIN courses c ON s.course_id = c.course_id where student_id=%s", (update_id,), fetch_one=True)
        departments = execute_query("SELECT department_id, department_name FROM departments")
        if request.method == 'POST':
            name = request.form.get('name').strip()
            email = request.form.get('email').strip()
            gender = request.form.get('gender','None').strip()
            mobileno = request.form.get('mobile','None').strip()
            role = request.form.get('role').strip()
            department_id = request.form.get('department_id', type=int)
            course_id = request.form.get('course_id',type=int)
            data = {'Name': name,'Email': email, 'Gender':gender, 'Mobileno':mobileno,'Role': role,'Department_id': department_id,'Course_id':course_id,'Existing_user_id': details['user_id']}

            if department_id==details['department_id'] and course_id!=details['course_id']:
                if data['Role']=='Faculty':
                    execute_query("UPDATE faculty set course_id=%s where department_id=%s and faculty_id=%s",(data['Course_id'],data['Department_id'],update_id),commit=True)
                elif data['Role']=='Student':
                    execute_query("UPDATE students set course_id=%s where department_id=%s and student_id=%s",(data['Course_id'],data['Department_id'],update_id),commit=True)

            elif department_id!=details['department_id'] and course_id==details['course_id']:
                if data['Role']=='Faculty':
                    execute_query("UPDATE faculty set department_id=%s where course_id=%s and faculty_id=%s",(data['Department_id'],data['Course_id'],update_id),commit=True)
                elif data['Role']=='Student':
                    execute_query("UPDATE students set department_id=%s where course_id=%s and student_id=%s",(data['Department_id'],data['Course_id'],update_id),commit=True)
            elif department_id!=details['department_id'] and course_id!=details['course_id']:
                if data['Role']=='Faculty':
                    execute_query("UPDATE faculty set department_id=%s, course_id=%s where faculty_id=%s",(data['Department_id'],data['Course_id'],update_id),commit=True)
                elif data['Role']=='Student':
                    execute_query("UPDATE students set department_id=%s, course_id=%s where student_id=%s",(data['Department_id'],data['Course_id'],update_id),commit=True)

            if email != details['email']:  # Check if email has changed
                # Ensure the new email doesn't already exist in the system
                email_count = execute_query("SELECT COUNT(*) as count FROM users WHERE email = %s AND user_id != %s", (email, details['user_id']),fetch_one=True)['count']# Send email to verify the email change
                data['Email'] = email
                if email_count == 1:
                    flash('Email Already Exists!')
                    return render_template('admin/update_details.html', details=details, departments=departments,update_id=update_id)
                token = create_token(data, salt=update_verify_details)
                verify_url = url_for('admin.update_verify', token=token, _external=True)
                subject = 'Confirm Your Email Update'
                body = f"Dear {name},\n\nPlease confirm your email update by clicking the following link:\n{verify_url}"
                send_email(receiver_email=email, subject=subject, body=body)

                flash(f'Email Sent to {role} new Email to update through the link Within 24 Hours.')
                if session.get('role')=='Faculty':
                    return redirect(url_for('faculty.dashboard'))
                return redirect(url_for(f'admin.view_{role.lower()}'))

            # Update details without changing email
            execute_query("UPDATE users SET name = %s,gender=%s,mobileno=%s, role = %s WHERE user_id = %s", (name,gender,mobileno, role,details['user_id']), commit=True)
            flash(f'{role} details updated successfully.')
            if session.get('role')=='Faculty':
                return redirect(url_for('faculty.dashboard'))
            return redirect(url_for(f'admin.view_{role.lower()}'))

        return render_template('admin/update_details.html', details=details, departments=departments,update_id=update_id)
    else:
        flash('Please Login to Continue.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/update_verify/<token>', methods=['GET', 'POST'])
def update_verify(token):
    data = verify_token(token, salt=update_verify_details, expiration=86400)  # 24 hours for token expiration
    if data:
        # Check if the new email is already registered
        email_count = execute_query("SELECT COUNT(*) as count FROM users WHERE email = %s AND user_id = %s", (data['Email'], data['Existing_user_id']),fetch_one=True)['count']
        if email_count ==1:
            flash('New Email Already Updated.')
            return redirect(url_for('auth.login'))

        # Update the user details in the database
        execute_query("UPDATE users SET email = %s WHERE user_id = %s",
                      (data['Email'], data['Existing_user_id']), commit=True)

        flash('Faculty email update verified successfully.')
        return redirect(url_for('auth.login'))
    else:
        flash('Verification link expired or invalid.')
        return redirect(url_for('auth.login'))

@admin_bp.route('/delete_department/<int:dept_id>', methods=['POST'])
def delete_department(dept_id):
    if session.get('role') == 'Admin':
        execute_query("DELETE FROM departments WHERE department_id = %s", (dept_id,), commit=True)
        flash("Department deleted successfully.")
        return redirect(url_for('admin.view_departments'))
    else:
        flash("Please login to continue.")
        return redirect(url_for('auth.login'))

@admin_bp.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    if session.get('role') == 'Admin':
        execute_query("DELETE FROM courses WHERE course_id = %s", (course_id,), commit=True)
        flash("Course deleted successfully.")
        return redirect(url_for('admin.view_courses'))
    else:
        flash("Please login to continue.")
        return redirect(url_for('auth.login'))

@admin_bp.route('/delete_details/<int:delete_id>/<role>', methods=['POST'])
def delete_details(delete_id,role):
    if session.get('role') == 'Admin':
        if role=='Faculty':   
            user_id = execute_query("Select user_id FROM faculty WHERE faculty_id = %s", (delete_id,), fetch_one=True)['user_id']
        if role=='Student':   
            user_id = execute_query("Select user_id FROM students WHERE student_id = %s", (delete_id,), fetch_one=True)['user_id']
        execute_query("DELETE FROM users WHERE user_id = %s AND role IN ('Faculty', 'Student')", (user_id,), commit=True)
        flash(f"{role} deleted successfully.")
        return redirect(url_for(f'admin.view_{role.lower()}'))
    else:
        flash("Please login to continue.")
        return redirect(url_for('auth.login'))


@admin_bp.route('/logout')
def logout():
    if session.get('role')=='Admin':
        session.pop('role')
        session.pop('user_id')
        flash('logout Success!')
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))

