import requests
import os
from datetime import datetime
import logging
from config.teams_webhook import TEAMS_WEBHOOK_URL, TEAMS_WEBHOOK_ENABLED
import json

logger = logging.getLogger(__name__)

def send_denied_exit_notification(student_data, reason, class_info=None):
    """Send a notification to MS Teams when a student's exit is denied."""
    try:
        # Check if Teams notifications are enabled
        if not TEAMS_WEBHOOK_ENABLED:
            logger.info("Teams webhook notifications are disabled")
            return
            
        # Use webhook URL from config file
        webhook_url = TEAMS_WEBHOOK_URL
        
        # Print debug info
        print(f"\n=== TEAMS NOTIFICATION ===")
        print(f"Webhook URL: {'Set' if webhook_url else 'Not set'}")
        print(f"Student: {student_data.get('id_number', 'Unknown')}")
        print(f"Reason: {reason}")
        print(f"Class info: {class_info}")
            
        # Get current time
        current_time = datetime.now()
        
        # Format the date and time
        day_of_week = current_time.strftime('%A')  # Full day name
        formatted_date = current_time.strftime('%B %d, %Y')  # March 25, 2025
        formatted_time = current_time.strftime('%I:%M %p')  # 4:11 PM
        
        # Format class schedule if available
        class_schedule = ""
        if class_info:
            # Format the class times properly
            start_time = class_info.get('time_start')
            end_time = class_info.get('time_end')
            
            # Print the time values that we received
            print(f"Received time_start: {start_time} ({type(start_time)})")
            print(f"Received time_end: {end_time} ({type(end_time)})")
            
            # Helper function to format time consistently
            def format_time_to_12hr(time_value):
                import datetime as dt
                
                # Handle timedelta objects
                if isinstance(time_value, dt.timedelta):
                    print(f"Converting timedelta: {time_value}")
                    # Convert timedelta to hours and minutes
                    total_seconds = int(time_value.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    
                    # Convert to 12-hour format
                    period = "A.M." if hours < 12 else "P.M."
                    hour_12 = hours % 12
                    if hour_12 == 0:
                        hour_12 = 12
                    
                    return f"{hour_12}:{minutes:02d} {period}"
                
                # Try to parse from string (HH:MM:SS format)
                if isinstance(time_value, str):
                    if (' A.M.' in time_value or ' P.M.' in time_value):
                        # Already properly formatted
                        return time_value
                    
                    try:
                        if ':' in time_value:
                            parts = time_value.split(':')
                            if len(parts) >= 2:
                                hour = int(parts[0])
                                minute = int(parts[1])
                                
                                # Convert to 12-hour format with A.M./P.M.
                                period = "A.M." if hour < 12 else "P.M."
                                hour_12 = hour % 12
                                if hour_12 == 0:
                                    hour_12 = 12
                                    
                                return f"{hour_12}:{minute:02d} {period}"
                    except Exception as e:
                        print(f"Error parsing time string: {e}")
                
                # Try to handle as datetime object
                elif hasattr(time_value, 'hour') and hasattr(time_value, 'minute'):
                    try:
                        hour = time_value.hour
                        minute = time_value.minute
                        period = "A.M." if hour < 12 else "P.M."
                        hour_12 = hour % 12
                        if hour_12 == 0:
                            hour_12 = 12
                        return f"{hour_12}:{minute:02d} {period}"
                    except Exception as e:
                        print(f"Error formatting datetime: {e}")
                
                # Fallback to string representation
                return str(time_value)
            
            # Format the times using the helper function
            print(f"Converting time_start: {start_time} ({type(start_time).__name__})")
            formatted_start = format_time_to_12hr(start_time)
            print(f"Converting time_end: {end_time} ({type(end_time).__name__})")
            formatted_end = format_time_to_12hr(end_time)
            
            print(f"Final formatted start time: {formatted_start}")
            print(f"Final formatted end time: {formatted_end}")
            
            class_schedule = (
                f"Current Class: {class_info.get('subject_name', 'Unknown')}\n"
                f"Teacher: {class_info.get('teacher_name', 'Unknown')}\n"
                f"Schedule: {day_of_week} {formatted_start} - {formatted_end}"
            )
            
        # Create the MessageCard
        card = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "FF0000",
            "summary": "Student Exit Denied",
            "sections": [{
                "activityTitle": "🚫 Student Exit Denied",
                "activitySubtitle": f"Exit denied at {day_of_week} {formatted_date} {formatted_time}",
                "facts": [
                    {
                        "name": "Current Class",
                        "value": class_info.get('subject_name', 'Unknown') if class_info else 'None'
                    },
                    {
                        "name": "Teacher",
                        "value": class_info.get('teacher_name', 'Unknown') if class_info else 'None'
                    },
                    {
                        "name": "Schedule",
                        "value": f"{formatted_start} - {formatted_end}" if class_info else 'None'
                    },
                    {
                        "name": "Student Name",
                        "value": student_data.get('first_name', '') + ' ' + 
                                (student_data.get('middle_initial', '') + '. ' if student_data.get('middle_initial') else '') + 
                                student_data.get('last_name', '')
                    },
                    {
                        "name": "ID Number",
                        "value": student_data.get('id_number', 'Unknown')
                    },
                    {
                        "name": "Grade & Section",
                        "value": f"{student_data.get('strand_code', '')} {student_data.get('grade_level', '')} - {student_data.get('section', 'Unknown')}"
                    },
                    {
                        "name": "Reason Denied",
                        "value": reason
                    }
                ]
            }]
        }
        
        # Print the request we're about to send
        print(f"Sending request to Teams webhook URL")
        print(f"Request payload: {json.dumps(card, indent=2)[:200]}...")
        
        # Send the notification
        response = requests.post(
            webhook_url, 
            json=card,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text[:100]}")
        
        response.raise_for_status()
        logger.info(f"Teams notification sent successfully for student {student_data.get('id_number', 'Unknown')}")
        print(f"✅ Teams notification sent successfully")
        
    except Exception as e:
        logger.error(f"Failed to send Teams notification: {str(e)}")
        print(f"❌ Error sending Teams notification: {str(e)}") 