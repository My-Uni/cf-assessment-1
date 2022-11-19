import sqlite3
import bcrypt
import  maskpass

conn = sqlite3.connect('swe4207.db')
cursor = conn.cursor()

def _create_user_table():
    cursor.execute(''' CREATE TABLE IF NOT EXISTS user (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )''')
    conn.commit()

def _create_user():
    while True:
        username = input('Enter new users username: ')
        password = maskpass.askpass(prompt="Enter new users password: ",mask="*")
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor.execute('''INSERT INTO user (username, password) VALUES (?, ?)''', (username, password))
            conn.commit()
            break
        except:
            print(f'Username ({username}) already exists, try again\n')

def _login():
    while True:
        username = input('Enter username: ')
        password = maskpass.askpass(prompt="Enter password: ",mask="*")
        password = password.encode('utf-8')
        cursor.execute('''SELECT password FROM user WHERE username = ?''', (username,))
        try:
            hashed = cursor.fetchone()[0]
            if bcrypt.checkpw(password, hashed):
                print('Sucessfully logged in')
                break
            else:
                print('Login failed, try again\n')
        except:
            print('Login failed, try again\n')
    
user = {
    'createTable': _create_user_table,
    'create': _create_user,
    'login': _login
} 

user['createTable']()
user['login']()
user['create']()