import os
if os.path.exists("defects.db"):
    os.remove("defects.db")

import sqlite3

def create_table():
    conn = sqlite3.connect('defects.db')
    c = conn.cursor()
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
            reported_by TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_defect(reported_date, module, description, severity, status,
                  assigned_to, resolution_date, image, vehicle_model, reported_by):
    conn = sqlite3.connect('defects.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO defects (
            reported_date, module, description, severity, status,
            assigned_to, resolution_date, image, vehicle_model, reported_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (reported_date, module, description, severity, status,
          assigned_to, resolution_date, image, vehicle_model, reported_by))
    conn.commit()
    conn.close()

def get_all_defects():
    conn = sqlite3.connect('defects.db')
    c = conn.cursor()
    c.execute('SELECT * FROM defects')
    rows = c.fetchall()
    conn.close()
    return rows
