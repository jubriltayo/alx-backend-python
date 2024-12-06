import sqlite3

# Set up SQLite database and create table
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        age INTEGER
    )
    ''')

    # Insert sample data if the table is empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:  # No data
        cursor.executemany('INSERT INTO users (id, name, email, age) VALUES (?, ?, ?, ?)', [
            ('1', 'Miss Arlene Herzog', 'Ada33@gmail.com', 103),
            ('2', 'John Doe', 'john.doe@example.com', 35),
            ('3', 'Jane Smith', 'jane.smith@example.com', 28)
        ])
    conn.commit()
    conn.close()

# Call setup function
setup_database()
