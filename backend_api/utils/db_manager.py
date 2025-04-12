import sqlite3
import os
import json

def get_db_path(train_id, travel_date):
    folder = "train_dbs"
    os.makedirs(folder, exist_ok=True)
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
    conn = sqlite3.connect(db_path)
    create_table_if_not_exists(conn)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passengers (name, age, gender, face_encoding) VALUES (?, ?, ?, ?)",
                   (name, age, gender, json.dumps(encoding)))
    conn.commit()
    conn.close()
