import sqlite3

def setup_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            title TEXT,
            url TEXT,
            permalink TEXT,
            subreddit TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id TEXT,
            body TEXT,
            score INTEGER,
            FOREIGN KEY (post_id) REFERENCES posts(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database and tables created successfully.")

if __name__ == "__main__":
    setup_database('mydatabaseSearchEngine.db')
