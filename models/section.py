from database.db_connector import Database

class Section:
    def __init__(self, id=None, name=None, grade_level=None, strand_id=None):
        self.id = id
        self.name = name
        self.grade_level = grade_level
        self.strand_id = strand_id
        self.db = Database()

    def save(self):
        if self.id:
            # Update existing section
            query = """
                UPDATE sections 
                SET section_name = %s, strand_id = %s, grade_level = %s 
                WHERE section_id = %s
            """
            params = (self.name, self.strand_id, self.grade_level, self.id)
            self.db.execute(query, params)
            return self.id
        else:
            # Insert new section
            query = """
                INSERT INTO sections (section_name, strand_id, grade_level)
                VALUES (%s, %s, %s)
            """
            params = (self.name, self.strand_id, self.grade_level)
            return self.db.insert(query, params)

    def delete(self):
        if self.id:
            query = "DELETE FROM sections WHERE section_id = %s"
            self.db.execute(query, (self.id,))
            return True
        return False

    @staticmethod
    def get_by_id(section_id):
        db = Database()
        query = "SELECT * FROM sections WHERE section_id = %s"
        result = db.fetch_one(query, (section_id,))
        if result:
            return Section(
                id=result['section_id'],
                name=result['section_name'],
                grade_level=result['grade_level'],
                strand_id=result['strand_id']
            )
        return None

    @staticmethod
    def get_all_by_strand_and_grade(strand_id, grade_level):
        db = Database()
        
        print(f"Looking for sections with strand_id={strand_id}, grade_level={grade_level}")
        
        # Extract just the numeric grade if the grade_level is in format "Grade XX"
        if grade_level and isinstance(grade_level, str) and grade_level.startswith('Grade '):
            try:
                grade_number = grade_level.replace('Grade ', '')
                print(f"Extracted grade number: {grade_number}")
                query = """
                    SELECT * FROM sections 
                    WHERE strand_id = %s AND grade_level = %s
                    ORDER BY section_name
                """
                results = db.fetch_all(query, (strand_id, int(grade_number)))
            except Exception as e:
                print(f"Error in get_all_by_strand_and_grade: {e}")
                results = []
        else:
            # If grade_level is not in expected format, try to use it directly
            print("Using grade_level as-is")
            query = """
                SELECT * FROM sections 
                WHERE strand_id = %s AND grade_level = %s
                ORDER BY section_name
            """
            results = db.fetch_all(query, (strand_id, grade_level))
        
        print(f"Query results: {results}")
        
        sections = []
        if results:
            for result in results:
                sections.append({
                    'section_id': result['section_id'],
                    'section_name': result['section_name'],
                    'grade_level': result['grade_level'],
                    'strand_id': result['strand_id']
                })
        
        print(f"Returning {len(sections)} sections")
        db.close()
        return sections

    @staticmethod
    def get_all():
        db = Database()
        query = """
            SELECT s.*, st.strand_code, st.strand_name 
            FROM sections s
            JOIN strands st ON s.strand_id = st.strand_id
            ORDER BY s.grade_level, s.section_name
        """
        results = db.fetch_all(query)
        
        sections = []
        if results:
            for result in results:
                sections.append({
                    'section_id': result['section_id'],
                    'section_name': result['section_name'],
                    'grade_level': result['grade_level'],
                    'strand_id': result['strand_id'],
                    'strand_code': result['strand_code'],
                    'strand_name': result['strand_name']
                })
        
        db.close()
        return sections

    @staticmethod
    def count_all():
        db = Database()
        query = "SELECT COUNT(*) as count FROM sections"
        result = db.fetch_one(query)
        return result['count'] if result else 0

    def get_strand_info(self):
        query = "SELECT * FROM strands WHERE strand_id = %s"
        result = self.db.fetch_one(query, (self.strand_id,))
        if result:
            return {
                'strand_id': result['strand_id'],
                'strand_name': result['strand_name'],
                'strand_code': result['strand_code']
            }
        return None