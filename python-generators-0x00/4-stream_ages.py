import pymysql

def stream_user_ages(batch_size):
    """
    A generator that streams user ages from the database, one by one.
    """
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="ALX_prodev"
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT age FROM user_data")

    for user in cursor:
        yield user['age']  # Yield age for each user
    
    cursor.close()
    connection.close()

def calculate_average_age(batch_size):
    """
    Calculate the average age of users using the stream_user_ages generator.
    """
    total_age = 0
    total_users = 0

    # Use the generator to accumulate sum and count
    for age in stream_user_ages(batch_size):
        total_age += age
        total_users += 1

    if total_users > 0:
        average_age = total_age / total_users
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found")
