from database.db_connector import Database

class Teacher:
    def __init__(self, id=None, first_name=None, middle_initial=None, last_name=None, email=None):
        self.id = id
        self.first_name = first_name
        self.middle_initial = middle_initial
        self.last_name = last_name
        self.email = email
        self.db = Database()

    def save(self):
        if self.id:
            # Update existing teacher
            query = """
                UPDATE teachers 
                SET first_name = %s, middle_initial = %s, last_name = %s, email = %s
                WHERE teacher_id = %s
            """
            params = (self.first_name, self.middle_initial, self.last_name, self.email, self.id)
            self.db.execute(query, params)
            return self.id
        else:
            # Insert new teacher
            query = """
                INSERT INTO teachers 
                (first_name, middle_initial, last_name, email)
                VALUES (%s, %s, %s, %s)
            """
            params = (self.first_name, self.middle_initial, self.last_name, self.email)
            return self.db.insert(query, params)

    def delete(self):
        if self.id:
            query = "DELETE FROM teachers WHERE teacher_id = %s"
            self.db.execute(query, (self.id,))
            return True
        return False

    @staticmethod
    def get_by_id(teacher_id):
        db = Database()
        query = "SELECT * FROM teachers WHERE teacher_id = %s"
        result = db.fetch_one(query, (teacher_id,))
        if result:
            return Teacher(
                id=result['teacher_id'],
                first_name=result['first_name'],
                middle_initial=result['middle_initial'],
                last_name=result['last_name'],
                email=result['email']
            )
        return None

    @staticmethod
    def get_all():
        db = Database()
        query = "SELECT * FROM teachers ORDER BY last_name, first_name"
        results = db.fetch_all(query)
        teachers = []
        for result in results:
            teachers.append(Teacher(
                id=result['teacher_id'],
                first_name=result['first_name'],
                middle_initial=result['middle_initial'],
                last_name=result['last_name'],
                email=result['email']
            ))
        return teachers

    def get_full_name(self):
        if self.middle_initial:
            return f"{self.first_name} {self.middle_initial}. {self.last_name}"
        return f"{self.first_name} {self.last_name}"