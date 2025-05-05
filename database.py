import sqlite3
import bcrypt

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

def delete_user(connection, username, password):
    cursor = connection.cursor()

    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        hashed_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            connection.commit()
            return True
    
    return False

def get_user_by_username(username, password, connection):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        hashed_password = result[1]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
    
    return False
