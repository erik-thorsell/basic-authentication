import sqlite3

database_path = '../database.db'

def get_db_connection():
    """Returns a connection aswell as a cursor to the SQLite database."""
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    conn.autocommit = True
    cursor = conn.cursor()
    return conn, cursor

def init_db():
    conn, cursor = get_db_connection()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        code INT,
        classes TEXT DEFAULT '{}' NOT NULL
    )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            members TEXT DEFAULT '{}' NOT NULL,
            administrators TEXT DEFAULT '{}' NOT NULL,
            lessons TEXT DEFAULT '{}' NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lessons (
            id INT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT DEFAULT '' NOT NULL,
            settings TEXT DEFAULT '{}' NOT NULL,
            content TEXT DEFAULT '{}' NOT NULL
        )
    ''')

    conn.commit()
    conn.close()