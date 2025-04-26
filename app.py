from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
import os
import MySQLdb
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from controllers.auth_controller import AuthController
from controllers.exit_controller import ExitController
from controllers.student_controller import StudentController
from controllers.schedule_controller import ScheduleController
from controllers.admin_controller import AdminController
from models.admin import Admin
from models.database import Database
from models.strand import Strand
from models.section import Section
from models.subject import Subject
from models.teacher import Teacher
from models.class_schedule import ClassSchedule
from models.student import Student
from models.exit_log import ExitLog
from utils.rfid_reader import RFIDReader
from config import DATABASE_CONFIG, APP_CONFIG, RFID_CONFIG
from config.teams_webhook import TEAMS_WEBHOOK_URL, TEAMS_WEBHOOK_ENABLED
import logging
import time

# Load environment variables from .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Environment variables loaded from .env file")
except ImportError:
    print("python-dotenv not installed, using environment variables from the system")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', APP_CONFIG['secret_key'])
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), APP_CONFIG['upload_folder'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Set up logging
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

# MySQL Configuration - Using values from config.py
app.config['MYSQL_HOST'] = DATABASE_CONFIG['host']
app.config['MYSQL_USER'] = DATABASE_CONFIG['user']
app.config['MYSQL_PASSWORD'] = DATABASE_CONFIG['password']
app.config['MYSQL_DB'] = DATABASE_CONFIG['database']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize Database
Database.initialize()

# Set up CORS and SocketIO
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

rfid_reader = RFIDReader()

# Helper functions
def formatProfilePicture(profile_path):
    if not profile_path:
        return '/static/img/default-profile.png'
    
    if profile_path.startswith('/static/'):
        return profile_path
    
    # If it's just a filename, prepend the path
    if not profile_path.startswith('/'):
        return f'/static/uploads/students/{profile_path}'
    
    return profile_path

@login_manager.user_loader
def load_user(user_id):
    try:
        return Admin.get_by_id(int(user_id))
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

# Auth routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('auth/login.html')  # Directly render login page instead of redirecting

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        # Get recent exit logs using our helper function
        exit_logs = get_formatted_exit_logs()
        
        # Get count of total students
        total_students = Database().fetch_one("SELECT COUNT(*) as count FROM students")['count']
        
        # Get count of total sections
        total_sections = Database().fetch_one("SELECT COUNT(*) as count FROM sections")['count']
        
        return render_template('admin/dashboard.html', exit_logs=exit_logs, total_students=total_students, total_sections=total_sections)
    except Exception as e:
        app.logger.error(f"Error in dashboard route: {e}")
        flash('An error occurred while loading the dashboard.', 'danger')
        return render_template('admin/dashboard.html', exit_logs=[], total_students=0, total_sections=0)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.get_by_username(username)
        if admin and admin.verify_password(password):
            login_user(admin)
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))
    
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/setup-admin', methods=['GET', 'POST'])
def setup_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        middle_initial = request.form.get('middle_initial')
        
        if username and password and first_name and last_name:
            try:
                admin_id = AdminController.create_admin(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    middle_initial=middle_initial
                )
                if admin_id:
                    flash('Admin account created successfully!', 'success')
                    return redirect(url_for('login'))
            except Exception as e:
                print(f"Error creating admin: {str(e)}")
                flash('Failed to create admin account.', 'danger')
        else:
            flash('All fields are required.', 'warning')
    
    return render_template('auth/setup_admin.html')

# Settings routes
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    admin = AuthController.get_current_admin()
    if not admin:
        return redirect(url_for('logout'))
    
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
        elif not admin.verify_password(current_password):
            flash('Current password is incorrect', 'error')
        else:
            success = AdminController.change_password(admin.id, current_password, new_password)
            if success:
                flash('Password changed successfully', 'success')
            else:
                flash('Failed to change password', 'error')
    
    return render_template('admin/settings.html', admin=admin)

@app.route('/clear-logs', methods=['POST'])
@login_required
def clear_logs():
    # Verify user is an admin
    admin = AuthController.get_current_admin()
    if not admin:
        flash('Unauthorized access', 'error')
        return redirect(url_for('login'))
    
    try:
        # Use the ExitLog model to clear all logs
        success = ExitLog.clear_all_logs()
        
        if success:
            # Log the action
            app.logger.info(f"All exit logs cleared by admin {admin.username}")
            flash('All exit logs have been successfully cleared', 'success')
        else:
            flash('Failed to clear exit logs', 'error')
    except Exception as e:
        app.logger.error(f"Error clearing exit logs: {str(e)}")
        flash(f'Error clearing exit logs: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/schedules')
@login_required
def schedules():
    grade_levels = ['Grade 11', 'Grade 12']
    strands = Strand.get_all()
    sections = Section.get_all()
    
    return render_template('admin/schedules.html',
                         grade_levels=grade_levels,
                         strands=strands,
                         sections=sections)

