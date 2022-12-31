#   Imports
import sqlite3
import bcrypt
import  maskpass
import os

#   Constants
conn = sqlite3.connect('swe4207.db')
cursor = conn.cursor()

#   Private Functions
def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer (
            customerid INTEGER PRIMARY KEY AUTOINCREMENT,
            forename TEXT NOT NULL,
            surname TEXT,
            dob TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS address (
            addressid INTEGER PRIMARY KEY AUTOINCREMENT,
            streetnumber TEXT,
            firstline TEXT NOT NULL,
            postcode TEXT,
            region TEXT NOT NULL,
            country TEXT NOT NULL,
            customerid INTEGER NOT NULL,
            FOREIGN KEY(customerid) REFERENCES customer(customerid)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account (
            accountid INTEGER PRIMARY KEY AUTOINCREMENT,
            balance REAL NOT NULL,
            opendate TEXT NOT NULL,
            closedate TEXT,
            status TEXT NOT NULL DEFAULT "ACTIVE",
            customerid INTEGER NOT NULL,
            FOREIGN KEY(customerid) REFERENCES customer(customerid)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transact (
            transactid INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            date TEXT NOT NULL,
            accountid INTEGER NOT NULL,
            FOREIGN KEY(accountid) REFERENCES account(accountid)
        );
    ''')

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
        os.system('clear')
        username = input('Enter username: ')
        password = maskpass.askpass(prompt="Enter password: ",mask="*")
        password = password.encode('utf-8')
        cursor.execute('''SELECT password FROM user WHERE username = ?''', (username,))
        try:
            hashed = cursor.fetchone()[0]
            if bcrypt.checkpw(password, hashed):
                print('Sucessfully logged in')
                display_menu['main']()
                break
            else:
                print('Login failed, try again\n')
        except:
            print('Login failed, try again\n')
    
user = {
    'create': _create_user,
    'login': _login
} 

def _main_menu():
    os.system('clear')
    print("".center(80, "*"))
    print(" MAIN MENU ".center(80, "*"))
    print("".center(80, "*"))

    print('''\n
[1] Customers
[2] Users
[3] Logout
[4] Logout & Exit
    ''')

    while True:
        user_choice = input()

        try:
            user_choice = int(user_choice)
            if user_choice == 1:
                display_menu['customers']()
                break
            elif user_choice == 2:
                print('Chose Users')
                break
            elif user_choice == 3:
                user['login']()
                break
            elif user_choice == 4:
                os.system('clear')
                print('Exiting Program...')
                os._exit(0)
                break
            else:
                print('Please choose a valid option\n')
        except:
            print('Please choose a valid option\n')

def _customers_menu():
    os.system('clear')
    print("".center(80, "*"))
    print(" CUSTOMERS ".center(80, "*"))
    print("".center(80, "*"))

    print('''\n
[1] Create new Customer
[2] View Customer Details
[3] Update Customer Details
[4] Main Menu
    ''')

    while True:
        user_choice = input()

        try:
            user_choice = int(user_choice)
            print(user_choice)
            if user_choice == 1:
                #   Create new Customer
                break
            elif user_choice == 2:
                #   View Customer Details
                break
            elif user_choice == 3:
                #   Update Customer Details
                break
            elif user_choice == 4:
                display_menu['main']()
                break
            else:
                print('Please choose a valid option\n')
        except:
            print('Please choose a valid option\n')

display_menu = {
    'main': _main_menu,
    'customers': _customers_menu
}

#   Initializing
#   Create Tables in the case that this is a fresh install
create_tables()

#   Default account, only run if it is a fresh install
    #cursor.execute('''INSERT INTO user (username, password) VALUES (?, ?)''', ('root', bcrypt.hashpw('root'.encode('utf-8'), bcrypt.gensalt())))
    #conn.commit()

user['login']()