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
    email VARCHAR(100)
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

-- Insert default admin (password: admin)
INSERT INTO admins (username, password, first_name, last_name)
VALUES ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'System', 'Administrator');

-- Insert strands
INSERT INTO strands (strand_name, strand_code, description) VALUES 
('STEM', 'STEM', 'Science, Technology, Engineering, and Mathematics'),
('ABM', 'ABM', 'Accountancy, Business, and Management'),
('GAS', 'GAS', 'General Academic Strand');

-- Get strand IDs for reference
SET @stem_id = (SELECT strand_id FROM strands WHERE strand_name = 'STEM');
SET @abm_id = (SELECT strand_id FROM strands WHERE strand_name = 'ABM');
SET @gas_id = (SELECT strand_id FROM strands WHERE strand_name = 'GAS');

-- Insert STEM sections for Grade 11
INSERT INTO sections (section_name, grade_level, strand_id) VALUES
('Altruism', 11, @stem_id),
('Benevolence', 11, @stem_id),
('Competence', 11, @stem_id),
('Diligence', 11, @stem_id),
('Enthusiasm', 11, @stem_id),
('Friendship', 11, @stem_id),
('Generosity', 11, @stem_id),
('Humility', 11, @stem_id),
('Integrity', 11, @stem_id),
('Justice', 11, @stem_id),
('Kindness', 11, @stem_id),
('Loyalty', 11, @stem_id),
('Modesty', 11, @stem_id),
('Nobility', 11, @stem_id),
('Obedience', 11, @stem_id),
('Peace', 11, @stem_id),
('Quality', 11, @stem_id);

-- Insert STEM sections for Grade 12
INSERT INTO sections (section_name, grade_level, strand_id) VALUES
('Altruism', 12, @stem_id),
('Benevolence', 12, @stem_id),
('Competence', 12, @stem_id),
('Diligence', 12, @stem_id),
('Enthusiasm', 12, @stem_id),
('Friendship', 12, @stem_id),
('Generosity', 12, @stem_id),
('Humility', 12, @stem_id),
('Integrity', 12, @stem_id),
('Justice', 12, @stem_id),
('Kindness', 12, @stem_id),
('Loyalty', 12, @stem_id),
('Modesty', 12, @stem_id),
('Nobility', 12, @stem_id),
('Obedience', 12, @stem_id),
('Peace', 12, @stem_id),
('Quality', 12, @stem_id),
('Respect', 12, @stem_id);  -- Respect is only for Grade 12

-- Insert ABM sections for Grade 11
INSERT INTO sections (section_name, grade_level, strand_id) VALUES
('Responsibility', 11, @abm_id),
('Sincerity', 11, @abm_id),
('Tenacity', 11, @abm_id);

-- Insert ABM sections for Grade 12
INSERT INTO sections (section_name, grade_level, strand_id) VALUES
('Responsibility', 12, @abm_id),
('Sincerity', 12, @abm_id),
('Tenacity', 12, @abm_id);

-- Insert GAS sections for Grade 11
INSERT INTO sections (section_name, grade_level, strand_id) VALUES
('Wisdom', 11, @gas_id);

-- Insert GAS sections for Grade 12
INSERT INTO sections (section_name, grade_level, strand_id) VALUES
('Wisdom', 12, @gas_id);

-- Insert some sample subjects
INSERT INTO subjects (subject_code, subject_name) VALUES
('MATH101', 'Mathematics 1'),
('ENG101', 'English 1'),
('SCI101', 'Science 1'),
('FIL101', 'Filipino 1'),
('PE101', 'Physical Education 1');

-- Insert some sample teachers
INSERT INTO teachers (first_name, middle_initial, last_name, email) VALUES
('John', 'A', 'Smith', 'john.smith@school.edu'),
('Maria', 'B', 'Garcia', 'maria.garcia@school.edu'),
('Robert', 'C', 'Johnson', 'robert.johnson@school.edu'),
('Sarah', 'D', 'Williams', 'sarah.williams@school.edu'),
('Michael', 'E', 'Brown', 'michael.brown@school.edu');