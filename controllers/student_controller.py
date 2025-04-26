from models.student import Student
from models.section import Section
from models.strand import Strand

class StudentController:
    @staticmethod
    def get_all_students_by_section(section_id):
        return Student.get_all_by_section(section_id)
    
    @staticmethod
    def get_student_by_id(student_id):
        return Student.get_by_id(student_id)
    
    @staticmethod
    def create_student(data, rfid_uid=None):
        student = Student(
            id_number=data.get('id_number'),
            first_name=data.get('first_name'),
            middle_initial=data.get('middle_initial'),
            last_name=data.get('last_name'),
            grade_level=data.get('grade_level'),
            strand_id=data.get('strand_id'),
            section_id=data.get('section_id'),
            rfid_uid=rfid_uid,
            profile_picture=data.get('profile_picture')
        )
        return student.save()
    
    @staticmethod
    def update_student(student_id, data, rfid_uid=None):
        student = Student.get_by_id(student_id)
        if not student:
            return False
        
        student.id_number = data.get('id_number', student.id_number)
        student.first_name = data.get('first_name', student.first_name)
        student.middle_initial = data.get('middle_initial', student.middle_initial)
        student.last_name = data.get('last_name', student.last_name)
        student.grade_level = data.get('grade_level', student.grade_level)
        student.strand_id = data.get('strand_id', student.strand_id)
        student.section_id = data.get('section_id', student.section_id)
        
        if rfid_uid:
            student.rfid_uid = rfid_uid
            
        if 'profile_picture' in data:
            student.profile_picture = data.get('profile_picture')
            
        return student.save()
    
    @staticmethod
    def delete_student(student_id):
        student = Student.get_by_id(student_id)
        if student:
            return student.delete()
        return False
    
    @staticmethod
    def assign_rfid(student_id, rfid_uid):
        student = Student.get_by_id(student_id)
        if student:
            student.rfid_uid = rfid_uid
            return student.save()
        return False
    
    @staticmethod
    def count_students():
        return Student.count_all()