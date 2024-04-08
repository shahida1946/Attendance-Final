from flask import Blueprint,redirect,url_for,render_template,request,flash,session,abort,jsonify
from database import execute_query
from sendmail import send_email
from key import salt,salt2
from datetime import datetime,timedelta

student_bp = Blueprint('student',__name__,url_prefix='/student')


@student_bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'Student':
        flash('Access denied. Please log in as a Student.')
        return redirect(url_for('auth.login'))

    student_user_id = session.get('user_id')
    print(session.get('user_id'))
    query = """
    SELECT s.student_id, u.name, u.email, d.department_name, c.course_name, c.course_id
    FROM students s
    JOIN users u ON s.user_id = u.user_id
    JOIN courses c ON s.course_id = c.course_id
    JOIN departments d ON s.department_id = d.department_id
    WHERE s.user_id = %s
    """
    student_details = execute_query(query, (student_user_id,),fetch_one=True)
    session['student_details'] = student_details
    return render_template('student/dashboard.html', student_details=student_details)

@student_bp.route('/enroll_course', methods=['GET', 'POST'])
def enroll_course():
    if session.get('role') != 'Student':
        flash('Access denied. Please log in as a Student.')
        return redirect(url_for('auth.login'))

    student_id = session.get('student_details')['student_id']

    if request.method == 'POST':
        course_id = request.form.get('course_id')
        if course_id:
            # Enroll the student in the selected course
            enrollment_query = """
            INSERT INTO course_enrollment (student_id, course_id)
            VALUES (%s, %s)
            """
            execute_query(enrollment_query, (student_id, course_id), commit=True)
            flash('Enrollment successful.')
            return redirect(url_for('student.enroll_course'))

    # Fetch courses available for enrollment
    query = """
    SELECT course_id, course_name
    FROM courses
    WHERE department_id = (
        SELECT department_id
        FROM students
        WHERE student_id = %s
    )
    AND course_id NOT IN (
        SELECT course_id
        FROM course_enrollment
        WHERE student_id = %s
    )
    """
    available_courses = execute_query(query, (student_id, student_id))
    return render_template('student/enroll_course.html', available_courses=available_courses)


@student_bp.route('/view_enrolled_courses')
def view_enrolled_courses():
    if session.get('role') != 'Student':
        flash('Access denied. Please log in as a Student.')
        return redirect(url_for('auth.login'))
    print(session.get('student_details'))
    student_id = session.get('student_details')['student_id']
    query = "SELECT ce.student_id, c.course_name,c.course_id,c.course_target, d.department_name, IFNULL(CONCAT(u.name, ' (Faculty)'), 'N/A') AS faculty_name,u.email as faculty_email, c.course_target FROM course_enrollment ce JOIN courses c ON ce.course_id = c.course_id JOIN departments d ON c.department_id = d.department_id LEFT JOIN faculty f ON ce.course_id = f.course_id LEFT JOIN users u ON f.user_id = u.user_id WHERE ce.student_id = %s"
    enrolled_courses = execute_query(query, (student_id,))
    print(enrolled_courses)
    return render_template('student/view_enrolled_courses.html', enrolled_courses=enrolled_courses)




@student_bp.route('/check_in/<int:course_id>', methods=['POST'])
def check_in(course_id):
    if session.get('role') != 'Student':
        flash('Access denied. Please log in as a Student.')
        return redirect(url_for('auth.login'))

    student_id = session.get('student_details')['student_id']
    current_date = datetime.now().date()
    # current_date = current_date + timedelta(days=1)
    current_time = datetime.now().time()

    # Check if the student already checked in for the course today
    check_already_checked_in = """
    SELECT * FROM attendance_records
    WHERE student_id = %s AND course_id = %s AND date = %s
    """
    already_checked_in = execute_query(check_already_checked_in, (student_id, course_id, current_date))

    if already_checked_in:
        flash('You have already checked in for this course today.')
        return redirect(url_for('student.view_attendance', course_id=course_id))

    # Continue with check-in process
    timetable_query = """
    SELECT start_time, end_time,lock_duration FROM timetable
    WHERE course_id = %s
    """
    timetable = execute_query(timetable_query, (course_id,), fetch_one=True)
    # Convert timedelta to time
    start_time = (datetime.min + timetable['start_time']).time() if isinstance(timetable['start_time'], timedelta) else timetable['start_time']
    current_time = (datetime.min + current_time).time() if isinstance(current_time, timedelta) else current_time
    end_time = (datetime.min + timetable['end_time']).time() if isinstance(timetable['end_time'], timedelta) else timetable['end_time']

    # Convert time objects to datetime objects for easy subtraction
    current_datetime = datetime.combine(datetime.min, current_time)
    start_datetime = datetime.combine(datetime.min, start_time)

    # Calculate the time difference
    time_difference = start_datetime - current_datetime

    # Calculate the absolute time difference
    absolute_time_difference = abs(time_difference)

    # Convert the absolute time difference to minutes
    absolute_time_difference_in_minutes = int(absolute_time_difference.total_seconds() / 60)

    # print(absolute_time_difference_in_minutes)
    if timetable and start_time <= current_time <= end_time:
        if absolute_time_difference_in_minutes > timetable['lock_duration']:
            attendance_query = """
            INSERT INTO attendance_records (student_id, course_id, date, check_in_time, status)
            VALUES (%s, %s, %s, %s, 'Absent')
            """
            execute_query(attendance_query, (student_id, course_id, current_date, current_time), commit=True)
            flash("Attendance Time Limit Exceeded.")
            return redirect(url_for('student.view_attendance', course_id=course_id))
        attendance_query = """
        INSERT INTO attendance_records (student_id, course_id, date, check_in_time, status)
        VALUES (%s, %s, %s, %s, 'Present')
        """
        execute_query(attendance_query, (student_id, course_id, current_date, current_time), commit=True)
        flash('Checked in successfully.')
    else:
        flash('Not within the allowed check-in time frame.')

    return redirect(url_for('student.view_attendance', course_id=course_id))


