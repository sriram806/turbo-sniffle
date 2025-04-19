import sqlite3
import os
import json
import re

def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_\-\.]', '_', filename)

def get_db_path(train_id, travel_date):
    folder = "train_dbs"
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    train_id = sanitize_filename(train_id)
    travel_date = sanitize_filename(travel_date)
    
    db_name = f"{folder}/train_{train_id}_{travel_date}.db"
    return db_name

def create_table_if_not_exists(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS passengers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            face_encoding TEXT,
            boarded BOOLEAN DEFAULT 0
        )
    ''')
    
def save_passenger(name, age, gender, train_id, travel_date, encoding):
    db_path = get_db_path(train_id, travel_date)
    print(f"Connecting to database at: {db_path}")
    conn = sqlite3.connect(db_path)
    create_table_if_not_exists(conn)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passengers (name, age, gender, face_encoding) VALUES (?, ?, ?, ?)",
                   (name, age, gender, json.dumps(encoding)))
    conn.commit()
    conn.close() 
