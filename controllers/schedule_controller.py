from models.class_schedule import ClassSchedule
from models.section import Section
from models.subject import Subject
from models.teacher import Teacher
# Fix the database import
from database.db_connector import Database  # Correct import path
from datetime import datetime, timedelta

class ScheduleController:
    @staticmethod
    def get_schedules_by_section(section_id):
        """Get all schedules for a specific section with related data"""
        db = Database()
        query = """
        SELECT cs.*, s.subject_code, s.subject_name, 
               t.first_name, t.middle_initial, t.last_name
        FROM class_schedules cs
        JOIN subjects s ON cs.subject_id = s.subject_id
        JOIN teachers t ON cs.teacher_id = t.teacher_id
        WHERE cs.section_id = %s
        ORDER BY cs.day_of_week, cs.time_start
        """
        schedules = db.fetch_all(query, (section_id,))
        db.close()
        
        # Format teacher name
        for schedule in schedules:
            middle_initial = f"{schedule['middle_initial']}. " if schedule['middle_initial'] else ""
            schedule['teacher_name'] = f"{schedule['first_name']} {middle_initial}{schedule['last_name']}"
        
        return schedules
    
    @staticmethod
    def get_schedule_by_id(schedule_id):
        """Get a specific schedule by ID with related data"""
        db = Database()
        query = """
        SELECT cs.*, s.subject_code, s.subject_name, 
               t.first_name, t.middle_initial, t.last_name,
               sec.section_name, sec.grade_level
        FROM class_schedules cs
        JOIN subjects s ON cs.subject_id = s.subject_id
        JOIN teachers t ON cs.teacher_id = t.teacher_id
        JOIN sections sec ON cs.section_id = sec.section_id
        WHERE cs.schedule_id = %s
        """
        schedule = db.fetch_one(query, (schedule_id,))
        db.close()
        
        if schedule:
            middle_initial = f"{schedule['middle_initial']}. " if schedule['middle_initial'] else ""
            schedule['teacher_name'] = f"{schedule['first_name']} {middle_initial}{schedule['last_name']}"
        
        return schedule
    
    @staticmethod
    def check_schedule_conflict(section_id, day_of_week, time_start, time_end, exclude_id=None):
        """Check if there's a schedule conflict for the given section, day and time"""
        db = Database()
        
        # Convert time strings to datetime objects for comparison
        try:
            time_start_obj = datetime.strptime(time_start, '%I:%M %p').time()
            time_end_obj = datetime.strptime(time_end, '%I:%M %p').time()
        except ValueError:
            # Try alternative format
            try:
                time_start_obj = datetime.strptime(time_start, '%H:%M').time()
                time_end_obj = datetime.strptime(time_end, '%H:%M').time()
            except ValueError:
                return True  # Invalid time format
        
        # Build query to check for conflicts
        query = """
        SELECT COUNT(*) as conflict_count
        FROM class_schedules
        WHERE section_id = %s
        AND day_of_week = %s
        AND (
            (time_start <= %s AND time_end > %s) OR
            (time_start < %s AND time_end >= %s) OR
            (time_start >= %s AND time_end <= %s)
        )
        """
        params = (
            section_id, day_of_week, 
            time_end_obj, time_start_obj,
            time_end_obj, time_start_obj,
            time_start_obj, time_end_obj
        )
        
        # Exclude the current schedule if editing
        if exclude_id:
            query += " AND schedule_id != %s"
            params += (exclude_id,)
        
        result = db.fetch_one(query, params)
        db.close()
        
        return result['conflict_count'] > 0
    
    @staticmethod
    def add_schedule(section_id, subject_id, teacher_id, day_of_week, time_start, time_end):
        """Add a new schedule"""
        try:
            # Convert time strings to datetime objects
            time_start_obj = datetime.strptime(time_start, '%I:%M %p').time()
            time_end_obj = datetime.strptime(time_end, '%I:%M %p').time()
        except ValueError:
            # Try alternative format
            try:
                time_start_obj = datetime.strptime(time_start, '%H:%M').time()
                time_end_obj = datetime.strptime(time_end, '%H:%M').time()
            except ValueError:
                return False  # Invalid time format
        
        db = Database()
        query = """
        INSERT INTO class_schedules (section_id, subject_id, teacher_id, day_of_week, time_start, time_end)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        result = db.execute(query, (section_id, subject_id, teacher_id, day_of_week, time_start_obj, time_end_obj))
        db.close()
        
        return result
    
    @staticmethod
    def update_schedule(schedule_id, subject_id, teacher_id, day_of_week, time_start, time_end):
        """Update an existing schedule"""
        try:
            # Convert time strings to datetime objects
            time_start_obj = datetime.strptime(time_start, '%I:%M %p').time()
            time_end_obj = datetime.strptime(time_end, '%I:%M %p').time()
        except ValueError:
            # Try alternative format
            try:
                time_start_obj = datetime.strptime(time_start, '%H:%M').time()
                time_end_obj = datetime.strptime(time_end, '%H:%M').time()
            except ValueError:
                return False  # Invalid time format
        
        db = Database()
        query = """
        UPDATE class_schedules
        SET subject_id = %s, teacher_id = %s, day_of_week = %s, time_start = %s, time_end = %s
        WHERE schedule_id = %s
        """
        result = db.execute(query, (subject_id, teacher_id, day_of_week, time_start_obj, time_end_obj, schedule_id))
        db.close()
        
        return result
    
    @staticmethod
    def delete_schedule(schedule_id):
        """Delete a schedule"""
        db = Database()
        query = "DELETE FROM class_schedules WHERE schedule_id = %s"
        result = db.execute(query, (schedule_id,))
        db.close()
        
        return result
    
    @staticmethod
    def get_section_schedule(section_id):
        return ClassSchedule.get_all_by_section(section_id)
    
    @staticmethod
    def create_schedule(data):
        schedule = ClassSchedule(
            section_id=data.get('section_id'),
            subject_id=data.get('subject_id'),
            teacher_id=data.get('teacher_id'),
            day_of_week=data.get('day_of_week'),
            time_start=data.get('time_start'),
            time_end=data.get('time_end')
        )
        return schedule.save()
    
    @staticmethod
    def update_schedule(schedule_id, data):
        schedule = ClassSchedule.get_by_id(schedule_id)
        if not schedule:
            return False
        
        schedule.section_id = data.get('section_id', schedule.section_id)
        schedule.subject_id = data.get('subject_id', schedule.subject_id)
        schedule.teacher_id = data.get('teacher_id', schedule.teacher_id)
        schedule.day_of_week = data.get('day_of_week', schedule.day_of_week)
        schedule.time_start = data.get('time_start', schedule.time_start)
        schedule.time_end = data.get('time_end', schedule.time_end)
        
        return schedule.save()
    
    @staticmethod
    def delete_schedule(schedule_id):
        schedule = ClassSchedule.get_by_id(schedule_id)
        if schedule:
            return schedule.delete()
        return False
    
    @staticmethod
    def get_current_classes():
        return ClassSchedule.get_current_classes()
    
    @staticmethod
    def get_timetable_data(section_id):
        # Get all schedules for the section
        schedules = ClassSchedule.get_all_by_section(section_id)
        
        # Organize by day and time
        timetable = {
            'Monday': {},
            'Tuesday': {},
            'Wednesday': {},
            'Thursday': {},
            'Friday': {}
        }
        
        for schedule in schedules:
            day = schedule['day_of_week']
            time_start = schedule['time_start']
            time_end = schedule['time_end']
            
            # Convert timedelta to hours and minutes
            start_hours = time_start.seconds // 3600
            start_minutes = (time_start.seconds % 3600) // 60
            end_hours = time_end.seconds // 3600
            end_minutes = (time_end.seconds % 3600) // 60
            
            # Create base datetime
            base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            start_datetime = base_date.replace(hour=start_hours, minute=start_minutes)
            end_datetime = base_date.replace(hour=end_hours, minute=end_minutes)
            
            # Create time slots in 15-minute intervals
            current_time = start_datetime
            while current_time < end_datetime:
                time_slot = current_time.strftime('%I:%M %p')
                
                if time_slot not in timetable[day]:
                    timetable[day][time_slot] = []
                
                # Convert timedelta to formatted time string for display
                start_time_str = f"{start_hours:02d}:{start_minutes:02d}"
                end_time_str = f"{end_hours:02d}:{end_minutes:02d}"
                start_obj = datetime.strptime(start_time_str, '%H:%M')
                end_obj = datetime.strptime(end_time_str, '%H:%M')
                
                timetable[day][time_slot].append({
                    'schedule_id': schedule['schedule_id'],
                    'subject_code': schedule['subject_code'],
                    'subject_name': schedule['subject_name'],
                    'teacher_name': f"{schedule['first_name']} {schedule['middle_initial'] + '.' if schedule['middle_initial'] else ''} {schedule['last_name']}",
                    'start_time': start_obj.strftime('%I:%M %p'),
                    'end_time': end_obj.strftime('%I:%M %p'),
                    'subject_id': schedule['subject_id'],
                    'teacher_id': schedule['teacher_id']
                })
                
                # Increment by 15 minutes
                current_time += timedelta(minutes=15)
        
        return timetable