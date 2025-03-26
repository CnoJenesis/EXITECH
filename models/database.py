import mysql.connector
from mysql.connector import Error
from config import DATABASE_CONFIG
import logging

class Database:
    _connection = None

    @classmethod
    def initialize(cls):
        try:
            print(f"Connecting with user: {DATABASE_CONFIG['user']}")
            cls._connection = mysql.connector.connect(**DATABASE_CONFIG)
            print("Database connection established")
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise e

    @classmethod
    def get_connection(cls):
        try:
            if cls._connection is None or not cls._connection.is_connected():
                cls.initialize()
            return cls._connection
        except Error as e:
            print(f"Error getting connection: {e}")
            raise e

    def fetch_one(self, query, params=None):
        cursor = None
        try:
            cursor = self.get_connection().cursor(dictionary=True)
            print(f"Executing query: {query}")
            print(f"With parameters: {params}")
            cursor.execute(query, params)
            result = cursor.fetchone()
            print(f"Query result: {result}")
            return result
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def fetch_all(self, query, params=None):
        cursor = self.get_connection().cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()

    def execute(self, query, params=None):
        connection = self.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            connection.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def insert(self, query, params=None):
        """Execute an INSERT query and return the last inserted ID"""
        return self.execute(query, params)

    def close(self):
        """Close the database connection"""
        if self._connection and self._connection.is_connected():
            self._connection.close()