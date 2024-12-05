import pymysql
import uuid
import csv


# Function to connect to MySQL server
def connect_db():
    """ COnnect to MySQL server """
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root"
    )

# Function to create the database if it doesnt exist
def create_database(connnection):
    """ Create the database if it doesnt exist """
    cursor = connnection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

# Function to connect to the database
def connect_to_prodev():
    """ Connect to ALX_prodev database """
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="ALX_prodev"
    )

# Function to create user_data table
def create_table(connection):
    """ Create the user_data table if it doesnt exist """
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL
        )
    """)
    cursor.close()

# Function to insert data into the user_data table
def insert_data(connection, file_path):
    """ Insert data into the user_data table if it doesnt exist """
    cursor = connection.cursor()

    # prepare the insert query
    insert_query = """
        INSERT INTO user_data (user_id, name, email, age) 
        VALUES (%s, %s, %s, %s)
    """

    # Read CSV file and return a list of dictionaries
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = str(uuid.uuid4())
            cursor.execute(insert_query, (user_id, row['name'], row['email'], row['age']))

    connection.commit()
    cursor.close()
