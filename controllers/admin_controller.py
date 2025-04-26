from models.admin import Admin
import hashlib

class AdminController:
    @staticmethod
    def get_admin_by_id(admin_id):
        return Admin.get_by_id(admin_id)
    
    @staticmethod
    def create_admin(username, password, first_name, last_name, middle_initial=None, profile_picture=None):
        """
        Create a new admin
        
        Args:
            username (str): Admin username
            password (str): Admin password
            first_name (str): Admin first name
            last_name (str): Admin last name
            middle_initial (str, optional): Admin middle initial
            profile_picture (str, optional): Admin profile picture
            
        Returns:
            int: Admin ID if successful, None otherwise
        """
        admin = Admin(
            username=username,
            password=password,
            first_name=first_name,
            middle_initial=middle_initial,
            last_name=last_name,
            profile_picture=profile_picture
        )
        return admin.save()
    
    @staticmethod
    def update_admin(admin_id, data):
        admin = Admin.get_by_id(admin_id)
        if not admin:
            return False
        
        admin.username = data.get('username', admin.username)
        admin.first_name = data.get('first_name', admin.first_name)
        admin.middle_initial = data.get('middle_initial', admin.middle_initial)
        admin.last_name = data.get('last_name', admin.last_name)
        
        if 'password' in data:
            admin.password = f"new:{data['password']}"
            
        if 'profile_picture' in data:
            admin.profile_picture = data.get('profile_picture')
            
        return admin.save()
    
    @staticmethod
    def change_password(admin_id, current_password, new_password):
        admin = Admin.get_by_id(admin_id)
        if admin and admin.verify_password(current_password):
            return admin.change_password(new_password)
        return False


def add_admin(username, password, first_name, last_name, middle_initial=None):
    """
    Add a new admin to the system
    
    Args:
        username (str): Admin username
        password (str): Admin password
        first_name (str): Admin first name
        last_name (str): Admin last name
        middle_initial (str, optional): Admin middle initial
        
    Returns:
        int: Admin ID if successful, None otherwise
    """
    # Check if admin with username already exists
    existing_admin = Admin.get_by_username(username)
    
    if existing_admin:
        # Update existing admin
        existing_admin.first_name = first_name
        existing_admin.last_name = last_name
        existing_admin.middle_initial = middle_initial
        
        # Only update password if it's different
        if not existing_admin.verify_password(password):
            existing_admin.password = f"new:{password}"  # Prefix with "new:" to indicate it needs hashing
        
        return existing_admin.save()
    else:
        # Create new admin
        admin = Admin(
            username=username,
            password=password,  # Will be hashed in the save method
            first_name=first_name,
            last_name=last_name,
            middle_initial=middle_initial
        )
        return admin.save()