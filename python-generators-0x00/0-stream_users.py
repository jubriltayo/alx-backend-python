import pymysql


def stream_users():
    """
    Generator function to fetch rows one by one from the user_data table
    """
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="ALX_prodev"
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM user_data")
    
    for row in cursor:
        yield row
    
    cursor.close()
    connection.close()
