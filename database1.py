import sqlite3

# ------------------------
# Connect to DB
# ------------------------
conn = sqlite3.connect('defects.db', check_same_thread=False)
c = conn.cursor()

# ------------------------
# Create Table (with new fields)
# ------------------------
def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS defects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reported_date TEXT,
            module TEXT,
            description TEXT,
            severity TEXT,
            status TEXT,
            assigned_to TEXT,
            resolution_date TEXT,
            image TEXT,
            vehicle_model TEXT,
            defect_category TEXT,
            reported_by TEXT
        )
    ''')
    conn.commit()

# ------------------------
# Insert New Defect
# ------------------------
def insert_defect(reported_date, module, description, severity, status,
                  assigned_to, resolution_date, image, vehicle_model,
                  defect_category, reported_by):
    c.execute('''
        INSERT INTO defects (
            reported_date, module, description, severity, status,
            assigned_to, resolution_date, image,
            vehicle_model, defect_category, reported_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        reported_date, module, description, severity, status,
        assigned_to, resolution_date, image,
        vehicle_model, defect_category, reported_by
    ))
    conn.commit()

# ------------------------
# Get All Defects
# ------------------------
def get_all_defects():
    c.execute('SELECT * FROM defects')
    data = c.fetchall()
    return data
