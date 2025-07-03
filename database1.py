import sqlite3

# Connect to or create the database
conn = sqlite3.connect('defects.db', check_same_thread=False)
c = conn.cursor()

# ---------------------------
# Create the defect table
# ---------------------------
def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS defects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_reported TEXT,
            vehicle_system TEXT,
            description TEXT,
            severity TEXT,
            status TEXT,
            assigned_to TEXT,
            resolution_date TEXT,
            image TEXT,
            vehicle_model TEXT,
            reported_by TEXT
        )
    ''')
    conn.commit()

# ---------------------------
# Insert a new defect
# ---------------------------
def insert_defect(date_reported, vehicle_system, description, severity, status,
                  assigned_to, resolution_date, image, vehicle_model, reported_by):
    c.execute('''
        INSERT INTO defects (
            date_reported, module, description, severity, status,
            assigned_to, resolution_date, image, vehicle_model, reported_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        date_reported, vehicle_system, description, severity, status,
        assigned_to, resolution_date, image, vehicle_model, reported_by
    ))
    conn.commit()

# ---------------------------
# Fetch all defect records
# ---------------------------
def get_all_defects():
    c.execute('SELECT * FROM defects')
    return c.fetchall()
