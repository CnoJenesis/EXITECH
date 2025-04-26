# Database configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'exitech',
    'user': 'root',
    'password': '',  # Empty password for local development
    'port': 3306
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