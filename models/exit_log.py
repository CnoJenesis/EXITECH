from database.db_connector import Database
from datetime import datetime
import logging

class ExitLog:
    def __init__(self, student_id, exit_time=None, return_time=None, reason=None, destination=None, status="ALLOWED"):
        self.student_id = student_id
        self.exit_time = exit_time
        self.return_time = return_time
        self.reason = reason
        self.destination = destination
        self.status = status

    def save(self):
        if not self.exit_time:
            self.exit_time = datetime.now()

        db = Database()
        try:
            # First check if student exists
            check_query = "SELECT student_id FROM students WHERE student_id = %s"
            student_exists = db.fetch_one(check_query, (self.student_id,))
            
            if not student_exists:
                logger = logging.getLogger(__name__)
                logger.error(f"Cannot save exit log - student ID {self.student_id} does not exist")
                return None
            
            # Insert the exit log
            query = """
                INSERT INTO exit_logs 
                (student_id, timestamp, status, reason, destination) 
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                self.student_id,
                self.exit_time,
                self.status,
                self.reason or "Student Exit",  # Default reason if none provided
                self.destination or "Outside Campus"  # Default destination if none provided
            )
            
            logger = logging.getLogger(__name__)
            logger.info(f"Saving exit log for student {self.student_id} with status {self.status}")
            
            log_id = db.insert(query, params)
            if not log_id:
                logger.error("Failed to log exit - no ID returned")
                return None
                
            logger.info(f"Successfully saved exit log with ID {log_id}")
            return log_id
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error saving exit log: {e}")
            return None
        finally:
            db.close()
        
    @staticmethod
    def get_recent_logs(limit=50):
        db = Database()
        query = """
            SELECT el.*, s.first_name, s.middle_initial, s.last_name, s.id_number,
                   s.grade_level, s.profile_picture, sec.section_name
            FROM exit_logs el
            JOIN students s ON el.student_id = s.student_id
            LEFT JOIN sections sec ON s.section_id = sec.section_id
            ORDER BY el.timestamp DESC
            LIMIT %s
        """
        return db.fetch_all(query, (limit,))
        
    @staticmethod
    def clear_all_logs():
        """Clear all exit logs from the database"""
        db = Database()
        query = "DELETE FROM exit_logs"
        try:
            result = db.execute(query)
            return result
        except Exception as e:
            print(f"Error clearing exit logs: {e}")
            return False