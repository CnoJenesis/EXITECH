from models.database import Database  # Update this line

class Student:
    def __init__(self, id=None, id_number=None, first_name=None, middle_initial=None, 
                 last_name=None, grade_level=None, strand_id=None, section_id=None, 
                 rfid_uid=None, profile_picture=None):
        self.id = id
        self.id_number = id_number
        self.first_name = first_name
        self.middle_initial = middle_initial
        self.last_name = last_name
        self.grade_level = grade_level
        self.strand_id = strand_id
        self.section_id = section_id
        self.rfid_uid = rfid_uid
        self.profile_picture = profile_picture
        self.db = Database()

    def save(self):
        if self.id:
            # Update existing student
            query = """
                UPDATE students 
                SET id_number = %s, first_name = %s, middle_initial = %s, 
                    last_name = %s, grade_level = %s, strand_id = %s, 
                    section_id = %s, rfid_uid = %s, profile_picture = %s
                WHERE student_id = %s
            """
            params = (self.id_number, self.first_name, self.middle_initial, 
                      self.last_name, self.grade_level, self.strand_id, 
                      self.section_id, self.rfid_uid, self.profile_picture, self.id)
            self.db.execute(query, params)
            return self.id
        else:
            # Insert new student
            query = """
                INSERT INTO students 
                (id_number, first_name, middle_initial, last_name, grade_level, 
                 strand_id, section_id, rfid_uid, profile_picture)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (self.id_number, self.first_name, self.middle_initial, 
                      self.last_name, self.grade_level, self.strand_id, 
                      self.section_id, self.rfid_uid, self.profile_picture)
            return self.db.insert(query, params)

    def delete(self):
        if self.id:
            query = "DELETE FROM students WHERE student_id = %s"
            self.db.execute(query, (self.id,))
            return True
        return False

    @staticmethod
    def get_by_id(student_id):
        db = Database()
        query = "SELECT * FROM students WHERE student_id = %s"
        result = db.fetch_one(query, (student_id,))
        if result:
            return Student(
                id=result['student_id'],
                id_number=result['id_number'],
                first_name=result['first_name'],
                middle_initial=result['middle_initial'],
                last_name=result['last_name'],
                grade_level=result['grade_level'],
                strand_id=result['strand_id'],
                section_id=result['section_id'],
                rfid_uid=result['rfid_uid'],
                profile_picture=result['profile_picture']
            )
        return None

    @staticmethod
    @staticmethod
    def get_by_rfid(rfid_uid):
        db = Database()
        try:
            cleaned_rfid = rfid_uid.strip()
            query = """
                SELECT s.*, 
                    CASE 
                        WHEN s.profile_picture IS NULL OR s.profile_picture = '' 
                        THEN '/static/img/default-profile.png'
                        ELSE CONCAT('/static/uploads/students/', s.profile_picture)
                    END as profile_picture_path
                FROM students s
                WHERE s.rfid_uid = %s
                LIMIT 1
            """
            result = db.fetch_one(query, (cleaned_rfid,))
            
            if result:
                print(f"Found student: {result['first_name']} {result['last_name']}")
                print(f"Profile picture path: {result['profile_picture_path']}")
                return Student(
                    id=result['student_id'],
                    id_number=result['id_number'],
                    rfid_uid=result['rfid_uid'],
                    first_name=result['first_name'],
                    middle_initial=result['middle_initial'],
                    last_name=result['last_name'],
                    grade_level=result['grade_level'],
                    strand_id=result['strand_id'],
                    section_id=result['section_id'],
                    profile_picture=result['profile_picture_path']
                )
            
            print(f"No student found with RFID UID: '{cleaned_rfid}'")
            return None
        finally:
            db.close()

    @staticmethod
    def get_all_by_section(section_id):
        db = Database()
        query = "SELECT * FROM students WHERE section_id = %s ORDER BY last_name, first_name"
        results = db.fetch_all(query, (section_id,))
        students = []
        for result in results:
            students.append(Student(
                id=result['student_id'],
                id_number=result['id_number'],
                first_name=result['first_name'],
                middle_initial=result['middle_initial'],
                last_name=result['last_name'],
                grade_level=result['grade_level'],
                strand_id=result['strand_id'],
                section_id=result['section_id'],
                rfid_uid=result['rfid_uid'],
                profile_picture=result['profile_picture']
            ))
        return students

    @staticmethod
    def count_all():
        db = Database()
        query = "SELECT COUNT(*) as count FROM students"
        result = db.fetch_one(query)
        return result['count'] if result else 0

    def get_full_name(self):
        if self.middle_initial:
            return f"{self.first_name} {self.middle_initial}. {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    # Completing the get_section_info method that was cut off
    def get_section_info(self):
        query = """
            SELECT s.section_name, st.strand_name, st.strand_code
            FROM sections s
            JOIN strands st ON s.strand_id = st.strand_id
            WHERE s.section_id = %s
        """
        result = self.db.fetch_one(query, (self.section_id,))
        if result:
            return {
                'section_name': result['section_name'],
                'strand_name': result['strand_name'],
                'strand_code': result['strand_code']
            }
        return None