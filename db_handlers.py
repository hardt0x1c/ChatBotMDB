import sqlite3

conn = sqlite3.Connection("addons/database/database.db")
cursor = conn.cursor()


def get_user(cursor, user_id):
    return cursor.execute("SELECT * FROM users WHERE user_id=?;", (user_id,)).fetchone()


def add_user(conn, cursor, user_id):
    try:
        cursor.execute("INSERT INTO users (user_id) VALUES (?);", (user_id,))
        conn.commit()
        return True
    except:
        return False


def get_users(cursor):
    cursor.execute('''SELECT user_id FROM users''')
    spam_base = cursor.fetchall()
    return spam_base
