import pymysql


class ExecuteQuery:
    def __init__(self, query, params=None):
        """ Initialize the context manager with a wuery and optional parameters """
        self.query = query
        self.params = params
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
        self.cursor.execute(self.query, self.params)
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
    query = "SELECT * FROM users WHERE age > %s"
    params = 25

    try:
        with ExecuteQuery(query, params) as cursor:
            for row in cursor:
                print(row)
    except Exception as e:
        print(f"Exception: {e}")