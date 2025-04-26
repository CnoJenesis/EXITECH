from models.student import Student
from models.class_schedule import ClassSchedule
from models.exit_log import ExitLog
from datetime import datetime
from database.db_connector import Database
import logging
import os
from utils.teams_notification import send_denied_exit_notification
from threading import Thread

logger = logging.getLogger(__name__)

class ExitController:
    @staticmethod
    def process_exit_request(rfid_uid):
        try:
            if not rfid_uid:
                return {'status': 'error', 'message': 'Invalid RFID'}
            
            rfid_uid = str(rfid_uid).strip()
            db = Database()
            
            # Debug log
            logger.info(f"Processing exit request for RFID: {rfid_uid}")
            
            # Find student with matching RFID
            student_query = """
            SELECT s.student_id, s.first_name, s.middle_initial, s.last_name, 
                   s.id_number, s.grade_level, s.section_id, 
                   CASE 
                       WHEN s.profile_picture IS NULL OR s.profile_picture = ''
                       THEN '/static/img/default-profile.png'
                       ELSE CONCAT('/static/uploads/students/', s.profile_picture)
                   END as profile_picture_path
            FROM students s
            WHERE s.rfid_uid = %s
            LIMIT 1
            """
            
            student = db.fetch_one(student_query, (rfid_uid,))
            
            if not student:
                logger.warning(f"No student found with RFID: {rfid_uid}")
                return {
                    'status': 'error', 
                    'message': "No student found with this RFID card.",
                    'student': {
                        'first_name': 'Unknown',
                        'last_name': 'Student',
                        'id_number': rfid_uid,
                        'exit_status': 'DENIED',
                        'reason': "RFID not registered in the system"
                    }
                }
            
            # Get the section details
            section_query = """
            SELECT sec.section_name, IFNULL(str.strand_code, '') as strand_code
            FROM sections sec
            LEFT JOIN strands str ON sec.strand_id = str.strand_id
            WHERE sec.section_id = %s
            """
            
            section_result = db.fetch_one(section_query, (student['section_id'],))
            
            if not section_result:
                section_result = {'section_name': 'Unknown Section', 'strand_code': ''}
                logger.warning(f"No section found for student: {student['student_id']}")
            
            # Check for recent exits from this student to prevent duplicates
            recent_exit_query = """
            SELECT log_id, timestamp, status 
            FROM exit_logs 
            WHERE student_id = %s 
            ORDER BY timestamp DESC 
            LIMIT 1
            """
            
            recent_exit = db.fetch_one(recent_exit_query, (student['student_id'],))
            
            # If there's a recent exit in the last 10 seconds, just return it instead of creating a new one
            if recent_exit:
                current_time = datetime.now()
                exit_time = recent_exit['timestamp']
                time_diff = (current_time - exit_time).total_seconds()
                
                if time_diff < 10:  # Less than 10 seconds ago
                    logger.info(f"Returning recent exit for student {student['id_number']} from {time_diff:.1f} seconds ago")
                    
                    # Format the response with the existing exit data
                    return {
                        'status': 'success',
                        'log_id': recent_exit['log_id'],
                        'student': {
                            'first_name': student['first_name'] or '',
                            'middle_initial': student['middle_initial'] or '',
                            'last_name': student['last_name'] or '',
                            'id_number': student['id_number'] or '',
                            'grade_level': student['grade_level'] or '',
                            'section': section_result['section_name'],
                            'strand_code': section_result['strand_code'],
                            'profile_picture': student['profile_picture_path'],
                            'exit_time': exit_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'exit_status': recent_exit['status'],
                            'reason': "Previously scanned"
                        }
                    }
            
            # Check for active exit restriction
            restriction_query = """
            SELECT er.restriction_id, er.reason
            FROM exit_restrictions er
            WHERE er.student_id = %s AND er.is_active = 1
            LIMIT 1
            """
            
            restriction = db.fetch_one(restriction_query, (student['student_id'],))
            
            current_time = datetime.now()
            exit_status = 'ALLOWED'
            reason = ''
            class_info = None
            
            if restriction:
                exit_status = 'DENIED'
                reason = restriction['reason'] or 'No exit permission'
                logger.warning(f"Exit denied for student {student['id_number']} - Reason: {reason}")
            
            # If no restrictions, check if student has a class currently in progress
            if exit_status == 'ALLOWED':
                # Debug information
                print(f"Checking if student {student['student_id']} (ID: {student['id_number']}) from section {student['section_id']} has class now")
                
                # Get time and day information for debugging
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                current_day = datetime.now().weekday()
                current_day_name = days[current_day]
                current_time_obj = datetime.now().time()
                print(f"Current day: {current_day_name}, Current time: {current_time_obj}")
                
                # Check if student has a class right now
                direct_class_check_query = """
                SELECT cs.schedule_id, s.subject_name, cs.time_start, cs.time_end, 
                       t.first_name as teacher_first_name, t.middle_initial as teacher_middle_initial, 
                       t.last_name as teacher_last_name
                FROM class_schedules cs 
                JOIN subjects s ON cs.subject_id = s.subject_id
                JOIN teachers t ON cs.teacher_id = t.teacher_id
                WHERE cs.section_id = %s
                AND cs.day_of_week = %s
                AND cs.time_start <= %s AND cs.time_end >= %s
                LIMIT 1
                """
                class_check = db.fetch_one(direct_class_check_query, (
                    student['section_id'], 
                    current_day_name, 
                    current_time_obj, 
                    current_time_obj
                ))
                
                if class_check:
                    print(f"DIRECT DB CHECK: Student {student['id_number']} has class {class_check['subject_name']} from {class_check['time_start']} to {class_check['time_end']}")
                    
                    # Check if the class is about to end (within 5 minutes)
                    if hasattr(class_check['time_end'], 'timestamp'):
                        class_end_time = class_check['time_end']
                        time_until_end = (class_end_time.hour * 60 + class_end_time.minute) - (current_time_obj.hour * 60 + current_time_obj.minute)
                        print(f"Minutes until class ends: {time_until_end}")
                        
                        # If class ends in 5 minutes or less, allow the exit
                        if time_until_end <= 5:
                            print(f"Class is about to end in {time_until_end} minutes, allowing exit")
                            exit_status = 'ALLOWED'
                            reason = f"Class ending soon: {class_check['subject_name']}"
                            logger.info(f"Exit allowed for student {student['id_number']} - Reason: {reason}")
                        else:
                            exit_status = 'DENIED'
                            
                            # Format teacher name
                            teacher_name = f"{class_check['teacher_first_name']} "
                            if class_check['teacher_middle_initial']:
                                teacher_name += f"{class_check['teacher_middle_initial']}. "
                            teacher_name += class_check['teacher_last_name']
                            teacher_name = teacher_name.strip()
                            
                            # Format class times before storing
                            formatted_start = class_check['time_start']
                            formatted_end = class_check['time_end']
                            
                            # Convert time_start to formatted string
                            if hasattr(formatted_start, 'hour') and hasattr(formatted_start, 'minute'):
                                hour = formatted_start.hour
                                minute = formatted_start.minute
                                period = "A.M." if hour < 12 else "P.M."
                                hour_12 = hour % 12
                                if hour_12 == 0:
                                    hour_12 = 12
                                formatted_start = f"{hour_12}:{minute:02d} {period}"
                                
                            # Convert time_end to formatted string
                            if hasattr(formatted_end, 'hour') and hasattr(formatted_end, 'minute'):
                                hour = formatted_end.hour
                                minute = formatted_end.minute
                                period = "A.M." if hour < 12 else "P.M."
                                hour_12 = hour % 12
                                if hour_12 == 0:
                                    hour_12 = 12
                                formatted_end = f"{hour_12}:{minute:02d} {period}"
                            
                            # Store class info for MS Teams notification
                            class_info = {
                                'subject_name': class_check['subject_name'],
                                'teacher_name': teacher_name,
                                'time_start': formatted_start,
                                'time_end': formatted_end
                            }
                            
                            # Print debug info about time formats
                            print(f"\n=== CLASS TIME DEBUGGING ===")
                            print(f"time_start type: {type(class_check['time_start'])}")
                            print(f"time_start value: {class_check['time_start']}")
                            print(f"time_end type: {type(class_check['time_end'])}")
                            print(f"time_end value: {class_check['time_end']}")
                            
                            # Try to convert to string in the correct format before sending
                            if hasattr(class_check['time_start'], 'strftime'):
                                hour = class_check['time_start'].hour
                                minute = class_check['time_start'].minute
                            reason = f"Class in progress: {class_check['subject_name']}"
                            logger.warning(f"Exit denied for student {student['id_number']} - Reason: {reason}")
                    else:
                        exit_status = 'DENIED'
                        
                        # Format teacher name
                        teacher_name = f"{class_check['teacher_first_name']} "
                        if class_check['teacher_middle_initial']:
                            teacher_name += f"{class_check['teacher_middle_initial']}. "
                        teacher_name += class_check['teacher_last_name']
                        teacher_name = teacher_name.strip()
                        
                        # Format class times before storing
                        formatted_start = class_check['time_start']
                        formatted_end = class_check['time_end']
                        
                        # Convert time_start to formatted string
                        if hasattr(formatted_start, 'hour') and hasattr(formatted_start, 'minute'):
                            hour = formatted_start.hour
                            minute = formatted_start.minute
                            period = "A.M." if hour < 12 else "P.M."
                            hour_12 = hour % 12
                            if hour_12 == 0:
                                hour_12 = 12
                            formatted_start = f"{hour_12}:{minute:02d} {period}"
                            
                        # Convert time_end to formatted string
                        if hasattr(formatted_end, 'hour') and hasattr(formatted_end, 'minute'):
                            hour = formatted_end.hour
                            minute = formatted_end.minute
                            period = "A.M." if hour < 12 else "P.M."
                            hour_12 = hour % 12
                            if hour_12 == 0:
                                hour_12 = 12
                            formatted_end = f"{hour_12}:{minute:02d} {period}"
                        
                        # Store class info for MS Teams notification
                        class_info = {
                            'subject_name': class_check['subject_name'],
                            'teacher_name': teacher_name,
                            'time_start': formatted_start,
                            'time_end': formatted_end
                        }
                        
                        reason = f"Class in progress: {class_check['subject_name']}"
                        logger.warning(f"Exit denied for student {student['id_number']} - Reason: {reason}")
                else:
                    print(f"DIRECT DB CHECK: No class found for student {student['id_number']} in section {student['section_id']} at {current_time_obj}")
                    
                    # Check if student just finished a class (within last 15 minutes)
                    just_finished_query = """
                    SELECT cs.schedule_id, s.subject_name, cs.time_start, cs.time_end
                    FROM class_schedules cs 
                    JOIN subjects s ON cs.subject_id = s.subject_id
                    WHERE cs.section_id = %s
                    AND cs.day_of_week = %s
                    AND TIME(cs.time_end) BETWEEN DATE_SUB(%s, INTERVAL 15 MINUTE) AND %s
                    ORDER BY cs.time_end DESC
                    LIMIT 1
                    """
                    just_finished = db.fetch_one(just_finished_query, (
                        student['section_id'], 
                        current_day_name, 
                        current_time_obj, 
                        current_time_obj
                    ))
                    
                    if just_finished:
                        print(f"Student just finished class {just_finished['subject_name']} at {just_finished['time_end']}")
                        exit_status = 'ALLOWED'
                        reason = f"Class recently ended: {just_finished['subject_name']}"
                        logger.info(f"Exit allowed for student {student['id_number']} - Reason: {reason}")
                    else:
                        # Check if student has another class soon (within the next 30 minutes)
                        next_class_query = """
                        SELECT cs.schedule_id, s.subject_name, cs.time_start, cs.time_end
                        FROM class_schedules cs 
                        JOIN subjects s ON cs.subject_id = s.subject_id
                        WHERE cs.section_id = %s
                        AND cs.day_of_week = %s
                        AND TIME(cs.time_start) BETWEEN %s AND DATE_ADD(%s, INTERVAL 30 MINUTE)
                        ORDER BY cs.time_start ASC
                        LIMIT 1
                        """
                        next_class = db.fetch_one(next_class_query, (
                            student['section_id'], 
                            current_day_name, 
                            current_time_obj, 
                            current_time_obj
                        ))
                        
                        if next_class:
                            print(f"Student has upcoming class {next_class['subject_name']} at {next_class['time_start']}")
                            exit_status = 'ALLOWED'
                            reason = f"Next class starts at {next_class['time_start'].strftime('%I:%M %p') if hasattr(next_class['time_start'], 'strftime') else str(next_class['time_start'])}: {next_class['subject_name']}"
                            logger.info(f"Exit allowed for student {student['id_number']} - Reason: {reason}")
                        else:
                            print(f"No upcoming classes found")
                            exit_status = 'ALLOWED'
                            reason = "No active classes"
                            logger.info(f"Exit allowed for student {student['id_number']} - No active classes")
            
            # Create and save exit log
            try:
                exit_log = ExitLog(
                    student_id=student['student_id'],
                    exit_time=current_time,
                    status=exit_status,
                    reason=reason,
                    destination="Outside Campus"
                )
                log_id = exit_log.save()
                
                if not log_id:
                    logger.error("Failed to save exit log")
                    # Continue execution even if saving fails, to at least show the status
                    logger.warning("Continuing execution despite exit log save failure")
            except Exception as e:
                logger.error(f"Error saving exit log: {str(e)}")
                # Continue execution even if saving fails
                logger.warning("Continuing execution despite exit log save failure")
                log_id = None
            
            # Format the response
            student_data = {
                'first_name': student['first_name'] or '',
                'middle_initial': student['middle_initial'] or '',
                'last_name': student['last_name'] or '',
                'id_number': student['id_number'] or '',
                'grade_level': student['grade_level'] or '',
                'section': section_result['section_name'],
                'strand_code': section_result['strand_code'],
                'profile_picture': student['profile_picture_path'],
                'exit_time': current_time.strftime('%Y-%m-%d %H:%M:%S'),  # Consistent MySQL-format timestamp
                'exit_status': exit_status,
                'reason': reason
            }
            
            result = {
                'status': 'success',
                'log_id': log_id,  # Include the log ID in the response
                'student': student_data
            }
            
            # Send MS Teams notification if exit is denied, but do it asynchronously
            if exit_status == 'DENIED' and class_info:
                try:
                    # Format student info for the notification
                    student_info = {
                        'first_name': student['first_name'] or '',
                        'middle_initial': student['middle_initial'] or '',
                        'last_name': student['last_name'] or '',
                        'id_number': student['id_number'] or '',
                        'grade_level': student['grade_level'] or '',
                        'section': section_result['section_name'],
                        'strand_code': section_result['strand_code']
                    }
                    
                    # Start notification thread without waiting for it
                    notification_thread = Thread(target=send_denied_exit_notification, 
                                               args=(student_info, reason, class_info))
                    notification_thread.daemon = True
                    notification_thread.start()
                except Exception as e:
                    # Just log the error and continue - don't let notification issues affect the exit process
                    logger.error(f"Failed to start notification thread: {str(e)}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing exit request: {str(e)}", exc_info=True)
            return {'status': 'error', 'message': f'Server error: {str(e)}'}
    
    @staticmethod
    def get_recent_logs(limit=50):
        try:
            logs = ExitLog.get_recent_logs(limit)
            return logs if logs else []
        except Exception as e:
            logger.error(f"Error getting recent logs: {str(e)}")
            return []