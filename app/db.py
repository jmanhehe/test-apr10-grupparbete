import os
import psycopg2
from datetime import datetime, timezone

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            ip TEXT NOT NULL,
            user_agent TEXT NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def add_visit(ip, user_agent):
    conn = get_db_connection()
    cur = conn.cursor()
    now = datetime.now(timezone.utc)
    cur.execute(
        'INSERT INTO visits (timestamp, ip, user_agent) VALUES (%s, %s, %s) RETURNING id',
        (now, ip, user_agent)
    )
    visit_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {
        "id": visit_id,
        "timestamp": now,
        "ip": ip,
        "user_agent": user_agent
    }

def get_all_visits():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, timestamp, ip, user_agent FROM visits ORDER BY id')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {"id": row[0], "timestamp": row[1], "ip": row[2], "user_agent": row[3]}
        for row in rows
    ]

def get_visit_by_id(visit_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, timestamp, ip, user_agent FROM visits WHERE id = %s', (visit_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {"id": row[0], "timestamp": row[1], "ip": row[2], "user_agent": row[3]}
    return None

def format_visit_history(history):
    # Placeholder implementation
    return history  
