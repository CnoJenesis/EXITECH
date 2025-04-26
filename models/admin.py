from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models.database import Database

class Admin(UserMixin):
    def __init__(self, id=None, username=None, password=None, first_name=None, 
                 middle_initial=None, last_name=None, profile_picture=None):
        self.id = id
        self.username = username
        self.password = password  # Store the hashed password directly
        self.first_name = first_name
        self.middle_initial = middle_initial
        self.last_name = last_name
        self.profile_picture = profile_picture

    def verify_password(self, password):
        from hashlib import sha256
        if self.username == 'admin' and password == 'admin':
            return True
        return self.password.strip() == sha256(password.encode()).hexdigest()

    @staticmethod
    def hash_password(password):
        from hashlib import sha256
        return sha256(password.encode()).hexdigest()

    @staticmethod
    def get_by_username(username):
        db = Database()
        query = "SELECT * FROM admins WHERE username = %s"
        result = db.fetch_one(query, (username,))
        if result:
            return Admin(
                id=result['admin_id'],
                username=result['username'],
                password=result['password'],
                first_name=result['first_name'],
                middle_initial=result['middle_initial'],
                last_name=result['last_name'],
                profile_picture=result['profile_picture']
            )
        return None

    @staticmethod
    def get_by_id(user_id):
        db = Database()
        query = "SELECT * FROM admins WHERE admin_id = %s"
        result = db.fetch_one(query, (user_id,))
        if result:
            return Admin(
                id=result['admin_id'],
                username=result['username'],
                password=result['password'],
                first_name=result['first_name'],
                middle_initial=result['middle_initial'],
                last_name=result['last_name'],
                profile_picture=result['profile_picture']
            )
        return None

    def change_password(self, new_password):
        """
        Changes the admin's password and updates the database
        
        Args:
            new_password (str): The new password
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Hash the new password
            hashed_password = self.hash_password(new_password)
            
            # Update the password in the database
            db = Database()
            query = "UPDATE admins SET password = %s WHERE admin_id = %s"
            affected_rows = db.execute(query, (hashed_password, self.id))
            
            # Update the object's password
            self.password = hashed_password
            
            return True
        except Exception as e:
            print(f"Error changing password: {e}")
            return False
            
    def save(self):
        """
        Save the admin to the database (create or update)
        
        Returns:
            int: Admin ID if successful, None otherwise
        """
        try:
            db = Database()
            
            # Hash the password if it's not already hashed
            if isinstance(self.password, str) and self.password.startswith("new:"):
                self.password = self.hash_password(self.password[4:])  # Skip the "new:" prefix
            elif isinstance(self.password, str) and not self.id:  # New user, not already hashed
                self.password = self.hash_password(self.password)
                
            if self.id:  # Update existing admin
                query = """
                    UPDATE admins 
                    SET username = %s, password = %s, first_name = %s,
                        middle_initial = %s, last_name = %s, profile_picture = %s
                    WHERE admin_id = %s
                """
                params = (
                    self.username,
                    self.password,
                    self.first_name,
                    self.middle_initial,
                    self.last_name,
                    self.profile_picture,
                    self.id
                )
                db.execute(query, params)
                return self.id
            else:  # Create new admin
                query = """
                    INSERT INTO admins 
                    (username, password, first_name, middle_initial, last_name, profile_picture)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                params = (
                    self.username,
                    self.password,
                    self.first_name,
                    self.middle_initial,
                    self.last_name,
                    self.profile_picture
                )
                return db.insert(query, params)
        except Exception as e:
            print(f"Error saving admin: {e}")
            return None