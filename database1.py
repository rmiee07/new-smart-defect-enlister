import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("defects.db", check_same_thread=False)
c = conn.cursor()

# Create the table if it doesn't exist
def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS defects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_reported TEXT,
            module TEXT,
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

# Insert new defect entry
def insert_defect(date_reported, module, description, severity, status,
                  assigned_to, resolution_date, image, vehicle_model, reported_by):
    c.execute('''
        INSERT INTO defects (
            date_reported, module, description, severity, status,
            assigned_to, resolution_date, image, vehicle_model, reported_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        date_reported, module, description, severity, status,
        assigned_to, resolution_date, image, vehicle_model, reported_by
    ))
    conn.commit()

# Retrieve all defects
def get_all_defects():
    c.execute("SELECT * FROM defects")
    return c.fetchall()
