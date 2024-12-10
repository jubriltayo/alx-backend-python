import sqlite3


class DatabaseConnection:
    def __init__(self, query, db_file):
        """ Initialization """
        self.query = query
        self.db_file = db_file
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Establish the database connection and return the results of the query
        """
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """ 
        Close the cursor and database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        return False


if __name__ == "__main__":
    query = "SELECT * FROM users"
    db_file = "users.db"

    try:
        with DatabaseConnection(query, db_file) as cursor:
            for row in cursor:
                print(row)
    except Exception as e:
        print(f"Exception: {e}")
