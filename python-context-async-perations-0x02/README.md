# Context Managers and Asynchronous Programming in Python

## Introduction

This project aims to enhance my backend development skills using Python, focusing on both synchronous and asynchronous programming paradigms. It includes various exercises related to database interaction, context managers, and asynchronous operations, specifically leveraging the `aiosqlite` and `asyncio` libraries.

The project provides solutions to:
1. Context Manager for managing database connections.
2. Asynchronous queries using `aiosqlite`.
3. Concurrency with `asyncio.gather()` to run multiple database queries concurrently.

---

## Key Concepts Covered

### 1. **Class-based Context Managers**
   - Used to manage database connections in an efficient and reusable manner.
   - Helps in automatically handling opening and closing of database connections using the `__enter__()` and `__exit__()` methods.

### 2. **Database Queries with SQLite**
   - Performing synchronous database operations using SQLite.
   - Fetching all users and filtering based on conditions (e.g., users older than 40).
   
### 3. **Asynchronous Programming**
   - Leveraging the `asyncio` library to run multiple coroutines concurrently.
   - Using `aiosqlite` to asynchronously interact with an SQLite database.
   - Using `asyncio.gather()` to execute multiple database queries concurrently without blocking.

---

## Installation

To run the code, ensure that you have Python installed (preferably Python 3.7+).

1. Install the required dependencies:
   ```bash
   pip install aiosqlite
   ```

2. Ensure you have an SQLite database, `users.db`, with the necessary `users` table.

---

## Features

### 1. **Custom Context Manager (`DatabaseConnection`)**
   - A reusable class-based context manager for establishing and closing database connections.
   - The context manager automatically handles the opening and closing of connections to an SQLite database.

   Example usage:
   ```python
   query = "SELECT * FROM users"
   with DatabaseConnection(query, "users.db") as cursor:
       for row in cursor:
           print(row)
   ```

### 2. **Asynchronous Database Queries**
   - Fetch all users and users older than 40 from an SQLite database using asynchronous functions.
   - Use `asyncio.gather()` to run both queries concurrently.

   Example usage:
   ```python
   async def fetch_concurrently():
       users, older_users = await asyncio.gather(
           async_fetch_users(),
           async_fetch_older_users()
       )
       # Print the results
   asyncio.run(fetch_concurrently())
   ```

### 3. **Asynchronous Functions:**
   - **`async_fetch_users()`**: Fetches all users from the `users` table.
   - **`async_fetch_older_users()`**: Fetches users older than 40 from the `users` table.


## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/jubriltayo/alx-backend-python.git
   ```

2. Ensure the SQLite database (`users.db`) exists with a `users` table containing relevant data.

3. Run the Python script that contains your desired functionality (e.g., database connection, or asynchronous query fetching).

---

## Conclusion

This project is designed to help understand the key backend concepts in Python, including context managers, database interactions with SQLite, and asynchronous programming for handling multiple tasks concurrently. These skills is useful to develop more efficient and scalable backend systems.
