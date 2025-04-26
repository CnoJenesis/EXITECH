import mysql.connector
from mysql.connector import Error as MySQLError
import logging
import time
import os

# Try to import psycopg2 for PostgreSQL
try:
    import psycopg2
    import psycopg2.extras
    from psycopg2 import Error as PostgreSQLError
    POSTGRESQL_AVAILABLE = True
except ImportError:
    POSTGRESQL_AVAILABLE = False
    PostgreSQLError = Exception  # Fallback type

from config import DATABASE_CONFIG

class Database:
    _connection = None
    _last_connection_time = 0
    _reconnect_interval = 60  # seconds

    @classmethod
    def initialize(cls):
        try:
            # Create a copy of the config to modify
            db_config = DATABASE_CONFIG.copy()
            
            # Remove non-connection config items that would cause errors
            for key in ['pg_url', 'ssl_disabled', 'pool_size', 'pool_recycle', 'sslmode', 'port']:
                if key in db_config:
                    db_config.pop(key)
            
            # For cloud database services, we may need to configure SSL
            if 'ssl_ca' in db_config and db_config['ssl_ca']:
                db_config['ssl_verify_cert'] = True
                db_config['ssl_ca'] = db_config['ssl_ca']
            
            print(f"Connecting to MySQL database at {db_config['host']} with user: {db_config['user']}")
            cls._connection = mysql.connector.connect(**db_config)
            cls._last_connection_time = time.time()
            print("Database connection established")
        except MySQLError as e:
            print(f"Error connecting to database: {e}")
            raise e

    @classmethod
    def get_connection(cls):
        try:
            # Check if connection is None or not connected
            if cls._connection is None or not cls._connection.is_connected():
                cls.initialize()
                return cls._connection
            
            # Check if we should refresh the connection
            current_time = time.time()
            if current_time - cls._last_connection_time > cls._reconnect_interval:
                try:
                    # Ping the server to check if connection is still alive
                    cls._connection.ping(reconnect=True, attempts=3, delay=2)
                    cls._last_connection_time = current_time
                except Exception:
                    # If ping fails, reinitialize
                    cls.initialize()
            
            return cls._connection
        except Exception as e:
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
        except Exception as e:
            print(f"Database error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def fetch_all(self, query, params=None):
        cursor = None
        try:
            cursor = self.get_connection().cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Database error in fetch_all: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def execute(self, query, params=None):
        connection = self.get_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            return True
        except Exception as e:
            print(f"Database error in execute: {e}")
            if connection:
                connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def insert(self, query, params=None):
        """Execute an INSERT query and return the last inserted ID"""
        connection = self.get_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Database error in insert: {e}")
            if connection:
                connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def close(self):
        """Close the database connection"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None