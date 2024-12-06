import time
import sqlite3 
import functools


def with_db_connection(func):
    """ Decorator that opens and closes the database connection """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """ Decorator to retry a function if it raises an exception """
    def decorator(func): # handles/accepts parameters (retries and delay)
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs): # handles the retry logic
            attempt = 0
            while attempt < retries:
                try:
                    return func(conn, *args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("Max retries reached, Operation failed.")
                        raise e # reraise the exception after max retries
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# attempt to fetch users with automatic retry on failure
try:
    users = fetch_users_with_retry()
    print(users)
except Exception as e:
    print(f"Failed to fetch users: {e}")