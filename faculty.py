from flask import Blueprint, render_template, session, redirect, url_for, flash,request
from database import execute_query
from datetime import datetime
faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')

@faculty_bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'Faculty':
        flash('Access denied. Please log in as a Faculty member.')
        return redirect(url_for('auth.login'))
    
    if session.get('user_id'):
        faculty_user_id = session.get('user_id')
        query = "SELECT f.faculty_id, u.name, u.email, u.gender, u.mobileno, u.role, d.department_name,d.department_id, c.course_name, c.course_id,c.course_target FROM faculty f JOIN users u ON f.user_id = u.user_id LEFT JOIN departments d ON f.department_id = d.department_id LEFT JOIN courses c ON f.course_id = c.course_id WHERE f.user_id=%s"
        faculty_details = execute_query(query, (faculty_user_id,), fetch_one=True)
        session['faculty_details'] = faculty_details
        # print(session.get('faculty_details')['faculty_id'])
        # Pass course_details to the template
        return render_template('faculty/dashboard.html', faculty_details=faculty_details)

    # If user_id is not set in session or any other issue
    flash('An error occurred while loading the dashboard.')
    return redirect(url_for('faculty.dashboard'))  # Redirect to the homepage or appropriate route


@faculty_bp.route('/view_course_target')
def View_course_target():
    if session.get('role') != 'Faculty':
        flash('Access denied. Please log in as a Faculty member.')
        return redirect(url_for('auth.login'))
    course_details = execute_query("SELECT f.faculty_id, u.name, u.email, u.gender, u.mobileno, u.role, d.department_name, c.course_name, c.course_id,c.course_target FROM faculty f JOIN users u ON f.user_id = u.user_id LEFT JOIN departments d ON f.department_id = d.department_id LEFT JOIN courses c ON f.course_id = c.course_id")
    return render_template('faculty/View_course_target.html',course_details=course_details)

@faculty_bp.route('/view_students')
def view_students():
    if session.get('role') != 'Faculty':
        flash('Access denied. Please log in as a Faculty member.')
        return redirect(url_for('auth.login'))
    student_details = execute_query("SELECT s.student_id, u.name AS student_name, u.email AS student_email, u.gender AS student_gender, u.mobileno AS student_mobile, d.department_name, c.course_name FROM students s JOIN users u ON s.user_id = u.user_id JOIN departments d ON s.department_id = d.department_id JOIN courses c ON s.course_id = c.course_id JOIN faculty f ON f.department_id = d.department_id AND f.course_id = c.course_id WHERE f.faculty_id =%s",(session.get('faculty_details')['faculty_id'],))
    return render_template('faculty/view_students.html',student_details=student_details)


@faculty_bp.route('/view_student_attendance')
def view_student_attendance():
    if session.get('role') != 'Faculty':
        flash('Access denied. Please log in as a Faculty member.')
        return redirect(url_for('auth.login'))

    faculty_id = session.get('faculty_details')['faculty_id']

    # Query to get student attendance details
    query = """
    SELECT s.student_id, u.name AS student_name, c.course_name,
           SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END) AS days_present,
           SUM(CASE WHEN ar.status = 'Absent' THEN 1 ELSE 0 END) AS days_absent,
           COUNT(ar.record_id) AS total_days,
           (SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END) / COUNT(ar.record_id)) * 100 AS attendance_percentage
    FROM students s
    JOIN users u ON s.user_id = u.user_id
    JOIN courses c ON s.course_id = c.course_id
    LEFT JOIN attendance_records ar ON s.student_id = ar.student_id
    WHERE EXISTS (
        SELECT 1 FROM faculty f
        WHERE f.faculty_id = %s AND f.department_id = s.department_id AND f.course_id = s.course_id
    )
    GROUP BY s.student_id, u.name, c.course_name
    """

    student_attendance = execute_query(query, (faculty_id,))

    return render_template('faculty/view_student_attendance.html', student_attendance=student_attendance)


@faculty_bp.route('/set_timetable', methods=['GET', 'POST'])
def set_timetable():
    if 'role' not in session or session['role'] != 'Faculty':
        flash('Access denied. Please log in as a Faculty member.')
        return redirect(url_for('auth.login'))

    faculty_details = session.get('faculty_details')
    if not faculty_details:
        flash('Faculty details are missing. Please log in again.')
        return redirect(url_for('auth.login'))

    faculty_id = faculty_details.get('faculty_id')
    course_id = faculty_details.get('course_id')

    if request.method == 'POST':
        start_time = request.form.get('start_time')  # Assuming this is in 12-hour format, e.g., "02:30 PM"
        end_time = request.form.get('end_time')     # Same as above, e.g., "03:30 PM"
        lock_duration = request.form.get('lock_duration')  # This should be in minutes
        existing_entry = execute_query(
            "SELECT timetable_id FROM timetable WHERE faculty_id=%s AND course_id=%s",
            (faculty_id, course_id), fetch_one=True)

        if existing_entry:
            timetable_id = existing_entry.get('timetable_id')
            update_query = """
            UPDATE timetable SET start_time=%s, end_time=%s, lock_duration=%s
            WHERE timetable_id=%s
            """
            execute_query(update_query, (start_time, end_time, lock_duration, timetable_id), commit=True)
            flash('Timetable updated successfully.')
        else:
            insert_query = """
            INSERT INTO timetable (faculty_id, course_id, start_time, end_time, lock_duration)
            VALUES (%s, %s, %s, %s, %s)
            """
            execute_query(insert_query, (faculty_id, course_id, start_time, end_time, lock_duration), commit=True)
            flash('Timetable set successfully.')

        return redirect(url_for('faculty.set_timetable'))

    existing_timetable = execute_query("SELECT DATE_FORMAT(start_time,'%l:%i %p') as start_time , DATE_FORMAT(end_time,'%l:%i %p') as end_time, lock_duration FROM timetable WHERE faculty_id=%s AND course_id=%s",(faculty_id, course_id), fetch_one=True)

    # No need to convert the time here, as it's already in 12-hour format
    return render_template('faculty/set_timetable.html', timetable_details=existing_timetable)

@faculty_bp.route('/logout')
def logout():
    if session.get('role')=='Faculty':
        session.pop('role')
        session.pop('user_id')
        session.clear()
        flash('logout Success!')
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))
