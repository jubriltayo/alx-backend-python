import sqlite3
import functools
from datetime import datetime

# decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func) # Ensure original function name instead of wrapper. fetch_all_users.__name__ == fetch_all_users
    def wrapper(*args, **kwargs):
        # if kwargs get 'query', if args get the first arg
        query = kwargs.get('query', args[0] if args else None)
        if query:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Executing SQL Query: {query}")
        else:
            print("No query found to log.")
        return func(*args, **kwargs) # call the original function
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
for user in users:
    print(user)