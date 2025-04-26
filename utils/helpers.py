import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

def generate_unique_filename(original_filename):
    """
    Generate a unique filename by adding a UUID and timestamp
    
    Args:
        original_filename (str): The original filename
        
    Returns:
        str: A unique filename
    """
    filename, extension = os.path.splitext(original_filename)
    unique_id = uuid.uuid4().hex
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{secure_filename(filename)}_{timestamp}_{unique_id}{extension}"

def format_time(time_obj):
    """
    Format a time object to a string
    
    Args:
        time_obj (datetime.time): The time object
        
    Returns:
        str: Formatted time string (HH:MM AM/PM)
    """
    if not time_obj:
        return ""
    return time_obj.strftime('%I:%M %p')

def get_day_of_week_number(day_name):
    """
    Convert day name to number (0 = Monday, 6 = Sunday)
    
    Args:
        day_name (str): Day name
        
    Returns:
        int: Day number
    """
    days = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }
    return days.get(day_name, 0)

def get_day_of_week_name(day_number):
    """
    Convert day number to name (0 = Monday, 6 = Sunday)
    
    Args:
        day_number (int): Day number
        
    Returns:
        str: Day name
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if 0 <= day_number < len(days):
        return days[day_number]
    return 'Monday'