@student_bp.route('/check_out/<int:course_id>', methods=['POST'])
def check_out(course_id):
    if session.get('role') != 'Student':
        flash('Access denied. Please log in as a Student.')
        return redirect(url_for('auth.login'))

    student_id = session.get('student_details')['student_id']
    current_date = datetime.now().date()
    # current_date = current_date + timedelta(days=1)
    current_time = datetime.now().time()

    # Fetch the timetable to get the allowed check-out time window for the course
    timetable_query = """
    SELECT start_time, end_time
    FROM timetable
    WHERE course_id = %s
    """
    timetable = execute_query(timetable_query, (course_id,), fetch_one=True)
    
    start_time = (datetime.min + timetable['start_time']).time() if isinstance(timetable['start_time'], timedelta) else timetable['start_time']

    # Check if there is a timetable entry and if it is the correct time to check out
    if not timetable or current_time <= start_time:
        flash('It is too early to check out.')
        return redirect(url_for('student.view_attendance', course_id=course_id))

    # Fetch the existing attendance record for today
    attendance_record_query = """
    SELECT check_in_time, check_out_time FROM attendance_records
    WHERE student_id = %s AND course_id = %s AND date = %s
    """
    attendance_record = execute_query(attendance_record_query, (student_id, course_id, current_date), fetch_one=True)

    if not attendance_record or not attendance_record['check_in_time']:
        flash('You must check in before checking out.')
        return redirect(url_for('student.view_attendance', course_id=course_id))

    # If already checked out, show a message
    if attendance_record['check_out_time']:
        flash('You have already checked out for this course today.')
        return redirect(url_for('student.view_attendance', course_id=course_id))
    
    end_time = (datetime.min + timetable['end_time']).time() if isinstance(timetable['end_time'], timedelta) else timetable['end_time']

    # Check if it's after the course end time for check out
    if current_time < end_time:
        flash('It is not yet time to check out.')
        return redirect(url_for('student.view_attendance', course_id=course_id))

    # Update check-out time
    checkout_query = """
    UPDATE attendance_records
    SET check_out_time = %s
    WHERE student_id = %s AND course_id = %s AND date = %s
    """
    execute_query(checkout_query, (current_time, student_id, course_id, current_date), commit=True)
    flash('Checked out successfully.')

    return redirect(url_for('student.view_attendance', course_id=course_id))


@student_bp.route('/view_attendance/<int:course_id>')
def view_attendance(course_id):
    if session.get('role') != 'Student':
        flash('Access denied. Please log in as a Student.')
        return redirect(url_for('auth.login'))

    student_id = session.get('student_details')['student_id']

    # Fetch course details
    course_query = """
    SELECT c.course_id,c.course_name, c.course_target, c.start_date, u.name as faculty_name
    FROM courses c
    JOIN faculty f ON c.course_id = f.course_id
    JOIN users u ON f.user_id = u.user_id
    WHERE c.course_id = %s
    """
    course_details = execute_query(course_query, (course_id,), fetch_one=True)

    start_date = course_details['start_date']
    target_days = course_details['course_target']
    end_date = start_date + timedelta(days=target_days)
    current_date = datetime.now().date()
    # current_date = current_date + timedelta(days=2)
    attendance_records = []

    for single_date in (start_date + timedelta(days=n) for n in range(target_days)):
        if single_date > current_date:
            # Future dates should not be processed
            attendance_records.append({'date': single_date, 'status': 'Future'})
            continue

        attendance_query = """
        SELECT date, check_in_time, check_out_time, status
        FROM attendance_records
        WHERE student_id = %s AND course_id = %s AND date = %s
        """
        attendance = execute_query(attendance_query, (student_id, course_id, single_date), fetch_one=True)

        if not attendance and single_date < current_date:
            # If no record exists for a past day, mark it as absent
            insert_absent_query = """
            INSERT INTO attendance_records (student_id, course_id, date, status)
            VALUES (%s, %s, %s, 'Absent')
            """
            execute_query(insert_absent_query, (student_id, course_id, single_date), commit=True)
            attendance = {'date': single_date, 'status': 'Absent'}

        attendance_records.append(attendance or {'date': single_date, 'status': 'Future'})

    return render_template('student/view_full_attendance.html', 
                           course_details=course_details, 
                           attendance_records=attendance_records,current_date=current_date)


@student_bp.route('/view_attendance_percentage')
def view_attendance_percentage():
    if session.get('role') != 'Student':
        flash('Access denied. Please log in as a Student.')
        return redirect(url_for('auth.login'))

    student_id = session.get('student_details')['student_id']

    # Query to get the attendance details along with the total number of classes from the course_target
    query = """
    SELECT ce.course_id, c.course_name,
           SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END) AS days_attended,
           c.course_target AS total_days,
           (SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END) / c.course_target) * 100 AS attendance_percentage
    FROM course_enrollment ce
    INNER JOIN courses c ON ce.course_id = c.course_id
    LEFT JOIN attendance_records ar ON ce.course_id = ar.course_id AND ar.student_id = %s
    WHERE ce.student_id = %s
    GROUP BY ce.course_id, c.course_name, c.course_target
    """
    attendance_details = execute_query(query, (student_id, student_id))

    return render_template('student/view_attendance_percentage.html', attendance_details=attendance_details)




@student_bp.route('/logout')
def logout():
    if session.get('role')=='Student':
        session.pop('role')
        session.pop('user_id')
        session.clear()
        flash('logout Success!')
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))