@app.route('/students')
@login_required
def students():
    try:
        # Query to get students with their section information
        query = """
        SELECT s.student_id, s.id_number, s.first_name, s.middle_initial, s.last_name, 
               s.grade_level, s.rfid_uid, s.profile_picture,
               sec.section_name, str.strand_code, str.strand_id
        FROM students s
        LEFT JOIN sections sec ON s.section_id = sec.section_id
        LEFT JOIN strands str ON sec.strand_id = str.strand_id
        ORDER BY s.last_name, s.first_name
        """
        students_data = Database().fetch_all(query)
        
        # Get sections for dropdown
        sections = Section.get_all()
        
        # Get strands for dropdown
        strands = Strand.get_all()
        
        return render_template('admin/students.html', 
                              students=students_data,
                              sections=sections,
                              strands=strands)
    except Exception as e:
        print(f"Error loading students page: {str(e)}")
        flash('An error occurred while loading students data.', 'danger')
        return render_template('admin/students.html', 
                              students=[], 
                              sections=[], 
                              strands=[])

@app.route('/api/students')
@login_required
def get_all_students():
    try:
        # Get filter parameters from the query string
        grade_level = request.args.get('grade_level')
        strand_id = request.args.get('strand_id')
        section_id = request.args.get('section_id')
        
        app.logger.info(f"Getting students with filters - grade_level: {grade_level}, strand_id: {strand_id}, section_id: {section_id}")
        
        # Base query with joins
        query = """
        SELECT s.student_id, s.id_number, s.first_name, s.middle_initial, s.last_name, 
               s.grade_level, s.rfid_uid, 
               CASE 
                   WHEN s.profile_picture IS NULL OR s.profile_picture = ''
                   THEN '/static/img/default-profile.png'
                   ELSE CONCAT('/static/uploads/students/', s.profile_picture)
               END as profile_picture,
               sec.section_name, sec.section_id, str.strand_code, str.strand_id
        FROM students s
        LEFT JOIN sections sec ON s.section_id = sec.section_id
        LEFT JOIN strands str ON sec.strand_id = str.strand_id
        """
        
        # Add WHERE clauses based on filter parameters
        where_clauses = []
        params = []
        
        # If section_id is provided, only filter by section_id to show all students 
        # from that section regardless of grade level
        if section_id and section_id.strip():
            where_clauses.append("s.section_id = %s")
            params.append(section_id)
        else:
            # Otherwise apply the other filters
            if grade_level and grade_level.strip():
                where_clauses.append("s.grade_level = %s")
                params.append(grade_level)
            
            if strand_id and strand_id.strip():
                where_clauses.append("str.strand_id = %s")
                params.append(strand_id)
        
        # Add WHERE clause to the query if any filters were applied
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
            
        # Add ORDER BY clause
        query += " ORDER BY s.first_name, s.last_name"
        
        app.logger.info(f"Student query: {query} with params: {params}")
        students_data = Database().fetch_all(query, tuple(params))
        
        # Format full_name for each student
        for student in students_data:
            middle_part = f" {student['middle_initial']}. " if student['middle_initial'] else " "
            student['full_name'] = f"{student['first_name']}{middle_part}{student['last_name']}"
        
        app.logger.info(f"Retrieved {len(students_data)} students")
        return jsonify({'status': 'success', 'students': students_data})
    except Exception as e:
        app.logger.error(f"Error getting students: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/students/<int:student_id>')
@login_required
def get_student_by_id(student_id):
    try:
        query = """
        SELECT s.student_id, s.id_number, s.first_name, s.middle_initial, s.last_name, 
               s.grade_level, s.rfid_uid, s.profile_picture, s.section_id, sec.strand_id,
               CASE 
                   WHEN s.profile_picture IS NULL OR s.profile_picture = ''
                   THEN '/static/img/default-profile.png'
                   ELSE CONCAT('/static/uploads/students/', s.profile_picture)
               END as formatted_profile_picture,
               sec.section_name, str.strand_code
        FROM students s
        LEFT JOIN sections sec ON s.section_id = sec.section_id
        LEFT JOIN strands str ON sec.strand_id = str.strand_id
        WHERE s.student_id = %s
        """
        student = Database().fetch_one(query, (student_id,))
        
        if not student:
            return jsonify({'status': 'error', 'message': 'Student not found'}), 404
        
        return jsonify({'status': 'success', 'student': student})
    except Exception as e:
        print(f"Error getting student: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/students/create', methods=['POST'])
@login_required
def create_student():
    try:
        # Get form data
        id_number = request.form.get('id_number').strip().upper()
        first_name = request.form.get('first_name').strip().upper()
        middle_initial = request.form.get('middle_initial', '').strip().upper()
        last_name = request.form.get('last_name').strip().upper()
        grade_level = request.form.get('grade_level')
        section_id = request.form.get('section_id') or None
        strand_id = request.form.get('strand_id') or None
        rfid_uid = request.form.get('rfid_uid', '').strip() or None
        
        # If section_id is provided but strand_id is not, get the strand_id from the section
        if section_id and not strand_id:
            section_query = "SELECT strand_id FROM sections WHERE section_id = %s"
            section_result = Database().fetch_one(section_query, (section_id,))
            if section_result and 'strand_id' in section_result:
                strand_id = section_result['strand_id']
        
        # Make sure strand_id is not None if a section is selected
        if section_id and not strand_id:
            return jsonify({'status': 'error', 'message': 'Strand ID is required when a section is selected'}), 400
                
        # Get the profile picture file
        profile_picture = None
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename:
                # Secure filename and save
                filename = secure_filename(f"{id_number}_{int(datetime.now().timestamp())}.jpg")
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'students', filename)
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                file.save(file_path)
                profile_picture = filename
        
        # Print values for debugging
        print(f"Creating student with strand_id: {strand_id}, section_id: {section_id}")
        
        # Create student object and save
        student_data = {
            'id_number': id_number,
            'first_name': first_name,
            'middle_initial': middle_initial,
            'last_name': last_name,
            'grade_level': grade_level,
            'section_id': section_id,
            'strand_id': strand_id,
            'profile_picture': profile_picture
        }
        
        student_id = StudentController.create_student(student_data, rfid_uid)
        
        if student_id:
            return jsonify({'status': 'success', 'student_id': student_id})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to create student'}), 500
            
    except Exception as e:
        print(f"Error creating student: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/students/<int:student_id>/update', methods=['POST'])
@login_required
def update_student(student_id):
    try:
        # Check if student exists
        student = Student.get_by_id(student_id)
        if not student:
            return jsonify({'status': 'error', 'message': 'Student not found'}), 404
        
        # Get form data
        id_number = request.form.get('id_number')
        first_name = request.form.get('first_name')
        middle_initial = request.form.get('middle_initial')
        last_name = request.form.get('last_name')
        grade_level = request.form.get('grade_level')
        section_id = request.form.get('section_id') or None
        rfid_uid = request.form.get('rfid_uid') or None
        
        # Get the profile picture file
        profile_picture = student.profile_picture
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename:
                # Delete old profile picture if it exists
                if student.profile_picture:
                    old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'students', student.profile_picture)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                # Secure filename and save
                filename = secure_filename(f"{id_number}_{int(datetime.now().timestamp())}.jpg")
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'students', filename)
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                file.save(file_path)
                profile_picture = filename
        
        # Update student object
        student_data = {
            'id_number': id_number,
            'first_name': first_name,
            'middle_initial': middle_initial,
            'last_name': last_name,
            'grade_level': grade_level,
            'section_id': section_id,
            'profile_picture': profile_picture
        }
        
        success = StudentController.update_student(student_id, student_data, rfid_uid)
        
        if success:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to update student'}), 500
            
    except Exception as e:
        print(f"Error updating student: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/students/<int:student_id>/delete', methods=['DELETE'])
@login_required
def delete_student(student_id):
    try:
        # Check if student exists and delete
        student = Student.get_by_id(student_id)
        if not student:
            return jsonify({'status': 'error', 'message': 'Student not found'}), 404
        
        # Delete profile picture if it exists
        if student.profile_picture:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'students', student.profile_picture)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Delete student record
        success = StudentController.delete_student(student_id)
        
        if success:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to delete student'}), 500
            
    except Exception as e:
        print(f"Error deleting student: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Public exit display routes
@app.route('/exit-display')
def exit_display():
    return render_template('public/exit_display.html')

@app.route('/api/strands')
def get_strands():
    try:
        grade_level = request.args.get('grade_level')
        strands = Strand.get_all()
        
        # If we have a grade level filter, we could filter here
        # Currently just returning all strands regardless of grade level
        
        return jsonify({'status': 'success', 'strands': strands})
    except Exception as e:
        print(f"Error getting strands: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/sections')
def get_sections():
    try:
        strand_id = request.args.get('strand_id')
        grade_level = request.args.get('grade_level')
        section_id = request.args.get('section_id')
        
        app.logger.info(f"API call: get sections with strand_id={strand_id}, grade_level={grade_level}, section_id={section_id}")
        
        if section_id:
            # Get a specific section by ID
            query = """
            SELECT s.section_id, s.section_name, s.strand_id, s.grade_level, 
                   str.strand_code, str.strand_name
            FROM sections s
            LEFT JOIN strands str ON s.strand_id = str.strand_id
            WHERE s.section_id = %s
            """
            sections = Database().fetch_all(query, (section_id,))
            app.logger.info(f"Retrieved section by ID: {sections}")
            return jsonify({'status': 'success', 'sections': sections})
        
        # Base query
        query = """
        SELECT s.section_id, s.section_name, s.strand_id, s.grade_level, 
               str.strand_code, str.strand_name
        FROM sections s
        LEFT JOIN strands str ON s.strand_id = str.strand_id
        """
        
        # Add filters
        params = []
        where_clauses = []
        
        if strand_id and strand_id.strip():
            where_clauses.append("s.strand_id = %s")
            params.append(strand_id)
            
        if grade_level and grade_level.strip():
            where_clauses.append("s.grade_level = %s")
            params.append(grade_level)
            
        # Add WHERE clause if any filters were applied
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
            
        # Add ordering
        query += " ORDER BY s.section_name"
        
        app.logger.info(f"Sections query: {query} with params {params}")
        sections = Database().fetch_all(query, tuple(params))
        app.logger.info(f"Found {len(sections)} sections")
        
        return jsonify({'status': 'success', 'sections': sections})
    except Exception as e:
        app.logger.error(f"Error getting sections: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/schedules')
def get_schedules():
    try:
        section_id = request.args.get('section_id')
        
        if not section_id:
            return jsonify({'status': 'error', 'message': 'Section ID is required'}), 400
        
        schedules = ClassSchedule.get_all_by_section(section_id)
        
        if not schedules:
            # Always include empty schedules array
            return jsonify({'status': 'success', 'schedules': []})
        
        # Format the time_start and time_end fields as strings
        for schedule in schedules:
            if isinstance(schedule['time_start'], timedelta):
                # Format timedelta as HH:MM
                seconds = schedule['time_start'].total_seconds()
                hours, remainder = divmod(seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                schedule['time_start'] = f"{int(hours):02d}:{int(minutes):02d}"
                
            if isinstance(schedule['time_end'], timedelta):
                # Format timedelta as HH:MM
                seconds = schedule['time_end'].total_seconds()
                hours, remainder = divmod(seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                schedule['time_end'] = f"{int(hours):02d}:{int(minutes):02d}"
        
        # Return only the JSON data since we're not using the HTML view anymore
        return jsonify({'status': 'success', 'schedules': schedules})
    except Exception as e:
        print(f"Error getting schedules: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/subjects')
def get_subjects():
    try:
        subjects_objects = Subject.get_all()
        # Convert objects to dictionaries for JSON serialization
        subjects = []
        for subject in subjects_objects:
            subjects.append({
                'subject_id': subject.id,
                'subject_code': subject.code,
                'subject_name': subject.name
            })
        return jsonify({'status': 'success', 'subjects': subjects})
    except Exception as e:
        print(f"Error getting subjects: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/teachers')
def get_teachers():
    try:
        teachers_objects = Teacher.get_all()
        # Convert objects to dictionaries for JSON serialization
        teachers = []
        for teacher in teachers_objects:
            teachers.append({
                'teacher_id': teacher.id,
                'first_name': teacher.first_name,
                'middle_initial': teacher.middle_initial,
                'last_name': teacher.last_name,
                'email': teacher.email
            })
        return jsonify({'status': 'success', 'teachers': teachers})
    except Exception as e:
        print(f"Error getting teachers: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/schedules/save', methods=['POST'])
def save_schedule():
    try:
        data = request.get_json()
        print(f"Schedule save request with data: {data}")
        
        # Validate required fields
        required_fields = ['section_id', 'subject_id', 'teacher_id', 'day_of_week', 'time_start', 'time_end']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'status': 'error', 'message': f'Missing required field: {field}'}), 400
        
        # Ensure day_of_week is uppercase for consistency
        data['day_of_week'] = data['day_of_week'].upper()
        
        # Prepare the query - either update or insert
        db = Database()
        if data.get('schedule_id'):
            # Update existing schedule
            query = """
                UPDATE class_schedules 
                SET section_id = %s, subject_id = %s, teacher_id = %s, 
                    day_of_week = %s, time_start = %s, time_end = %s
                WHERE schedule_id = %s
            """
            params = (
                data['section_id'], 
                data['subject_id'],
                data['teacher_id'],
                data['day_of_week'],
                data['time_start'],
                data['time_end'],
                data['schedule_id']
            )
            success = db.execute(query, params)
            if success:
                return jsonify({'status': 'success', 'message': 'Schedule updated successfully', 'schedule_id': data['schedule_id']})
            else:
                return jsonify({'status': 'error', 'message': 'Failed to update schedule'}), 500
        
        # The outer else for the if data.get('schedule_id') check  
        else:
            # Insert new schedule
            query = """
                INSERT INTO class_schedules (section_id, subject_id, teacher_id, day_of_week, time_start, time_end)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                data['section_id'], 
                data['subject_id'],
                data['teacher_id'],
                data['day_of_week'],
                data['time_start'],
                data['time_end']
            )
            schedule_id = db.insert(query, params)
            if schedule_id:
                return jsonify({'status': 'success', 'message': 'Schedule created successfully', 'schedule_id': schedule_id})
            else:
                return jsonify({'status': 'error', 'message': 'Failed to create schedule'}), 500
            
    except Exception as e:
        print(f"Error saving schedule: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/schedules/delete/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    try:
        schedule = ClassSchedule.get_by_id(schedule_id)
        if not schedule:
            return jsonify({'status': 'error', 'message': 'Schedule not found'}), 404
            
        result = schedule.delete()
        if result:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to delete schedule'}), 500
            
    except Exception as e:
        print(f"Error deleting schedule: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/schedules/<int:schedule_id>')
def get_schedule(schedule_id):
    try:
        # Use a join query instead of the basic get_by_id to get additional information
        db = Database()
        print(f"Fetching schedule with ID: {schedule_id}")
        
        query = """
            SELECT cs.*, s.subject_code, s.subject_name, 
                   t.first_name, t.middle_initial, t.last_name
            FROM class_schedules cs
            JOIN subjects s ON cs.subject_id = s.subject_id
            JOIN teachers t ON cs.teacher_id = t.teacher_id
            WHERE cs.schedule_id = %s
        """
        result = db.fetch_one(query, (schedule_id,))
        
        print(f"Query result for schedule ID {schedule_id}: {result}")
        
        if not result:
            print(f"Schedule with ID {schedule_id} not found")
            return jsonify({'status': 'error', 'message': 'Schedule not found'}), 404
            
        # Format time fields to HH:MM for the form
        from datetime import timedelta
        
        if isinstance(result['time_start'], timedelta):
            seconds = result['time_start'].total_seconds()
            hours, remainder = divmod(seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            # Ensure minutes are properly included in the formatted time
            time_start = f"{int(hours):02d}:{int(minutes):02d}"
            
            # Also create a formatted AM/PM version for display purposes
            from datetime import datetime
            time_obj = datetime.strptime(time_start, '%H:%M')
            time_start_display = time_obj.strftime('%I:%M %p')
        else:
            time_start = result['time_start']
            time_start_display = result['time_start']
            
        if isinstance(result['time_end'], timedelta):
            seconds = result['time_end'].total_seconds()
            hours, remainder = divmod(seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            # Ensure minutes are properly included in the formatted time
            time_end = f"{int(hours):02d}:{int(minutes):02d}"
            
            # Also create a formatted AM/PM version for display purposes
            from datetime import datetime
            time_obj = datetime.strptime(time_end, '%H:%M')
            time_end_display = time_obj.strftime('%I:%M %p')
        else:
            time_end = result['time_end']
            time_end_display = result['time_end']
            
        schedule_data = {
            'schedule_id': result['schedule_id'],
            'section_id': result['section_id'],
            'subject_id': result['subject_id'],
            'teacher_id': result['teacher_id'],
            'day_of_week': result['day_of_week'],
            'time_start': time_start,
            'time_end': time_end,
            'time_start_display': time_start_display,
            'time_end_display': time_end_display,
            'subject_code': result['subject_code'],
            'subject_name': result['subject_name'],
            'first_name': result['first_name'],
            'middle_initial': result['middle_initial'],
            'last_name': result['last_name']
        }
        
        print(f"Returning schedule data: {schedule_data}")
        return jsonify({'status': 'success', 'schedule': schedule_data})
    except Exception as e:
        print(f"Error getting schedule: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    app.logger.info(f"Client connected: {request.sid}")
    # Send initial exit logs to the client
    try:
        exit_logs = get_formatted_exit_logs(limit=20)
        if exit_logs:
            app.logger.info(f"Sending initial {len(exit_logs)} exit logs to client {request.sid}")
            emit('initial_exits', exit_logs)
        else:
            app.logger.warning(f"No exit logs found to send to client {request.sid}")
    except Exception as e:
        app.logger.error(f"Error sending initial exit logs: {str(e)}")

@socketio.on('disconnect')
def handle_disconnect():
    app.logger.info(f"Client disconnected: {request.sid}")

@socketio.on('test_connection')
def handle_test_connection():
    app.logger.info(f"Received test connection from client {request.sid}")
    emit('test_response', {'status': 'connected', 'time': datetime.now().isoformat()})

@socketio.on('error')
def handle_error(error):
    app.logger.error(f"Socket.IO error from client {request.sid}: {error}")

# Function to emit exit logs to all clients
def emit_exit_log(exit_log):
    """
    Emit exit log to all connected Socket.IO clients
    This ensures real-time updates across all instances
    """
    try:
        if not exit_log:
            app.logger.warning("Attempted to emit None exit log")
            return False
            
        app.logger.info(f"Emitting exit log to all clients: {exit_log.get('student_name') if isinstance(exit_log, dict) else 'unknown'}")
        
        # Format the exit log for the client
        if not isinstance(exit_log, dict):
            try:
                # Convert to dict if it's a model object
                app.logger.error(f"Exit log is not a dict, this is not supported")
                return False
            except Exception as e:
                app.logger.error(f"Error handling exit log: {str(e)}")
                return False

        # Ensure exit_time is serializable
        if 'exit_time' in exit_log and not isinstance(exit_log['exit_time'], str):
            try:
                exit_log['exit_time'] = exit_log['exit_time'].isoformat()
            except (AttributeError, TypeError) as e:
                app.logger.error(f"Error formatting exit time: {str(e)}")
                exit_log['exit_time'] = str(exit_log['exit_time'])

        # Broadcast to all clients
        socketio.emit('new_exit_log', exit_log, broadcast=True)
        app.logger.info(f"Successfully emitted exit log to all clients")
        return True
    except Exception as e:
        app.logger.error(f"Error emitting exit log: {str(e)}")
        return False

# Function to get formatted exit logs
def get_formatted_exit_logs(limit=20):
    """
    Get formatted exit logs from the database
    """
    try:
        # Get raw logs from ExitLog model
        raw_logs = ExitLog.get_recent_logs(limit=limit)
        
        if not raw_logs:
            app.logger.warning("No exit logs found in database")
            return []
            
        # Format the logs for the client
        formatted_logs = []
        for log in raw_logs:
            try:
                # Create proper student name
                student_name = f"{log['first_name']} "
                if log['middle_initial']:
                    student_name += f"{log['middle_initial']}. "
                student_name += f"{log['last_name']}"
                
                # Create grade section
                grade_section = f"Grade {log['grade_level']}"
                if log['section_name']:
                    grade_section += f" - {log['section_name']}"
                
                # Format timestamp
                timestamp_formatted = None
                if 'timestamp' in log and log['timestamp']:
                    try:
                        # Format to ISO string if it's a datetime object
                        if isinstance(log['timestamp'], datetime):
                            timestamp_formatted = log['timestamp'].isoformat()
                        else:
                            timestamp_formatted = str(log['timestamp'])
                    except Exception as e:
                        app.logger.error(f"Error formatting timestamp: {str(e)}")
                        timestamp_formatted = str(log['timestamp'])
                
                # Format profile picture path to ensure it's a valid URL path
                profile_picture = '/static/img/default-profile.png'
                
                if 'profile_picture' in log and log['profile_picture']:
                    # If it's already a full path, use it as is
                    if log['profile_picture'].startswith('/static/'):
                        profile_picture = log['profile_picture']
                    # Otherwise, add the proper path prefix
                    else:
                        profile_picture = f"/static/uploads/students/{log['profile_picture']}"
                
                app.logger.info(f"Formatted profile picture: {profile_picture}")
                
                # Create standardized format for client
                formatted_log = {
                    'student_name': student_name,
                    'id_number': log['id_number'],
                    'grade_section': grade_section,
                    'exit_time': timestamp_formatted,
                    'status': log['status'].upper() if log['status'] else 'UNKNOWN',
                    'profile_picture': profile_picture
                }
                
                formatted_logs.append(formatted_log)
            except Exception as e:
                app.logger.error(f"Error formatting log {log}: {str(e)}")
                # Skip this log and continue
        
        app.logger.info(f"Returning {len(formatted_logs)} formatted exit logs")
        return formatted_logs
    except Exception as e:
        app.logger.error(f"Error getting formatted exit logs: {str(e)}")
        return []

# Function to get the latest exit log for a student with a specific RFID
def get_latest_exit_log_by_rfid(rfid_uid):
    """
    Get the latest exit log for a student with a specific RFID
    """
    try:
        if not rfid_uid:
            app.logger.error("No RFID UID provided")
            return None
            
        # Get student ID from RFID
        db = Database()
        student_query = "SELECT student_id FROM students WHERE rfid_uid = %s LIMIT 1"
        student_result = db.fetch_one(student_query, (rfid_uid,))
        
        if not student_result:
            app.logger.warning(f"No student found with RFID: {rfid_uid}")
            return None
            
        student_id = student_result['student_id']
        
        # Get the latest exit log for this student
        exit_query = """
            SELECT el.*, s.first_name, s.middle_initial, s.last_name, s.id_number, 
                   s.grade_level, s.profile_picture, sec.section_name
            FROM exit_logs el
            JOIN students s ON el.student_id = s.student_id
            LEFT JOIN sections sec ON s.section_id = sec.section_id
            WHERE el.student_id = %s
            ORDER BY el.timestamp DESC
            LIMIT 1
        """
        exit_log = db.fetch_one(exit_query, (student_id,))
        
        if not exit_log:
            app.logger.warning(f"No exit log found for student with RFID: {rfid_uid}")
            return None
            
        # Format the exit log
        student_name = f"{exit_log['first_name']} "
        if exit_log['middle_initial']:
            student_name += f"{exit_log['middle_initial']}. "
        student_name += f"{exit_log['last_name']}"
        
        grade_section = f"Grade {exit_log['grade_level']}"
        if exit_log['section_name']:
            grade_section += f" - {exit_log['section_name']}"
        
        # Format profile picture URL
        profile_picture = '/static/img/default-profile.png'
        if exit_log['profile_picture']:
            profile_picture = f"/static/uploads/students/{exit_log['profile_picture']}"
        
        # Format timestamp
        timestamp_formatted = None
        if 'timestamp' in exit_log and exit_log['timestamp']:
            try:
                # Format to ISO string if it's a datetime object
                if isinstance(exit_log['timestamp'], datetime):
                    timestamp_formatted = exit_log['timestamp'].isoformat()
                else:
                    timestamp_formatted = str(exit_log['timestamp'])
            except Exception as e:
                app.logger.error(f"Error formatting timestamp: {str(e)}")
                timestamp_formatted = str(exit_log['timestamp'])
        
        # Create formatted exit log
        formatted_log = {
            'student_name': student_name,
            'id_number': exit_log['id_number'],
            'grade_section': grade_section,
            'exit_time': timestamp_formatted,
            'status': exit_log['status'].upper() if exit_log['status'] else 'UNKNOWN',
            'profile_picture': profile_picture
        }
        
        return formatted_log
    except Exception as e:
        app.logger.error(f"Error getting latest exit log by RFID: {str(e)}")
        return None

@app.route('/process_exit', methods=['POST'])
def process_exit():
    """
    Process an exit request based on RFID
    This endpoint is called when a student taps their RFID card
    """
    try:
        # Get RFID from request data
        data = request.get_json() or {}
        rfid_uid = data.get('rfid_uid')
        
        if not rfid_uid:
            app.logger.error("No RFID UID provided in process_exit request")
            return jsonify({'status': 'error', 'message': 'No RFID UID provided'}), 400
            
        app.logger.info(f"Processing exit for RFID: {rfid_uid}")
        
        # Process the exit using ExitController
        result = ExitController.process_exit_request(rfid_uid)
        
        if result.get('status') == 'success':
            app.logger.info(f"Exit processed successfully: {result.get('message')}")
            
            # Get the most recent exit log for this student to emit via Socket.IO
            try:
                # Get most recent exit log directly
                exit_log = get_latest_exit_log_by_rfid(rfid_uid)
                
                if exit_log:
                    app.logger.info(f"Found exit log for emission: {exit_log.get('student_name')}")
                    
                    # Emit to all connected clients
                    emission_success = emit_exit_log(exit_log)
                    
                    if not emission_success:
                        app.logger.warning("First emission attempt failed, retrying...")
                        # Try one more time after a short delay
                        time.sleep(0.5)
                        emit_exit_log(exit_log)
                else:
                    app.logger.warning(f"No exit log found after processing exit for RFID: {rfid_uid}")
            except Exception as e:
                app.logger.error(f"Error emitting exit log for RFID {rfid_uid}: {str(e)}")
        else:
            app.logger.warning(f"Exit processing failed: {result.get('message')}")
            
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"Error in process_exit: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/student/rfid/<rfid_uid>')
def get_student_by_rfid(rfid_uid):
    try:
        query = """
            SELECT s.*, 
                   CASE 
                       WHEN s.profile_picture IS NULL OR s.profile_picture = ''
                       THEN '/static/img/default-profile.png'
                       ELSE CONCAT('/static/uploads/students/', s.profile_picture)
                   END as photo,
                   sec.section_name
            FROM students s
            LEFT JOIN sections sec ON s.section_id = sec.section_id
            WHERE s.rfid_uid = %s
            LIMIT 1
        """
        student = Database().fetch_one(query, (rfid_uid,))
        
        if not student:
            return jsonify({'message': 'Student not found'}), 404
        
        return jsonify({
            'id_number': student['id_number'],
            'name': f"{student['first_name']} {student['middle_initial'] + '.' if student['middle_initial'] else ''} {student['last_name']}",
            'grade_section': f"Grade {student['grade_level']} - {student['section_name']}",
            'photo': student['photo']
        })
    except Exception as e:
        print(f"Error getting student by RFID: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/student-id-layout')
def student_id_layout():
    return render_template('public/student_id_layout.html')

@app.route('/api/check-status')
def check_status():
    try:
        last_timestamp = request.args.get('last_timestamp')
        
        # Default query for no timestamp
        query = """
        SELECT 
            el.log_id,
            el.timestamp,
            el.status,
            el.reason,
            s.student_id,
            s.id_number,
            s.first_name, 
            s.middle_initial,
            s.last_name,
            s.grade_level,
            CASE 
                WHEN s.profile_picture IS NULL OR s.profile_picture = ''
                THEN '/static/img/default-profile.png'
                ELSE CONCAT('/static/uploads/students/', s.profile_picture)
            END as profile_picture,
            IFNULL(sec.section_name, 'Unknown Section') as section_name,
            IFNULL(st.strand_code, '') as strand_code
        FROM exit_logs el
        JOIN students s ON el.student_id = s.student_id
        LEFT JOIN sections sec ON s.section_id = sec.section_id
        LEFT JOIN strands st ON sec.strand_id = st.strand_id
        WHERE 1=1
        """
        
        query_params = []
        
        if last_timestamp:
            try:
                # Convert JavaScript timestamp (milliseconds) to MySQL datetime format
                last_time = datetime.fromtimestamp(int(last_timestamp) / 1000.0)
                query += " AND el.timestamp > %s"
                query_params = [last_time]
            except (ValueError, TypeError) as e:
                print(f"Error parsing timestamp: {e}")
        
        query += " ORDER BY el.timestamp DESC LIMIT 5"
        
        recent_exits = Database().fetch_all(query, tuple(query_params))
        
        if not recent_exits:
            return jsonify({'update': False})
        
        formatted_exits = []
        for exit in recent_exits:
            timestamp_str = None
            if exit['timestamp']:
                try:
                    timestamp_str = exit['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                except:
                    timestamp_str = str(exit['timestamp'])
                    
            formatted_exit = {
                'log_id': exit['log_id'],
                'first_name': exit['first_name'] or '',
                'middle_initial': exit['middle_initial'] or '',
                'last_name': exit['last_name'] or '',
                'id_number': exit['id_number'] or 'Unknown',
                'grade_level': exit['grade_level'] or '',
                'section_name': exit['section_name'],
                'strand_code': exit['strand_code'],
                'status': exit['status'] or 'UNKNOWN',
                'reason': exit['reason'] or '',
                'timestamp': timestamp_str,
                'profile_picture': exit['profile_picture']
            }
            formatted_exits.append(formatted_exit)
        
        return jsonify({'update': True, 'exits': formatted_exits})
    except Exception as e:
        print(f"Error checking status: {str(e)}")
        return jsonify({'update': False, 'error': str(e)})

@app.route('/api/check-rfid-scan')
def check_rfid_scan():
    try:
        # Get the most recent RFID scan
        rfid_uid = rfid_reader.get_last_scan()
        
        if rfid_uid:
            # Clear the last scan to prevent duplicate readings
            rfid_reader.clear_last_scan()
            
            return jsonify({
                'rfid_detected': True,
                'rfid_uid': rfid_uid
            })
        else:
            return jsonify({
                'rfid_detected': False
            })
    except Exception as e:
        print(f"Error checking RFID scan: {str(e)}")
        return jsonify({
            'rfid_detected': False,
            'error': str(e)
        })

@app.route('/api/subjects/create', methods=['POST'])
@login_required
def create_subject():
    try:
        # Get subject data from request
        data = request.json
        subject_code = data.get('subject_code')
        subject_name = data.get('subject_name')
        
        # Validate required fields
        if not subject_code or not subject_name:
            return jsonify({'status': 'error', 'message': 'Subject code and name are required'}), 400
        
        # Check if subject code already exists
        existing_subject = Subject.get_by_code(subject_code)
        if existing_subject:
            return jsonify({'status': 'error', 'message': 'Subject code already exists'}), 400
        
        # Create and save new subject
        subject = Subject(code=subject_code, name=subject_name)
        subject_id = subject.save()
        
        if subject_id:
            return jsonify({
                'status': 'success', 
                'subject': {
                    'subject_id': subject_id,
                    'subject_code': subject_code,
                    'subject_name': subject_name
                }
            })
        else:
            return jsonify({'status': 'error', 'message': 'Failed to create subject'}), 500
            
    except Exception as e:
        print(f"Error creating subject: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/teachers/create', methods=['POST'])
@login_required
def create_teacher():
    try:
        # Get teacher data from request
        data = request.json
        first_name = data.get('first_name', '').strip().upper()
        middle_initial = data.get('middle_initial', '').strip().upper()
        last_name = data.get('last_name', '').strip().upper()
        email = data.get('email', '').strip()  # Email should not be capitalized
        
        # Validate required fields
        if not first_name or not last_name:
            return jsonify({'status': 'error', 'message': 'First name and last name are required'}), 400
        
        # Create and save new teacher
        teacher = Teacher(
            first_name=first_name,
            middle_initial=middle_initial,
            last_name=last_name,
            email=email
        )
        teacher_id = teacher.save()
        
        if teacher_id:
            return jsonify({
                'status': 'success', 
                'teacher': {
                    'teacher_id': teacher_id,
                    'first_name': first_name,
                    'middle_initial': middle_initial,
                    'last_name': last_name,
                    'email': email
                }
            })
        else:
            return jsonify({'status': 'error', 'message': 'Failed to create teacher'}), 500
            
    except Exception as e:
        print(f"Error creating teacher: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/process-rfid', methods=['POST'])
def process_rfid():
    try:
        data = request.get_json()
        if not data or 'rfid_uid' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Invalid request format'
            }), 400
        
        # Process the RFID card
        rfid_uid = data['rfid_uid']
        rfid_reader.process_card(rfid_uid)
        
        return jsonify({
            'status': 'success',
            'message': 'RFID card processed successfully'
        })
    except Exception as e:
        app.logger.error(f"Error processing RFID: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error processing RFID: {str(e)}'
        }), 500

@app.route('/api/recent-exits')
def get_recent_exits():
    try:
        app.logger.info("Recent exits API endpoint called")
        
        # Add timestamp to log to help with debugging
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        app.logger.info(f"Request time: {current_time}")
        
        # Fetch the formatted exit logs with strong caching prevention
        limit = request.args.get('limit', default=20, type=int)
        app.logger.info(f"Fetching {limit} most recent exit logs")
        
        exit_logs = get_formatted_exit_logs(limit=limit)
        
        # Log what we're returning
        app.logger.info(f"Returning {len(exit_logs)} formatted exit logs")
        
        # Create response with strong no-cache headers
        response = jsonify(exit_logs)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['Last-Modified'] = current_time
        
        return response
    except Exception as e:
        app.logger.error(f"Error in get_recent_exits: {str(e)}")
        return jsonify([])

if __name__ == '__main__':
    try:
        app.logger.info("Starting Exit Management System server with Socket.IO")
        app.logger.info(f"Socket.IO configured with mode: {socketio.async_mode}")
        
        # Only run the socketio server when executing this file directly (not in Vercel)
        socketio.run(app, 
                    host='0.0.0.0', 
                    port=5000, 
                    debug=True, 
                    log_output=True)
    except Exception as e:
        app.logger.error(f"Error starting server: {str(e)}", exc_info=True)