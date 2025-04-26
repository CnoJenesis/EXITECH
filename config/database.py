import os
import re

# Parse database URL if provided
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:Satsatfamily1962!@db.kmjhaapjzygmrdunrjwf.supabase.co:5432/postgres')

# For local development or if psycopg2 is not available, use MySQL
# The PostgreSQL URL will be used in production environments
DATABASE_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', 'October14?'),
    'database': os.environ.get('MYSQL_DB', 'exitech'),
    'auth_plugin': 'mysql_native_password',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'raise_on_warnings': True,
    'ssl_disabled': os.environ.get('MYSQL_SSL_DISABLED', 'True').lower() == 'true',
    'ssl_ca': os.environ.get('MYSQL_SSL_CA', None),
    'pool_size': int(os.environ.get('MYSQL_POOL_SIZE', 5)),
    'pool_recycle': int(os.environ.get('MYSQL_POOL_RECYCLE', 3600))
}

# Store the Postgres URL for Vercel deployment
DATABASE_CONFIG['pg_url'] = DATABASE_URL

print(f"Database configured for local MySQL. PostgreSQL URL stored for production deployment.")