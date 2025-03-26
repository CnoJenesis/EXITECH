from models.student import Student
from models.section import Section
from models.strand import Strand
from database.db_connector import Database

def add_student_to_db():
    # Student information
    student_info = {
        'id_number': '23-4474-290',
        'first_name': 'ROSSJERSLEY JOHN',
        'middle_initial': 'G',
        'last_name': 'VILLARICO',
        'grade_level': 12,
        'rfid_uid': '0949993986',
        'profile_picture': None
    }
    
    # Find the STEM strand
    strands = Strand.get_all()
    stem_strand = None
    for strand in strands:
        if strand['strand_code'] == 'STEM':
            stem_strand = strand
            break
    
    if not stem_strand:
        print("STEM strand not found in the database")
        return False
    
    # Find the Integrity section for Grade 12 STEM
    sections = Section.get_all_by_strand_and_grade(stem_strand['strand_id'], 12)
    integrity_section = None
    for section in sections:
        if section['section_name'] == 'Integrity':
            integrity_section = section
            break
    
    if not integrity_section:
        print("Integrity section not found for Grade 12 STEM")
        return False
    
    # Add strand_id and section_id to student info
    student_info['strand_id'] = stem_strand['strand_id']
    student_info['section_id'] = integrity_section['section_id']
    
    # Find the Benevolence section for Grade 12 STEM
    sections = Section.get_all_by_strand_and_grade(stem_strand['strand_id'], 12)
    benevolence_section = None
    for section in sections:
        if section['section_name'] == 'Benevolence':
            benevolence_section = section
            break
    
    if not benevolence_section:
        print("Benevolence section not found for Grade 12 STEM")
        return False
    
    # Add strand_id and section_id to student info
    student_info['strand_id'] = stem_strand['strand_id']
    student_info['section_id'] = benevolence_section['section_id']
    
    # Create student object
    student = Student(
        id_number=student_info['id_number'],
        first_name=student_info['first_name'],
        middle_initial=student_info['middle_initial'],
        last_name=student_info['last_name'],
        grade_level=student_info['grade_level'],
        strand_id=student_info['strand_id'],
        section_id=student_info['section_id'],
        rfid_uid=student_info['rfid_uid'],
        profile_picture=student_info['profile_picture']
    )
    
    # Save student to database
    student_id = student.save()
    
    if student_id:
        print(f"Student added successfully with ID: {student_id}")
        
        # Verify the student can be found by RFID
        db = Database()
        query = "SELECT * FROM students WHERE rfid_uid = %s"
        result = db.fetch_one(query, (student_info['rfid_uid'],))
        db.close()
        
        if result:
            print(f"Verified: Student can be found by RFID UID: {student_info['rfid_uid']}")
        else:
            print(f"WARNING: Student could not be found by RFID UID: {student_info['rfid_uid']}")
            print("This may cause scanning issues.")
        
        return True
    else:
        print("Failed to add student")
        return False

if __name__ == "__main__":
    add_student_to_db()