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


def transactional(func):
    """ Decorator to manage transactions (commit or rollback) """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs) # call original function
            conn.commit() # save transaction
            return result
        except Exception as e: # exception was caught to allow time for rollback and log
            conn.rollback() # rollback transaction
            print(f"Transaction failed: {e}")
            raise # reraise the exception to notify original function (caller)
    return wrapper


@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    #### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
