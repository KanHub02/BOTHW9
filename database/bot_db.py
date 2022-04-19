import sqlite3
from config import bot


def sql_create():
    global connection, cursor
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()
    if connection:
        print("Database connected successfully")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tvshow 
        (photo TEXT, title TEXT PRIMARY KEY, description TEXT)
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS my_users 
        (photo TEXT, telegram_acount_id TEXT,username PRIMARY KEY, first_name TEXT,last_name TEXT)
        """
    )
    connection.commit()


async def sql_insert(state):
    async with state.proxy() as data:
        cursor.execute("""
        INSERT INTO tvshow VALUES (?, ?, ?)
        """, tuple(data.values()))
        connection.commit()

async def user_insert(state):
    async with state.proxy() as data:
        cursor.execute("""
        INSERT INTO my_users VALUES (?, ?, ? ,? ,?)
        """, tuple(data.values()))
        connection.commit()

async def sql_select(message):
    for result in cursor.execute("""SELECT * FROM tvshow""").fetchall():
        await bot.send_photo(message.chat.id,
                             result[0],
                             caption=f'Title {result[1]}\n'
                                     f'Description: {result[2]}')


async def user_select(message):
    for show in cursor.execute("""SELECT * FROM my_users""").fetchall():
        await bot.send_photo(message.chat.id,
                             show[0],
                             caption=f'telegram_acount_id {show[1]}\n'
                                     f'username: {show[2]}\n'
                                     f'first_name {show[3]}\n'
                                     f'last_name: {show[4]}')


async def sql_casual_select():
    return cursor.execute("""SELECT * FROM tvshow""").fetchall()

async def user_casual_select():
    return cursor.execute("""SELECT * FROM my_users""").fetchall()


async def sql_delete(data):
    cursor.execute("""
    DELETE FROM tvshow WHERE title == ?
    """, (data,))
    connection.commit()

async def user_delete(data):
    cursor.execute("""
    DELETE FROM my_users WHERE username == ?
    """, (data,))
    connection.commit()