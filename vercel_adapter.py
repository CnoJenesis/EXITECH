"""
PostgreSQL adapter for Vercel deployment.

This file will be used in production on Vercel to connect to PostgreSQL
instead of MySQL. Place it in the root directory of your project.

IMPORTANT: Install psycopg2-binary in your Vercel environment:
- Make sure to include "psycopg2-binary" in your requirements.txt file
"""

import os
import psycopg2
import psycopg2.extras
import re

# PostgreSQL adapter for Vercel deployment
class VercelPostgresAdapter:
    """Adapter for PostgreSQL on Vercel deployment environment"""
    
    @staticmethod
    def setup():
        """
        Sets up environment for PostgreSQL by monkey patching the Database class.
        Call this function in api/index.py before importing app.
        """
        from models.database import Database
        
        # Store the original initialize method
        original_initialize = Database.initialize
        
        # Define our new initialize method that uses PostgreSQL
        @classmethod
        def pg_initialize(cls):
            from config import DATABASE_CONFIG
            
            # Get PostgreSQL URL from DATABASE_CONFIG or environment
            pg_url = DATABASE_CONFIG.get('pg_url') or os.environ.get('DATABASE_URL')
            
            if not pg_url:
                raise ValueError("No PostgreSQL URL found. Set DATABASE_URL environment variable.")
            
            # Parse the connection string
            match = re.match(r'postgresql://(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)/(?P<database>.+)', pg_url)
            if not match:
                raise ValueError(f"Invalid PostgreSQL URL format: {pg_url}")
            
            db_config = match.groupdict()
            
            print(f"Connecting to PostgreSQL at {db_config['host']} with user: {db_config['user']}")
            
            # Connect to PostgreSQL
            cls._connection = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database'],
                sslmode='require'
            )
            
            print("PostgreSQL connection established")
        
        # Override Database.initialize with our PostgreSQL version
        Database.initialize = pg_initialize
        
        # Also override get_connection to check connection properly
        original_get_connection = Database.get_connection
        
        @classmethod
        def pg_get_connection(cls):
            try:
                if cls._connection is None or cls._connection.closed:
                    cls.initialize()
                return cls._connection
            except Exception as e:
                print(f"Error getting PostgreSQL connection: {e}")
                cls.initialize()
                return cls._connection
        
        Database.get_connection = pg_get_connection
        
        # Override fetch_one to work with PostgreSQL
        original_fetch_one = Database.fetch_one
        
        def pg_fetch_one(self, query, params=None):
            cursor = None
            try:
                connection = self.get_connection()
                cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(query, params)
                result = cursor.fetchone()
                
                # Convert result to dict if it exists
                if result:
                    return dict(result)
                return None
            except Exception as e:
                print(f"PostgreSQL error in fetch_one: {e}")
                return None
            finally:
                if cursor:
                    cursor.close()
        
        Database.fetch_one = pg_fetch_one
        
        # Override fetch_all to work with PostgreSQL
        original_fetch_all = Database.fetch_all
        
        def pg_fetch_all(self, query, params=None):
            cursor = None
            try:
                connection = self.get_connection()
                cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute(query, params)
                results = cursor.fetchall()
                
                # Convert results to dict
                return [dict(row) for row in results]
            except Exception as e:
                print(f"PostgreSQL error in fetch_all: {e}")
                return []
            finally:
                if cursor:
                    cursor.close()
        
        Database.fetch_all = pg_fetch_all
        
        # Override insert to work with PostgreSQL
        original_insert = Database.insert
        
        def pg_insert(self, query, params=None):
            """Execute an INSERT query and return the last inserted ID"""
            connection = self.get_connection()
            cursor = None
            try:
                # Make sure query returns the ID
                if "RETURNING" not in query.upper():
                    # Add RETURNING id to the query
                    query = query.rstrip(';')
                    query += " RETURNING id;"
                
                cursor = connection.cursor()
                cursor.execute(query, params)
                result = cursor.fetchone()
                connection.commit()
                
                # Return the ID from RETURNING clause
                return result[0] if result else None
            except Exception as e:
                print(f"PostgreSQL error in insert: {e}")
                if connection:
                    connection.rollback()
                return None
            finally:
                if cursor:
                    cursor.close()
        
        Database.insert = pg_insert
        
        # Also override close method
        original_close = Database.close
        
        def pg_close(self):
            if self._connection and not self._connection.closed:
                self._connection.close()
                self._connection = None
        
        Database.close = pg_close
        
        print("PostgreSQL adapter setup complete")
        
        return True 