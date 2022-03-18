from mimetypes import init
import sqlite3

DATABASE_FILE = 'instance/database.sqlite3'

def init_db():
    connection = sqlite3.connect(DATABASE_FILE)
    with open('schema.sql') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def execute_db_command(command, args=()):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute(command, args)
    connection.commit()
    connection.close()

def execute_db_query(query, args=(), one=False):
    cur = get_db_connection().execute(query, args)
    values = cur.fetchall()
    cur.close()
    return values[0] if one else values

def main():
    init_db()

if __name__ == '__main__':
    main()