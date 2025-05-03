import sqlite3

def connect_to_database():
    connection = sqlite3.connect('auth_api.db')
    return connection

def create_users_table(connection):
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    connection.commit()

def create_user(connection, username, password): 
    cursor = connection.cursor()

    try:
        cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
        connection.commit()
        return True 
    
    except sqlite3.IntegrityError: 
        return False 

def clear_users_table(connection):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users')
    connection.commit()
