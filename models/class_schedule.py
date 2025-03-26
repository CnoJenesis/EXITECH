from database.db_connector import Database
from datetime import datetime, time

class ClassSchedule:
    def __init__(self, id=None, section_id=None, subject_id=None, teacher_id=None, 
                 day_of_week=None, time_start=None, time_end=None):
        self.id = id
        self.section_id = section_id
        self.subject_id = subject_id
        self.teacher_id = teacher_id
        self.day_of_week = day_of_week
        self.time_start = time_start
        self.time_end = time_end
        self.db = Database()

    def save(self):
        if self.id:
            # Update existing schedule
            query = """
                UPDATE class_schedules 
                SET section_id = %s, subject_id = %s, teacher_id = %s,
                    day_of_week = %s, time_start = %s, time_end = %s
                WHERE schedule_id = %s
            """
            params = (self.section_id, self.subject_id, self.teacher_id,
                      self.day_of_week, self.time_start, self.time_end, self.id)
            self.db.execute(query, params)
            return self.id
        else:
            # Insert new schedule
            query = """
                INSERT INTO class_schedules 
                (section_id, subject_id, teacher_id, day_of_week, time_start, time_end)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (self.section_id, self.subject_id, self.teacher_id,
                      self.day_of_week, self.time_start, self.time_end)
            return self.db.insert(query, params)

    def delete(self):
        if self.id:
            query = "DELETE FROM class_schedules WHERE schedule_id = %s"
            self.db.execute(query, (self.id,))
            return True
        return False

    @staticmethod
    def get_by_id(schedule_id):
        db = Database()
        query = "SELECT * FROM class_schedules WHERE schedule_id = %s"
        result = db.fetch_one(query, (schedule_id,))
        if result:
            return ClassSchedule(
                id=result['schedule_id'],
                section_id=result['section_id'],
                subject_id=result['subject_id'],
                teacher_id=result['teacher_id'],
                day_of_week=result['day_of_week'],
                time_start=result['time_start'],
                time_end=result['time_end']
            )
        return None

    @staticmethod
    def get_all_by_section(section_id):
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
        return db.fetch_all(query, (section_id,))

    @staticmethod
    def get_current_classes():
        db = Database()
        # Get current day of week (0 = Monday, 6 = Sunday)
        current_day = datetime.now().weekday()
        # Convert to our format (Monday, Tuesday, etc.)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_day_name = days[current_day]
        
        # Get current time
        current_time = datetime.now().time()
        
        query = """
            SELECT cs.*, s.subject_code, s.subject_name, 
                   t.first_name, t.middle_initial, t.last_name,
                   sec.section_name, sec.grade_level,
                   str.strand_code
            FROM class_schedules cs
            JOIN subjects s ON cs.subject_id = s.subject_id
            JOIN teachers t ON cs.teacher_id = t.teacher_id
            JOIN sections sec ON cs.section_id = sec.section_id
            JOIN strands str ON sec.strand_id = str.strand_id
            WHERE cs.day_of_week = %s
            AND cs.time_start <= %s AND cs.time_end >= %s
        """
        return db.fetch_all(query, (current_day_name, current_time, current_time))

    @staticmethod
    def is_student_in_class(student_id):
        db = Database()
        # Get current day of week and time
        current_day = datetime.now().weekday()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_day_name = days[current_day]
        current_time = datetime.now().time()
        
        print(f"\n=== CLASS SCHEDULE CHECK ===")
        print(f"Current time: {current_time}")
        print(f"Current day: {current_day_name}")
        print(f"Checking schedule for student ID: {student_id}")
        
        # First, let's get student's section
        student_section_query = """
            SELECT s.section_id, sec.section_name, sec.grade_level,
                  IFNULL(str.strand_code, '') as strand_code,
                  s.id_number
            FROM students s
            JOIN sections sec ON s.section_id = sec.section_id
            LEFT JOIN strands str ON sec.strand_id = str.strand_id
            WHERE s.student_id = %s
        """
        student_section = db.fetch_one(student_section_query, (student_id,))
        
        if not student_section:
            print(f"❌ ERROR: Student {student_id} not found or has no section assigned")
            return True, "No section assigned"
            
        section_id = student_section['section_id']
        section_name = student_section['section_name']
        strand_code = student_section['strand_code']
        grade_level = student_section['grade_level']
        id_number = student_section['id_number']
        
        print(f"\n👤 Student Info:")
        print(f"  ID Number: {id_number}")
        print(f"  Section ID: {section_id}")
        print(f"  Section: {strand_code} {grade_level} - {section_name}")
        
        # Check for current class
        current_class_query = """
            SELECT cs.schedule_id, s.subject_name, cs.time_start, cs.time_end,
                   t.first_name, t.last_name
            FROM class_schedules cs
            JOIN subjects s ON cs.subject_id = s.subject_id
            JOIN teachers t ON cs.teacher_id = t.teacher_id
            WHERE cs.section_id = %s
            AND cs.day_of_week = %s
            AND CAST(%s AS time) BETWEEN cs.time_start AND cs.time_end
        """
        
        current_time_str = current_time.strftime('%H:%M:%S')
        print(f"\n🔍 Checking for class at {current_time_str}")
        
        current_class = db.fetch_one(current_class_query, (
            section_id,
            current_day_name,
            current_time_str
        ))
        
        if current_class:
            print(f"\n❌ Found active class:")
            print(f"  Subject: {current_class['subject_name']}")
            print(f"  Time: {current_class['time_start']} - {current_class['time_end']}")
            print(f"  Teacher: {current_class['first_name']} {current_class['last_name']}")
            print(f"EXIT DENIED - Student has ongoing class")
            return True, f"Class in progress: {current_class['subject_name']}"
        
        print(f"\n✅ No active classes found")
        print(f"EXIT ALLOWED - Student is free to leave")
        return False, "No active classes"