-- Drop existing database if it exists
DROP DATABASE IF EXISTS exitech;

-- Create database
CREATE DATABASE exitech;

-- Use the database
USE exitech;

-- Create tables
CREATE TABLE IF NOT EXISTS strands (
    strand_id INT AUTO_INCREMENT PRIMARY KEY,
    strand_name VARCHAR(50) NOT NULL UNIQUE,
    strand_code VARCHAR(10) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    section_name VARCHAR(50) NOT NULL,
    grade_level INT NOT NULL,
    strand_id INT NOT NULL,
    FOREIGN KEY (strand_id) REFERENCES strands(strand_id),
    UNIQUE KEY section_grade_strand (section_name, grade_level, strand_id)
);

CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    id_number VARCHAR(20) NOT NULL UNIQUE,
    rfid_uid VARCHAR(50) UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    middle_initial VARCHAR(5),
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10),
    grade_level INT NOT NULL,
    strand_id INT NOT NULL,
    section_id INT NOT NULL,
    profile_picture VARCHAR(255),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (strand_id) REFERENCES strands(strand_id)
);

CREATE TABLE IF NOT EXISTS subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(20) NOT NULL UNIQUE,
    subject_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_initial VARCHAR(5),
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS class_schedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT NOT NULL,
    subject_id INT NOT NULL,
    teacher_id INT NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    time_start TIME NOT NULL,
    time_end TIME NOT NULL,
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

CREATE TABLE IF NOT EXISTS exit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    status VARCHAR(20) NOT NULL,
    reason VARCHAR(255),
    destination VARCHAR(255),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE IF NOT EXISTS admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_initial VARCHAR(5),
    last_name VARCHAR(50) NOT NULL,
    profile_picture VARCHAR(255)
);

-- Create indexes for better performance
CREATE INDEX idx_student_rfid ON students(rfid_uid);
CREATE INDEX idx_schedule_section ON class_schedules(section_id);
CREATE INDEX idx_schedule_day_time ON class_schedules(day_of_week, time_start, time_end);
CREATE INDEX idx_exit_logs_student ON exit_logs(student_id);
CREATE INDEX idx_exit_logs_timestamp ON exit_logs(timestamp);

-- Insert default admin
INSERT INTO admins (username, password, first_name, last_name)
VALUES ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'System', 'Administrator');
-- Default password is 'admin'