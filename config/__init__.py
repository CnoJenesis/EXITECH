# This file makes the config directory a Python package

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'October14?',
    'database': 'exitech',
    'auth_plugin': 'mysql_native_password',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'raise_on_warnings': True
}

# Application configuration
APP_CONFIG = {
    'debug': True,
    'secret_key': 'exitech_secret_key_change_in_production',
    'upload_folder': 'static/uploads',
    'allowed_extensions': {'png', 'jpg', 'jpeg', 'gif'}
}

# RFID Reader configuration
RFID_CONFIG = {
    'enabled': True,
    'simulation_mode': True  # Set to False in production with real hardware
}