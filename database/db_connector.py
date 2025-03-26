import mysql.connector
from mysql.connector import Error
import logging
import os
from config import DATABASE_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Database:
    """
    Database connector class for MySQL database operations
    """
    
    def __init__(self):
        """Initialize database connection"""
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish connection to the database"""
        try:
            self.connection = mysql.connector.connect(**DATABASE_CONFIG)
            logger.info("Database connection established")
        except Error as e:
            logger.error(f"Error connecting to MySQL database: {e}")
    
    def execute_query(self, query, params=None):
        """
        Execute a query without returning results
        
        Args:
            query (str): SQL query
            params (tuple, optional): Query parameters
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connection or not self.connection.is_connected():
            self.connect()
            if not self.connection or not self.connection.is_connected():
                return False
        
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            return True
        except Error as e:
            logger.error(f"Error executing query: {e}")
            return False
        finally:
            cursor.close()
    
    def fetch_all(self, query, params=None):
        """
        Execute a query and fetch all results
        
        Args:
            query (str): SQL query
            params (tuple, optional): Query parameters
            
        Returns:
            list: List of dictionaries containing the results
        """
        if not self.connection or not self.connection.is_connected():
            self.connect()
            if not self.connection or not self.connection.is_connected():
                return []
        
        cursor = self.connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            return cursor.fetchall()
        except Error as e:
            logger.error(f"Error fetching data: {e}")
            return []
        finally:
            cursor.close()
    
    def fetch_one(self, query, params=None):
        """
        Execute a query and fetch one result
        
        Args:
            query (str): SQL query
            params (tuple, optional): Query parameters
            
        Returns:
            dict: Dictionary containing the result or None
        """
        if not self.connection or not self.connection.is_connected():
            self.connect()
            if not self.connection or not self.connection.is_connected():
                return None
        
        cursor = self.connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            return cursor.fetchone()
        except Error as e:
            logger.error(f"Error fetching data: {e}")
            return None
        finally:
            cursor.close()
    
    def insert(self, query, params=None):
        """
        Insert data and return the last inserted ID
        
        Args:
            query (str): SQL query
            params (tuple, optional): Query parameters
            
        Returns:
            int: Last inserted ID or None
        """
        if not self.connection or not self.connection.is_connected():
            self.connect()
            if not self.connection or not self.connection.is_connected():
                return None
        
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            logger.error(f"Error inserting data: {e}")
            return None
        finally:
            cursor.close()
    
    def close(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")