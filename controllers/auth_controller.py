from flask_login import login_user, logout_user, current_user
from models.admin import Admin

class AuthController:
    @staticmethod
    def login(username, password):
        try:
            print(f"Login attempt for username: {username}")
            admin = Admin.get_by_username(username)
            if admin:
                print(f"Admin found: {admin.username}")
                if admin.verify_password(password):
                    print("Password verified successfully")
                    login_user(admin)
                    return True
                print("Password verification failed")
            else:
                print("Admin not found")
            return False
        except Exception as e:
            print(f"Login error: {e}")
            return False

    @staticmethod
    def logout():
        logout_user()

    @staticmethod
    def get_current_admin():
        try:
            if current_user.is_authenticated:
                return Admin.get_by_id(current_user.get_id())
            return None
        except Exception as e:
            print(f"Get current admin error: {e}")
            return None

    @staticmethod
    def is_authenticated():
        return current_user.is_authenticated