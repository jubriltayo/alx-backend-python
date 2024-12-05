#!/usr/bin/python3
seed = __import__('seed')
import pymysql.cursors
import sys


def paginate_users(page_size, offset):
    """Fetches a page of user data with a specific page size and offset."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(pymysql.cursors.DictCursor)  # Ensures rows are returned as dictionaries
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    A generator function to lazily fetch and yield paginated data.
    """
    offset = 0
    
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # If no more rows are fetched, stop iteration
            break
        yield page
        offset += page_size
