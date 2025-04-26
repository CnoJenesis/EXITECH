"""
PostgreSQL adapter for Vercel deployment using pg8000.

This file will be used in production on Vercel to connect to PostgreSQL
instead of MySQL. Place it in the root directory of your project.
"""

import os
import re
import pg8000

# PostgreSQL adapter for Vercel deployment
class VercelPostgresAdapter:
    """Adapter for PostgreSQL on Vercel deployment environment using pg8000"""
    
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
            
            # Connect to PostgreSQL using pg8000
            cls._connection = pg8000.connect(
                user=db_config['user'],
                password=db_config['password'],
                host=db_config['host'],
                port=int(db_config['port']),
                database=db_config['database']
            )
            
            print("PostgreSQL connection established")
        
        # Override Database.initialize with our PostgreSQL version
        Database.initialize = pg_initialize
        
        # Also override get_connection to check connection properly
        original_get_connection = Database.get_connection
        
        @classmethod
        def pg_get_connection(cls):
            try:
                if cls._connection is None:
                    cls.initialize()
                # pg8000 doesn't have a simple is_connected() method, so we'll test with a simple query
                try:
                    cursor = cls._connection.cursor()
                    cursor.execute("SELECT 1")
                    cursor.close()
                except Exception:
                    # If query fails, reinitialize
                    cls.initialize()
                return cls._connection
            except Exception as e:
                print(f"Error getting PostgreSQL connection: {e}")
                cls.initialize()
                return cls._connection
        
        Database.get_connection = pg_get_connection
        
        # Override fetch_one to work with pg8000
        original_fetch_one = Database.fetch_one
        
        def pg_fetch_one(self, query, params=None):
            connection = self.get_connection()
            cursor = None
            try:
                cursor = connection.cursor()
                print(f"Executing PG query: {query}")
                print(f"With parameters: {params}")
                
                # Execute the query
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # Fetch column names
                column_names = [desc[0] for desc in cursor.description] if cursor.description else []
                
                # Fetch the row
                row = cursor.fetchone()
                
                # No results
                if not row:
                    return None
                
                # Convert to dict
                result = {column_names[i]: row[i] for i in range(len(column_names))}
                print(f"Query result: {result}")
                return result
            except Exception as e:
                print(f"PostgreSQL error in fetch_one: {e}")
                return None
            finally:
                if cursor:
                    cursor.close()
        
        Database.fetch_one = pg_fetch_one
        
        # Override fetch_all to work with pg8000
        original_fetch_all = Database.fetch_all
        
        def pg_fetch_all(self, query, params=None):
            connection = self.get_connection()
            cursor = None
            try:
                cursor = connection.cursor()
                
                # Execute the query
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # Fetch column names
                column_names = [desc[0] for desc in cursor.description] if cursor.description else []
                
                # Fetch all rows
                rows = cursor.fetchall()
                
                # Convert to list of dicts
                result = []
                for row in rows:
                    row_dict = {column_names[i]: row[i] for i in range(len(column_names))}
                    result.append(row_dict)
                
                return result
            except Exception as e:
                print(f"PostgreSQL error in fetch_all: {e}")
                return []
            finally:
                if cursor:
                    cursor.close()
        
        Database.fetch_all = pg_fetch_all
        
        # Override execute to work with pg8000
        original_execute = Database.execute
        
        def pg_execute(self, query, params=None):
            connection = self.get_connection()
            cursor = None
            try:
                cursor = connection.cursor()
                
                # Execute the query
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                connection.commit()
                return True
            except Exception as e:
                print(f"PostgreSQL error in execute: {e}")
                if connection:
                    connection.rollback()
                return False
            finally:
                if cursor:
                    cursor.close()
        
        Database.execute = pg_execute
        
        # Override insert to work with pg8000
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
                
                # Execute the query
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # Get the ID from RETURNING clause
                result = cursor.fetchone()
                
                connection.commit()
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
            if self._connection:
                self._connection.close()
                self._connection = None
        
        Database.close = pg_close
        
        print("PostgreSQL adapter setup complete")
        
        return True 