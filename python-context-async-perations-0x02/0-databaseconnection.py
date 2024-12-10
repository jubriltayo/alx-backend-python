import pymysql


class DatabaseConnection:
    def __init__(self, query):
        """ Initialization """
        self.query = query
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Establish the database connection and return the results of the query
        """
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute(self.query)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """ 
        Close the cursor and database connection.
        Handle exceptions if necessary
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        return False


if __name__ == "__main__":
    query = "SELECT * FROM user_data"

    try:
        with DatabaseConnection(query) as cursor:
            for row in cursor:
                print(row)
    except Exception as e:
        print(f"Exception: {e}")