import asyncio
import aiosqlite



# Asynchronous function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute('SELECT * FROM users')
        users = await cursor.fetchall()
        return users


# Asynchronous function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute('SELECT * FROM users WHERE age > 40')
        old_users = await cursor.fetchall()
        return old_users


# Function to run both queries concurrently
async def fetch_concurrently():
    users, old_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All Users:")
    for user in users:
        print(user)

    print("\n")

    print("Users Older Than 40:")
    for user in old_users:
        print(old_users)


# Run the asynchronous function
asyncio.run(fetch_concurrently())