from database.db_connector import Database

class Strand:
    def __init__(self, id=None, name=None, code=None):
        self.id = id
        self.name = name
        self.code = code
        self.db = Database()

    def save(self):
        if self.id:
            # Update existing strand
            query = """
                UPDATE strands 
                SET strand_code = %s, strand_name = %s, description = %s 
                WHERE strand_id = %s
            """
            params = (self.code, self.name, self.description, self.id)
            self.db.execute(query, params)
            return self.id
        else:
            # Insert new strand
            query = """
                INSERT INTO strands (strand_code, strand_name, description)
                VALUES (%s, %s, %s)
            """
            params = (self.code, self.name, self.description)
            return self.db.insert(query, params)

    def delete(self):
        if self.id:
            query = "DELETE FROM strands WHERE strand_id = %s"
            self.db.execute(query, (self.id,))
            return True
        return False

    @staticmethod
    def get_by_id(strand_id):
        db = Database()
        query = "SELECT * FROM strands WHERE strand_id = %s"
        result = db.fetch_one(query, (strand_id,))
        if result:
            return Strand(
                id=result['strand_id'],
                name=result['strand_name'],
                code=result['strand_code']
            )
        return None

    @staticmethod
    def get_all():
        db = Database()
        query = "SELECT * FROM strands ORDER BY strand_name"
        results = db.fetch_all(query)
        
        strands = []
        if results:
            for result in results:
                strands.append({
                    'strand_id': result['strand_id'],
                    'strand_name': result['strand_name'],
                    'strand_code': result['strand_code'],
                    'description': result.get('description', '')
                })
        
        db.close()
        return strands

    @staticmethod
    def get_by_code(code):
        db = Database()
        query = "SELECT * FROM strands WHERE strand_code = %s"
        result = db.fetch_one(query, (code,))
        if result:
            return Strand(
                id=result['strand_id'],
                name=result['strand_name'],
                code=result['strand_code']
            )
        return None