# Python Decorators: A Practical Guide

This repository demonstrates the practical applications of Python decorators in managing database interactions efficiently. Each script builds on core concepts such as caching, retry mechanisms, connection management, and transactions. The examples use SQLite and Python’s built-in tools to illustrate how decorators simplify repetitive tasks in backend development.

---

## **Features**
1. **Connection Management**: Automatically open and close database connections with a reusable `with_db_connection` decorator.
2. **Transaction Handling**: Commit or rollback database changes using a `transactional` decorator.
3. **Retry Mechanism**: Handle transient database errors by retrying queries with the `retry_on_failure` decorator.
4. **Query Caching**: Avoid redundant queries with the `cache_query` decorator.
5. **Logging**: Log SQL queries to debug database operations effectively.

---

## **Scripts**

### 1. **Logging Queries**
- **Objective**: Create a decorator to log SQL queries before execution.
- **Key Points**:
  - Logs query strings for monitoring or debugging.
  - Example:
    ```python
    @log_queries
    def fetch_all_users(query):
        # Executes the query while logging
    ```

---

### 2. **Connection Management**
- **Objective**: Simplify database connection handling with the `with_db_connection` decorator.
- **Key Points**:
  - Automatically opens and closes the connection.
  - Prevents resource leaks by using a `try/finally` block.
  - Example:
    ```python
    @with_db_connection
    def get_user_by_id(conn, user_id):
        # Database operations with connection
    ```

---

### 3. **Transaction Management**
- **Objective**: Ensure changes are committed or rolled back based on success or failure.
- **Key Points**:
  - Uses `try/except/finally` to handle errors and rollback.
  - Automatically commits changes if no error occurs.
  - Example:
    ```python
    @with_db_connection
    @transactional
    def update_user_email(conn, user_id, new_email):
        # Updates the user's email
    ```

---

### 4. **Retry Mechanism**
- **Objective**: Retry database queries if they fail due to transient errors.
- **Key Points**:
  - Configurable retries and delay between attempts.
  - Example:
    ```python
    @with_db_connection
    @retry_on_failure(retries=3, delay=2)
    def fetch_users_with_retry(conn):
        # Fetches users with automatic retry on failure
    ```

---

### 5. **Query Caching**
- **Objective**: Cache query results to improve performance and avoid redundant queries.
- **Key Points**:
  - Caches results in memory using a dictionary.
  - Fetches results from the cache if the query is repeated.
  - Example:
    ```python
    @with_db_connection
    @cache_query
    def fetch_users_with_cache(conn, query):
        # Executes the query and caches the result
    ```

---

## **Requirements**
- Python 3.6+
- SQLite3 (default with Python)
- No additional dependencies

---

## **Usage**
1. Clone the repository:
   ```bash
   git clone https://github.com/jubriltayo/alx-backend-python.git
   ```
2. Navigate to the directory:
   ```bash
   cd python-decorators
   ```
3. Run individual scripts:
   ```bash
   python <script_name>.py
   ```

---

## **Concepts Covered**
1. **Python Decorators**:
   - How to wrap functions with additional logic.
   - Combining multiple decorators.
2. **Database Management**:
   - Simplifying database interactions with reusable patterns.
3. **Error Handling**:
   - Using `try/except/finally` for robust applications.
4. **Performance Optimization**:
   - Leveraging caching to reduce redundant database calls.

---

## **Examples**

### Logging Queries:
```python
Executing query: SELECT * FROM users
```

### Retrying on Failure:
```plaintext
Attempt 1 failed, retrying in 1 second...
Attempt 2 failed, retrying in 1 second...
```

### Caching:
```plaintext
Executing query and caching result.
Using cached result.
```

---

## **Contributors**
- **Jubril Tayo**: Backend Developer specializing in Python and SQL.
