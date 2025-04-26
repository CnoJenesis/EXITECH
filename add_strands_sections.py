from database.db_connector import Database

def add_strands_and_sections():
    db = Database()
    
    # First, check if strands table exists and create it if not
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS strands (
            strand_id INT AUTO_INCREMENT PRIMARY KEY,
            strand_name VARCHAR(50) NOT NULL UNIQUE,
            strand_code VARCHAR(10) NOT NULL UNIQUE,
            description VARCHAR(255)
        )
    """)
    
    # Check if sections table exists and create it if not
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS sections (
            section_id INT AUTO_INCREMENT PRIMARY KEY,
            section_name VARCHAR(50) NOT NULL,
            grade_level INT NOT NULL,
            strand_id INT NOT NULL,
            FOREIGN KEY (strand_id) REFERENCES strands(strand_id),
            UNIQUE KEY section_grade_strand (section_name, grade_level, strand_id)
        )
    """)
    
    # Add strands with codes
    strands = [
        {'name': 'STEM', 'code': 'STEM', 'description': 'Science, Technology, Engineering, and Mathematics'},
        {'name': 'ABM', 'code': 'ABM', 'description': 'Accountancy, Business, and Management'},
        {'name': 'GAS', 'code': 'GAS', 'description': 'General Academic Strand'}
    ]
    
    strand_ids = {}
    
    # Insert strands using INSERT IGNORE to handle duplicates
    for strand in strands:
        query = """
            INSERT IGNORE INTO strands (strand_name, strand_code, description) 
            VALUES (%s, %s, %s)
        """
        db.execute_query(query, (strand['name'], strand['code'], strand['description']))
        
        # Get the strand ID
        get_id_query = "SELECT strand_id FROM strands WHERE strand_name = %s"
        result = db.fetch_one(get_id_query, (strand['name'],))
        if result:
            strand_ids[strand['name']] = result['strand_id']
            print(f"Added/Found strand: {strand['name']} with ID: {strand_ids[strand['name']]}")
    
    # Define sections for each strand and grade level
    stem_sections = [
        "Altruism", "Benevolence", "Competence", "Diligence", "Enthusiasm",
        "Friendship", "Generosity", "Humility", "Integrity", "Justice",
        "Kindness", "Loyalty", "Modesty", "Nobility", "Obedience",
        "Peace", "Quality"
    ]
    
    # Respect is only for Grade 12
    grade_12_only = ["Respect"]
    
    abm_sections = ["Responsibility", "Sincerity", "Tenacity"]
    gas_sections = ["Wisdom"]
    
    # Only proceed if we have valid strand IDs
    if all(strand_ids.values()):
        # Add sections using INSERT IGNORE to handle duplicates
        
        # Add sections for STEM
        for section in stem_sections:
            # Add for Grade 11
            query = """
                INSERT IGNORE INTO sections (section_name, grade_level, strand_id) 
                VALUES (%s, %s, %s)
            """
            db.execute_query(query, (section, 11, strand_ids['STEM']))
            print(f"Added Grade 11 STEM section: {section}")
            
            # Add for Grade 12
            db.execute_query(query, (section, 12, strand_ids['STEM']))
            print(f"Added Grade 12 STEM section: {section}")
        
        # Add Respect for Grade 12 only
        for section in grade_12_only:
            query = """
                INSERT IGNORE INTO sections (section_name, grade_level, strand_id) 
                VALUES (%s, %s, %s)
            """
            db.execute_query(query, (section, 12, strand_ids['STEM']))
            print(f"Added Grade 12 STEM section: {section}")
        
        # Add sections for ABM
        for section in abm_sections:
            # Add for Grade 11
            query = """
                INSERT IGNORE INTO sections (section_name, grade_level, strand_id) 
                VALUES (%s, %s, %s)
            """
            db.execute_query(query, (section, 11, strand_ids['ABM']))
            print(f"Added Grade 11 ABM section: {section}")
            
            # Add for Grade 12
            db.execute_query(query, (section, 12, strand_ids['ABM']))
            print(f"Added Grade 12 ABM section: {section}")
        
        # Add sections for GAS
        for section in gas_sections:
            # Add for Grade 11
            query = """
                INSERT IGNORE INTO sections (section_name, grade_level, strand_id) 
                VALUES (%s, %s, %s)
            """
            db.execute_query(query, (section, 11, strand_ids['GAS']))
            print(f"Added Grade 11 GAS section: {section}")
            
            # Add for Grade 12
            db.execute_query(query, (section, 12, strand_ids['GAS']))
            print(f"Added Grade 12 GAS section: {section}")
        
        print("All strands and sections have been added successfully!")
    else:
        print("Failed to get valid strand IDs. Sections were not added.")
    
    db.close()

if __name__ == "__main__":
    add_strands_and_sections()