import pymysql
import sys


def stream_users_in_batches(batch_size):
    """
    Fetch rows from the user_data in batches using a generator
    """
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="ALX_prodev"
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    batch = []
    for user in cursor:
        batch.append(user)
        if len(batch) >= batch_size:
            yield batch
            batch = [] 

    if batch:
        yield batch # last batch
    
    return
    
    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """ Process each batch to filter users over the age of 25 """
    try:
        for batch in stream_users_in_batches(batch_size):
            filtered_batch = [user for user in batch if user['age'] > 25] # filter users with age over 25
            for user in filtered_batch:
                print(user)
    except (BrokenPipeError, OSError):
        sys.stderr.close()