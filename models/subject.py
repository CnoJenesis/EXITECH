from database.db_connector import Database

class Subject:
    def __init__(self, id=None, code=None, name=None):
        self.id = id
        self.code = code
        self.name = name
        self.db = Database()

    def save(self):
        if self.id:
            # Update existing subject
            query = """
                UPDATE subjects 
                SET subject_code = %s, subject_name = %s
                WHERE subject_id = %s
            """
            params = (self.code, self.name, self.id)
            self.db.execute(query, params)
            return self.id
        else:
            # Insert new subject
            query = """
                INSERT INTO subjects 
                (subject_code, subject_name)
                VALUES (%s, %s)
            """
            params = (self.code, self.name)
            return self.db.insert(query, params)

    def delete(self):
        if self.id:
            query = "DELETE FROM subjects WHERE subject_id = %s"
            self.db.execute(query, (self.id,))
            return True
        return False

    @staticmethod
    def get_by_id(subject_id):
        db = Database()
        query = "SELECT * FROM subjects WHERE subject_id = %s"
        result = db.fetch_one(query, (subject_id,))
        if result:
            return Subject(
                id=result['subject_id'],
                code=result['subject_code'],
                name=result['subject_name']
            )
        return None

    @staticmethod
    def get_all():
        db = Database()
        query = "SELECT * FROM subjects ORDER BY subject_code"
        results = db.fetch_all(query)
        subjects = []
        for result in results:
            subjects.append(Subject(
                id=result['subject_id'],
                code=result['subject_code'],
                name=result['subject_name']
            ))
        return subjects

    @staticmethod
    def get_by_code(code):
        db = Database()
        query = "SELECT * FROM subjects WHERE subject_code = %s"
        result = db.fetch_one(query, (code,))
        if result:
            return Subject(
                id=result['subject_id'],
                code=result['subject_code'],
                name=result['subject_name']
            )
        return None