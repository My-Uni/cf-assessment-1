#################################
#
#   SWE4207 - Assignment 1
#
#   Name: Morgan Dale 
#   Student ID: 2207481
#   Date Updated: 11-01-2023
#
#################################

#   Imports
import datetime
from prettytable import PrettyTable
from termcolor import colored
import sqlite3
import time
import bcrypt
import maskpass
import os

#   Constants
conn = sqlite3.connect('swe4207.db')
cursor = conn.cursor()

#####################
#   SQL Functions   #
#####################

# This function will create all tables nessesary for the program to work, if they do not exist

def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            userid      INTEGER     PRIMARY KEY AUTOINCREMENT,
            username    VARCHAR(15) NOT NULL    UNIQUE,
            password    TEXT        NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer (
            customerid  INTEGER PRIMARY KEY AUTOINCREMENT,
            customerusername VARCHAR(15) NOT NULL UNIQUE,
            forename    VARCHAR(15) NOT NULL,
            surname     VARCHAR(15) NOT NULL,
            dob         DATE        NOT NULL,
            addressid   INTEGER     NOT NULL,
            FOREIGN KEY(addressid) REFERENCES address(addressid)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS address (
            addressid   INTEGER PRIMARY KEY AUTOINCREMENT,
            streetnumber INTEGER,
            firstline   VARCHAR(30) NOT NULL,
            postcode    VARCHAR(10) NOT NULL,
            region      VARCHAR(15) NOT NULL,
            country     VARCHAR(25) NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transact (
            transactionid INTEGER PRIMARY KEY AUTOINCREMENT,
            amount      REAL        NOT NULL,
            type        VARCHAR(10) NOT NULL,
            date        DATE        NOT NULL,
            accountid   INTEGER     NOT NULL,
            reference   VARCHAR(25) NULL,
            FOREIGN KEY(accountid) REFERENCES account(accountid)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account (
            accountid   INTEGER     PRIMARY KEY     AUTOINCREMENT,
            balance     REAL        NOT NULL        DEFAULT 0.00,
            opendate    DATE        NOT NULL,
            closedate   DATE        NULL,
            status      VARCHAR(10) NOT NULL        DEFAULT "ACTIVE",
            customerid  INTEGER NOT NULL,
            FOREIGN KEY(customerid) REFERENCES customer(customerid)
        );
    ''')

#############
#   Menus   #
#############

#   The following Functions will display the corresponding menu (named specifically for each menu type)
#   ONLY comments will be made on the FIRST MENU to describe each function as each menu is repetative

def _main_menu():
    # Clears the screen & display the menu title
    os.system('cls')
    print(colored("".center(80, "*"), 'yellow'))
    print(colored(" MAIN MENU ".center(80, "*"), 'yellow'))
    print(colored("".center(80, "*"), 'yellow'))

    # Displays the menu options
    print('''\n
[1] Customers
[2] Users
[3] Accounts
[4] Transactions
[5] Logout
[6] Logout & Exit
    ''')

    # Loops until a valid option is chosen
    while True:
        user_choice = input()

        # Trys to convert the user input to an integer, if it fails, the user has entered an invalid option
        try:
            user_choice = int(user_choice)

            # If the user has chosen a valid option, then it will call the corresponding function
            if user_choice == 1:
                display_menu['customers']()
                break
            elif user_choice == 2:
                display_menu['users']()
                break
            elif user_choice == 3:
                display_menu['accounts']()
                break
            elif user_choice == 4:
                display_menu['transactions']()
                break
            elif user_choice == 5:
                user['login']()
                break
            elif user_choice == 6:
                os.system('cls')
                print('Exiting Program...')
                os._exit(0)
            else:
                print('Please choose a valid option\n')
        except:
            print('Please choose a valid option\n')

def _customers_menu():
    os.system('cls')
    print(colored("".center(80, "*"), 'yellow'))
    print(colored(" CUSTOMERS ".center(80, "*"), 'yellow'))
    print(colored("".center(80, "*"), 'yellow'))

    print('''\n
[1] Create new Customer
[2] View Customer Details
[3] View ALL Customer Details
[4] Update Customer Details
[5] Update Customer Address Details
[6] Delete Customer
[7] Main Menu
    ''')

    while True:
        user_choice = input()

        try:
            user_choice = int(user_choice)

            if user_choice == 1:
                customer['create']()
                break
            elif user_choice == 2:
                customer['view']()
                break
            elif user_choice == 3:
                customer['viewall']()
                break
            elif user_choice == 4:
                customer['update']()
                break
            elif user_choice == 5:
                customer['updateaddress']()
                break
            elif user_choice == 6:
                customer['delete']()
                break
            elif user_choice == 7:
                display_menu['main']()
            else:
                print('Please choose a valid option\n')
        except:
            print('Please choose a valid option\n')

def _users_menu():
    os.system('cls')
    print(colored("".center(80, "*"), 'yellow'))
    print(colored(" USERS ".center(80, "*"), 'yellow'))
    print(colored("".center(80, "*"), 'yellow'))

    print('''\n
[1] Create new User
[2] View User Details
[3] View ALL User Details
[4] Update User Details
[5] Delete User
[6] Main Menu
    ''')

    while True:
        user_choice = input()

        try:
            user_choice = int(user_choice)

            if user_choice == 1:
                user['create']()
                break
            elif user_choice == 2:
                user['view']()
                break
            elif user_choice == 3:
                user['viewall']()
                break
            elif user_choice == 4:
                user['update']()
                break
            elif user_choice == 5:
                user['delete']()
                break
            elif user_choice == 6:
                display_menu['main']()
                break
            else:
                print('Please choose a valid option\n')
        except:
            print('Please choose a valid option\n')

def _accounts_menu():
    os.system('cls')
    print(colored("".center(80, "*"), 'yellow'))
    print(colored(" ACCOUNTS ".center(80, "*"), 'yellow'))
    print(colored("".center(80, "*"), 'yellow'))

    print('''\n
[1] Create new Account
[2] View Account Details
[3] View ALL Account Details
[4] Update Account Details
[5] Close Account
[6] Main Menu
    ''')

    while True:
        user_choice = input()

        try:
            user_choice = int(user_choice)

            if user_choice == 1:
                account['create']()
                break
            elif user_choice == 2:
                account['view']()
                break
            elif user_choice == 3:
                account['viewall']()
                break
            elif user_choice == 4:
                account['update']()
                break
            elif user_choice == 5:
                account['delete']()
                break
            elif user_choice == 6:
                display_menu['main']()
                break
            else:
                print('Please choose a valid option\n')
        except:
            print('Please choose a valid option\n')

def _transactions_menu():
    os.system('cls')
    print(colored("".center(80, "*"), 'yellow'))
    print(colored(" TRANSACTIONS ".center(80, "*"), 'yellow'))
    print(colored("".center(80, "*"), 'yellow'))

    print('''\n
[1] Create new Transaction
[2] View Account Transactions
[3] View ALL Transactions
[4] View Transactions by Date
[5] Update Transaction Details
[6] Revoke Transaction
[7] Main Menu
    ''')

    while True:
        user_choice = input()

        try:
            user_choice = int(user_choice)

            if user_choice == 1:
                transaction['create']()
                break
            elif user_choice == 2:
                transaction['viewaccount']()
                break
            elif user_choice == 3:
                transaction['viewall']()
                break
            elif user_choice == 4:
                transaction['viewdate']()
                break
            elif user_choice == 5:
                transaction['update']()
                break
            elif user_choice == 6:
                transaction['revoke']()
                break
            elif user_choice == 7:
                display_menu['main']()
                break
            else:
                print('Please choose a valid option\n')
        except:
            print('Please choose a valid option\n')

display_menu = {
    'main': _main_menu,
    'customers': _customers_menu,
    'users': _users_menu,
    'accounts': _accounts_menu,
    'transactions': _transactions_menu
}

######################
#   User Functions   #
######################

# The following functions are specific to user case scenarios, again the functions are named accordingly
# Most of the repetitive code will only be commented in the first function

def _create_user():
    while True:
        # Clears the screen and display the menu title
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" CREATE USER ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        # Asks the user for the new users username and password
        username = input('Enter new users username: ')
        password = maskpass.askpass(prompt="Enter new users password: ",mask="*")
        # Hash's the password using bcrypt, this is a one way encryption so the password cannot be decrypted
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Inserts the new user into the database
        try:
            cursor.execute('''INSERT INTO user (username, password) VALUES (?, ?)''', (username, password))
            print(conn.commit())
            print(f'\nUser ({username}) created sucessfully')
            time.sleep(1)
            display_menu['users']()
            break
        except:
            # If the username already exists, the database will throw an error, this will be caught and the user will be asked to try again
            print(f'Username ({username}) already exists, try again\n')
            time.sleep(1)

def _login():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'magenta'))
        print(colored(" SYSTEM LOGIN ".center(80, "*"), 'magenta'))
        print(colored("".center(80, "*"), 'magenta'))

        username = input('\nEnter username: ')
        password = maskpass.askpass(prompt="Enter password: ",mask="*")
        password = password.encode('utf-8')
        cursor.execute('''SELECT password FROM user WHERE username = ?''', (username,))
        try:
            # Checks the password entered against the hashed password in the database
            hashed = cursor.fetchone()[0]
            if bcrypt.checkpw(password, hashed):
                print('\nSucessfully logged in...')
                time.sleep(1)
                display_menu['main']()
                break
            else:
                print('Login failed, try again\n')
                time.sleep(1)
        except:
            print('Login failed, try again\n')
            time.sleep(1)

def _view_user():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" VIEW USER ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        username = input('\nEnter users username: ')
        try:
            # Selects the user from the database and display the details, grabs all the details from the user table
            cursor.execute('''SELECT * FROM user WHERE username = ?''', (username,))
            customer = cursor.fetchone()
            os.system('cls')
            print(colored("".center(80, "*"), 'cyan'))
            print(colored(" VIEW USER ".center(80, "*"), 'cyan'))
            print(colored("".center(80, "*"), 'cyan'))
            print(f'''
User ID: {customer[0]}
Username: {customer[1]}
Password: ********
            ''')
            input('\nPress any button to continue...')
            display_menu['users']()
            break
        except:
            print(f'User ({username}) does not exist, try again\n')
            time.sleep(1)

def _view_all_users():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" VIEW ALL USERS ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        # Selects all the users from the database
        cursor.execute('''SELECT * FROM user''')
        users = cursor.fetchall()
        
        # If there are no users in the database, the users variable will be None, this will be caught and the user will be asked to try again
        if users == None:
            print(f'No users exist, try again\n')
            time.sleep(1)
            display_menu['users']()
            break

        # Displays the users in a table using PrettyTable
        tbl = PrettyTable()
        tbl._title = "All Users"
        tbl.field_names = ["ID", "Username", "Password"]

        # Loops through the users and add them to the pretty table
        for user in users:
            tbl.add_row([user[0], user[1], "********"])

        print(f'\n{tbl}')
        
        input('\nPress any button to continue...')
        display_menu['users']()
        
def _update_user():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" UPDATE USER ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        username = input('\nEnter username: ')
        collumn = input('What would you like to update? : ')
        value = input('Enter new value: ')

        # If the user tries to update the userid or password, the password will be hashed using bcrypt, and the userid will be ignored
        if collumn == 'userid':
            print('You cannot change the userid\n')
            time.sleep(1)
            continue
        elif collumn == 'password':
            value = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())

        # Updates the user in the database
        try:
            cursor.execute(f'''UPDATE user SET {collumn} = ? WHERE username = ?''', (value, username))
            conn.commit()
            print(f'\nUser ({username}) has been updated successfully\n ')
            time.sleep(1)
            display_menu['users']()
            break
        except:
            print(f'User ({username}) or collum ${collumn} does not exist, try again\n')
            time.sleep(1)

def _delete_user():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" DELETE USER ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        username = input('\nEnter username: ')
        try:
            # Confirms with the user if they would like to delete, if not go back to menu
            if input(f'\n[IMPORTANT] Do you wish to delete this user ({username})? (y/n): ').lower() == 'n':
                display_menu['users']()
                break

            cursor.execute('''DELETE FROM user WHERE username = ?''', (username,))
            conn.commit()
            print(f'\nUser ({username}) has been deleted successfully\n ')
            time.sleep(1)
            display_menu['users']()
            break
        except:
            print(f'User ({username}) does not exist, try again\n')
            time.sleep(1)

# Dictionary of user functions
user = {
    'create': _create_user,
    'login': _login,
    'view': _view_user,
    'viewall': _view_all_users,
    'update': _update_user,
    'delete': _delete_user
} 

##########################
#   Customer Functions   #
##########################

# The following functions are specific to customer case scenarios, again the functions are named accordingly
# Most of the repetitive code will only be commented in the first function

def _create_customer():
    while True:
        # Clears the screen and display the menu title
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" CREATE CUSTOMER ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        # Asks for customer details
        forename = input('\nEnter new customers forename: ')
        lastname = input('Enter new customers last name: ')
        dob = input('Enter new customers date of birth (DD-MM-YYYY): ')

        # Asks for address details
        print('''
Please enter the following address details:
        ''')
        addressline1 = input('Address Line 1: ')
        streetnumber = input('Street Number: ')
        region = input('Region: ')
        country = input('Country: ')
        postcode = input('Postcode: ')

        # Creates a username from the first digit of the forename, the entire surname and the last two digits of the year of dob
        username = forename[0] + lastname + dob[-2:]
        username = username.lower()
        
        # Inserts the address and customer into the database
        try:
            cursor.execute('''INSERT INTO address (firstline, streetnumber, region, country, postcode) VALUES (?, ?, ?, ?, ?)''', (addressline1, streetnumber, region, country, postcode))
            conn.commit()
            cursor.execute('''INSERT INTO customer (customerusername, forename, surname, dob, addressid) VALUES (?, ?, ?, ?, ?)''', (username, forename, lastname, dob, cursor.lastrowid))
            conn.commit()
            print(f'\nCustomer ({username}) created successfully with id {cursor.lastrowid}')
            time.sleep(1)
            display_menu['customers']()
            break
        except Exception as err:
            print(err)
            print(f'Username ({username}) already exists, try again\n')
            time.sleep(1)

def _view_customer():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" VIEW CUSTOMER ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        customerusername = input('\nEnter customer username: ')
        try:
            # Selects the customer from the database, and join the address table to get the full address
            cursor.execute('''
            SELECT Customer.customerid, Customer.customerusername, Customer.forename, Customer.surname, Customer.dob, Address.firstline, Address.region, Address.country, Address.postcode
            FROM Customer
            JOIN Address ON Customer.addressid = Address.addressid
            WHERE Customer.customerusername = ?
            ''', (customerusername,))
            customer = cursor.fetchone()
            os.system('cls')
            print(colored("".center(80, "*"), 'cyan'))
            print(colored(" VIEW CUSTOMER ".center(80, "*"), 'cyan'))
            print(colored("".center(80, "*"), 'cyan'))

            # Prints the customer details, including Full Address
            print(f'''
Customer ID: {customer[0]}
Customer Username: {customer[1]}
Forename: {customer[2]}
Surname: {customer[3]}
Date of Birth: {customer[4]}
            ''')
            print(f'Full Address: {customer[5]}, {customer[6]}, {customer[7]}, {customer[8]}')

            input('\nPress any button to continue...')
            display_menu['customers']()
            break
        except Exception as err:
            print(err)
            print(f'Customer ({customerusername}) does not exist, try again\n')
            time.sleep(1)

def _view_all_customers():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" VIEW ALL CUSTOMERS ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        # Selects all customers from the database, and join the address table to get the full address
        cursor.execute('''
        SELECT Customer.customerid, Customer.customerusername, Customer.forename, Customer.surname, Customer.dob, Address.firstline, Address.region, Address.country, Address.postcode
        FROM Customer
        JOIN Address ON Customer.addressid = Address.addressid
        ''')
        customers = cursor.fetchall()

        if customers == None:
            print(f'No customers exist, try again\n')
            time.sleep(1)
            display_menu['customers']()
            break

        # Prints the customer details, including Full Address, using PrettyTable
        tbl = PrettyTable()
        tbl._title = "All Customers"
        tbl.field_names = ["ID", "Username", "Forename", "Surname", "Date of Birth", "Full Address"]

        # Loops through the customers and add them to the pretty table
        for customer in customers:
            tbl.add_row([customer[0], customer[1], customer[2], customer[3], customer[4], f'{customer[5]}, {customer[6]}, {customer[7]}, {customer[8]}'])

        print(f'\n{tbl}')
        
        input('\nPress any button to continue...')
        display_menu['customers']()

def _update_customer_address():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" UPDATE CUSTOMER ADDRESS ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        customerusername = input('\nEnter customer username: ')
        collumn = input('What would you like to update? : ')
        value = input('Enter new value: ')

        # Checks if the user is trying to change the addressid, if they are then ignore it
        if collumn == 'addressid':
            print('You cannot change the addressid\n')
            time.sleep(1)
            continue

        # Updates the address in the database
        try:
            cursor.execute(f'''UPDATE address SET {collumn} = ? WHERE addressid = (SELECT addressid FROM customer WHERE customerusername = ?)''', (value, customerusername))
            conn.commit()
            print(f'\nCustomer ({customerusername}) address updated successfully')
            time.sleep(1)
            display_menu['customers']()
            break
        except Exception as err:
            print(f'Customer ({customerusername}) does not exist, try again\n')
            time.sleep(1)

def _update_customer():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" UPDATE CUSTOMER ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        customerusername = input('\nEnter customer username: ')
        collumn = input('What would you like to update? : ')
        value = input('Enter new value: ')

        # Checks if the user is trying to change the customerid, if they are then ignore it. Also check if the date is in the correct format
        if collumn == 'dob':
            try:
                datetime.datetime.strptime(value, '%m-%d-%Y')
            except ValueError:
                print('Incorrect date format, should be DD-MM-YYYY\n')
                time.sleep(1)
                continue
        if collumn == 'customerid':
            print('You cannot change the customerid\n')
            time.sleep(1)
            continue

        # Updates the customer in the database
        try:
            cursor.execute(f'''UPDATE customer SET {collumn} = ? WHERE customerusername = ?''', (value, customerusername))
            conn.commit()
            print(f'\nCustomer ({customerusername}) has been updated successfully\n ')
            time.sleep(1)
            display_menu['customers']()
            break
        except:
            print(f'Customer ({customerusername}) or collum ${collumn} does not exist, try again\n')
            time.sleep(1)

def _delete_customer():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" DELETE CUSTOMER ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        customerusername = input('\nEnter customer username: ')

        # Deletes the customer from the database
        try:
            # Confirms with the user if they would like to delete, if not go back to menu
            if input(f'\n[IMPORTANT] Do you wish to delete this customer ({customerusername})? (y/n): ').lower() == 'n':
                display_menu['accounts']()
                break

            cursor.execute('''DELETE FROM customer WHERE customerusername = ?''', (customerusername,))
            conn.commit()
            print(f'\nCustomer ({customerusername}) has been deleted successfully\n ')
            time.sleep(1)
            display_menu['customers']()
            break
        except:
            print(f'Customer ({customerusername}) does not exist, try again\n')
            time.sleep(1)
            
# Dictionary of functions for the customer menu
customer = {
    'create': _create_customer,
    'view': _view_customer,
    'update': _update_customer,
    'viewall': _view_all_customers,
    'delete': _delete_customer,
    'updateaddress': _update_customer_address
}

#########################
#   Account Functions   #
#########################

# The following functions are specific to account case scenarios, again the functions are named accordingly
# Most of the repetitive code will only be commented in the first function

def _create_account():
    while True:
        # Clears the screen and print the menu title
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" CREATE ACCOUNT ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        # Gets the customer username and check if it exists
        username = input('\nEnter holder (customer) username: ')

        cursor.execute('''SELECT customerid FROM customer WHERE customerusername = ?''', (username,))
        customerid = cursor.fetchone()
        
        if customerid == None:
            print(f'Customer ({username}) does not exist, try again\n')
            time.sleep(1)
            continue
        customerid = customerid[0]

        # Gets the current date (open date) and insert the account into the database
        opendate = datetime.datetime.now().strftime('%d-%m-%Y')

        try:
            cursor.execute('''INSERT INTO account (customerid, opendate) VALUES (?, ?)''', (customerid, opendate))
            conn.commit()
            print(f'\nAccount ({cursor.lastrowid}) created successfully for customer {username}')
            time.sleep(1)
            display_menu['accounts']()
            break
        except Exception as err:
            print(f'There seems to be an internal error, please try again\n')
            time.sleep(1)

def _view_account():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" VIEW ACCOUNT ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        accountid = input('\nEnter Account ID: ')

        # Gets the account from the database and print it, along with the customer username
        try:
            cursor.execute('''SELECT account.accountid, account.balance, account.opendate, account.closedate, account.status, customer.customerusername 
            FROM account 
            JOIN customer ON account.customerid = customer.customerid 
            WHERE accountid = ?''', (accountid,))
            account = cursor.fetchone()
            os.system('cls')
            print(colored("".center(80, "*"), 'cyan'))
            print(colored(" VIEW ACCOUNT ".center(80, "*"), 'cyan'))
            print(colored("".center(80, "*"), 'cyan'))

            print(f'''
Account ID: {account[0]}
Balance: {account[1]}
Open Date: {account[2]}
Closed Date: {account[3]}
Status: {account[4]}
Account Holder: {account[5]}
            ''')
            input('\nPress any button to continue...')
            display_menu['accounts']()
            break
        except Exception as err:
            print(f'Account ({accountid}) does not exist, try again\n')
            time.sleep(1)

def _view_all_accounts():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" VIEW ALL ACCOUNTS ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        # Gets all the accounts from the database and print them, along with the customer username
        cursor.execute('''SELECT account.accountid, account.balance, account.opendate, account.closedate, account.status, customer.customerusername 
        FROM account 
        JOIN customer ON account.customerid = customer.customerid''')
        accounts = cursor.fetchall()
        
        # Checks if there are any accounts, if not go back to the menu
        if accounts == None:
            print(f'No accounts exist, try again\n')
            time.sleep(1)
            display_menu['accounts']()
            break

        # Creates a table and add the accounts to it, using PrettyTable
        tbl = PrettyTable()
        tbl._title = "All Accounts"
        tbl.field_names = ["ID", "Balance", "Open Date", "Closed Date", "Status", "Account Holder"]

        for account in accounts:
            tbl.add_row([account[0], account[1], account[2], account[3], account[4], account[5]])

        print(f'\n{tbl}')
        
        input('\nPress any button to continue...')
        display_menu['accounts']()

def _update_account():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" UPDATE ACCOUNT ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        accountid = input('\nEnter account id: ')
        collumn = input('What would you like to update? : ')
        value = input('Enter new value: ')

        # Checks if user is trying to change accountid, if so then ignore it. Also checks if the date is in the correct format
        if collumn == 'opendate':
            try:
                datetime.datetime.strptime(value, '%m-%d-%Y')
            except ValueError:
                print('Incorrect date format, should be DD-MM-YYYY\n')
                time.sleep(1)
                continue
        if collumn == 'closedate':
            try:
                datetime.datetime.strptime(value, '%m-%d-%Y')
            except ValueError:
                print('Incorrect date format, should be DD-MM-YYYY\n')
                time.sleep(1)
                continue
        if collumn == 'accountid':
            print('You cannot change the accountid\n')
            time.sleep(1)
            continue

        # Updates the account in the database
        try:
            cursor.execute(f'''UPDATE account SET {collumn} = ? WHERE accountid = ?''', (value, accountid))
            conn.commit()
            print(f'\nAccount ({accountid}) has been updated successfully\n ')
            time.sleep(1)
            display_menu['accounts']()
            break
        except:
            print(f'Account ({accountid}) or collum ${collumn} does not exist, try again\n')
            time.sleep(1)

def _close_account():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" CLOSE ACCOUNT ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        accountid = input('\nEnter account id: ')
        closedate = datetime.datetime.now().strftime('%d-%m-%Y')

        try:
            # Confirms with the user if they would like to delete, if not go back to menu
            if input(f'\n[IMPORTANT] Do you wish to close this account ({accountid})? (y/n): ').lower() == 'n':
                display_menu['accounts']()
                break

            # Instead of using DELETE, we will just mark the account as closed for auditing purposes
            cursor.execute('''UPDATE account SET status = ?, closedate = ? WHERE accountid = ?''', ('INACTIVE', closedate, accountid,))
            conn.commit()
            print(f'\nAccount ({accountid}) has been closed successfully\n ')
            time.sleep(1)
            display_menu['accounts']()
            break
        except Exception as err:
            print(f'Account ({accountid}) does not exist, try again\n')
            time.sleep(1)

def _update_balance(accountid, amount):
    # Updates the balance of the account, used for transactions
    try:
        cursor.execute('''UPDATE account SET balance = balance + ? WHERE accountid = ?''', (amount, accountid,))
        conn.commit()
        return True
    except Exception as err:
        return False

# Dictionary of account functions
account = {
    'create': _create_account,
    'view': _view_account,
    'viewall': _view_all_accounts,
    'update': _update_account,
    'delete': _close_account,
    'updatebal': _update_balance
}

#############################
#   Transaction Functions   #
#############################

# The following functions are specific to transaction case scenarios, again the functions are named accordingly
# Most of the repetitive code will only be commented in the first function

def _create_transaction():
    while True:
        # Clears the screen and prints the title
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" CREATE TRANSACTION ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        # Gets the account id and amount from the user, also gets the reference and transaction type
        accountid = input('\nEnter account id: ')
        amount = input('Enter amount (- if this is a debit transaction, + if this is a credit transaction): ')
        reference = input('Enter reference: ')
        transactiontype = 'DEBIT' if float(amount) < 0 else 'CREDIT'
        transactiondate = datetime.datetime.now().strftime('%d-%m-%Y')

        # Updates the account balance, if it successfuly does that then inserts the transaction into transact
        try:
            if not account['updatebal'](accountid, amount):
                print('Transaction failed, please try again\n')
                break
            cursor.execute('''INSERT INTO transact (accountid, amount, type, date, reference) VALUES (?, ?, ?, ?, ?)''', (accountid, amount, transactiontype, transactiondate, reference))
            conn.commit()
            print(f'\nTransaction ({cursor.lastrowid}) created successfully for account {accountid}')
            time.sleep(1)
            display_menu['transactions']()
            break
        except Exception as err:
            print(f'There seems to be an internal error, please try again\n')
            time.sleep(1)

def _view_account_transactions():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" VIEW ACCOUNT TRANSACTIONS ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        accountid = input('\nEnter account id: ')

        # Gets all the transactions for the account and prints them out
        try:
            cursor.execute('''SELECT * FROM transact WHERE accountid = ?''', (accountid,))
            transactions = cursor.fetchall()
            os.system('cls')
            print(colored("".center(80, "*"), 'cyan'))
            print(colored(" VIEW ACCOUNT TRANSACTIONS ".center(80, "*"), 'cyan'))
            print(colored("".center(80, "*"), 'cyan'))

            # Uses PrettyTable to print out transaction information
            tbl = PrettyTable()
            tbl._title = f'Account ({accountid}) Transactions'
            tbl.field_names = ["ID", "Account ID", "Amount", "Type", "Date", "Reference"]

            # Loops through all transactions, adding them to the table
            for transaction in transactions:
                tbl.add_row([transaction[0], transaction[4], transaction[1], transaction[2], transaction[3], transaction[5]])

            print(f'\n{tbl}')
            input('\nPress any button to continue...')
            display_menu['transactions']()
            break
        except Exception as err:
            print(f'Account ({accountid}) does not exist, try again\n')
            time.sleep(1)

def _view_all_transactions():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" VIEW ALL TRANSACTIONS ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        # Gets all transactions and prints them out
        try:
            cursor.execute('''SELECT * FROM transact''')
            transactions = cursor.fetchall()
            os.system('cls')
            print(colored("".center(80, "*"), 'cyan'))
            print(colored(" VIEW ALL TRANSACTIONS ".center(80, "*"), 'cyan'))
            print(colored("".center(80, "*"), 'cyan'))

            # Again, uses PrettyTable to print out transaction information
            tbl = PrettyTable()
            tbl._title = f'All Transactions'
            tbl.field_names = ["ID", "Account ID", "Amount", "Type", "Date", "Reference"]

            # Loops through all transactions, adding them to the table
            for transaction in transactions:
                tbl.add_row([transaction[0], transaction[4], transaction[1], transaction[2], transaction[3], transaction[5]])

            print(f'\n{tbl}')
            input('\nPress any button to continue...')
            display_menu['transactions']()
            break
        except Exception as err:
            print(f'There seems to be an internal error, please try again\n')
            time.sleep(1)

def _view_transaction_by_date():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" VIEW TRANSACTION BY DATE ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        # Gets the start and end date from the user
        startdate = input('\nEnter start date (DD-MM-YYYY): ')
        enddate = input('Enter end date (DD-MM-YYYY): ')

        # Gets all transactions between the start and end date and prints them out
        try:
            cursor.execute('''SELECT * FROM transact WHERE date BETWEEN ? AND ?''', (startdate, enddate))
            transactions = cursor.fetchall()
            os.system('cls')
            print(colored("".center(80, "*"), 'cyan'))
            print(colored(" VIEW TRANSACTION BY DATE ".center(80, "*"), 'cyan'))
            print(colored("".center(80, "*"), 'cyan'))

            # Once again, uses PrettyTable to print out transaction information
            tbl = PrettyTable()
            tbl._title = f'Transactions between {startdate} and {enddate}'
            tbl.field_names = ["ID", "Account ID", "Amount", "Type", "Date", "Reference"]

            # Loops through all transactions, adding them to the table
            for transaction in transactions:
                tbl.add_row([transaction[0], transaction[4], transaction[1], transaction[2], transaction[3], transaction[4]])

            print(f'\n{tbl}')
            input('\nPress any button to continue...')
            display_menu['transactions']()
            break
        except Exception as err:
            print(f'There seems to be an internal error, please try again\n')
            time.sleep(1)

def _update_transaction():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" UPDATE TRANSACTION ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        transactionid = input('\nEnter transaction id: ')

        # Gets the transactionid
        cursor.execute('''SELECT * FROM transact WHERE transactionid = ?''', (transactionid,))
        transaction = cursor.fetchone()

        # Updates the account balance based off wether this transaction is CREDIT or DEBIT
        if transaction[2] == 'CREDIT':
            if not account['updatebal'](transaction[4], -abs(transaction[1])):
                print('Transaction failed, please try again\n')
                break
        elif transaction[2] == 'DEBIT':
            if not account['updatebal'](transaction[4], abs(transaction[1])):
                print('Transaction failed, please try again\n')
                break
        else:
            print(f'Transaction ({transactionid}) has already been updated or revoked!\n')
            time.sleep(1)
            display_menu['transactions']()

        # Gets the new amount and updates the transaction
        try:
            # Gets the new amount, along with it's type
            amount = float(input('Enter amount (- if this is a debit transaction, + if this is a credit transaction): '))
            transactiontype = 'DEBIT' if float(amount) < 0 else 'CREDIT'
            
            # Updates the previous transaction
            cursor.execute('''UPDATE transact SET type = ? WHERE transactionid = ?''', ('UPDATED', transactionid))
            if not account['updatebal'](transaction[4], amount):
                print('Transaction failed, please try again\n')
                break
            # Inserts a new transaction with the new amount
            cursor.execute('''INSERT INTO transact (type, amount, date, accountid, reference) VALUES(?, ?, ?, ?, ?)''', (transactiontype, amount, datetime.datetime.now().strftime('%d-%m-%Y'), transaction[4], f'Updated transaction {transactionid}'))
            conn.commit()
            print(f'\nTransaction ({transactionid}) updated successfully\n')
            time.sleep(1)
            display_menu['transactions']()
            break
        except Exception as err:
            print(f'Transaction ({transactionid}) does not exist, try again\n')
            time.sleep(1)

def _revoke_transaction():
    while True:
        os.system('cls')
        print(colored("".center(80, "*"), 'cyan'))
        print(colored(" REVOKE TRANSACTION ".center(80, "*"), 'cyan'))
        print(colored("".center(80, "*"), 'cyan'))

        transactionid = input('\nEnter transaction id: ')

        # Gets the transactionid
        cursor.execute('''SELECT type, amount, accountid FROM transact WHERE transactionid = ?''', (transactionid,))
        transaction = cursor.fetchone()

        # If there is no transaction, it will print out an error message
        if transaction is None:
            print(f'Transaction ({transactionid}) does not exist, try again\n')
            time.sleep(1)
            continue
        
        # Update the amount  based off wether this transaction is CREDIT or DEBIT
        transactiontype = transaction[0]
        if transactiontype == 'DEBIT':
            amount = abs(transaction[1])
            transactiontype = 'CREDIT'
        elif transactiontype == 'CREDIT':
            amount = -abs(transaction[1])
            transactiontype = 'DEBIT'
        else: # If the transaction has already been updated or revoked, it will print out an error message
            print(f'Transaction ({transactionid}) could not be revoked.\n')
            time.sleep(1)
            display_menu['transactions']()
            break

        # Updates the account balance and the transaction, along with inserting a new transaction
        try:
            if not account['updatebal'](transaction[2], amount):
                print('Transaction failed, please try again\n')
                break
            cursor.execute('''UPDATE transact SET type = ? WHERE transactionid = ?''', ('REVOKED', transactionid))
            cursor.execute('''INSERT INTO transact (type, amount, date, accountid, reference) VALUES(?, ?, ?, ?, ?)''', (transactiontype, amount, datetime.datetime.now().strftime('%d-%m-%Y'), transaction[2], f'Revoked transaction {transactionid}'))
            conn.commit()
            print(f'\nTransaction ({transactionid}) revoked successfully\n')
            time.sleep(1)
            display_menu['transactions']()
            break
        except Exception as err:
            print(f'Error occured: {err}\n')
            time.sleep(1)

# Dictionary of all the transactional functions
transaction = {
    'create': _create_transaction,
    'viewaccount': _view_account_transactions,
    'viewall': _view_all_transactions,
    'viewdate': _view_transaction_by_date,
    'update': _update_transaction,
    'revoke': _revoke_transaction
}

####################
#   Initializing   #
####################

#   Create Tables in the case that this is a fresh install
create_tables()

#   Default account, only run if it is a fresh install
cursor.execute('''SELECT * FROM user WHERE username = ?''', ('root',))
rootuser = cursor.fetchone()
if rootuser == None:
    cursor.execute('''INSERT INTO user (username, password) VALUES (?, ?)''', ('root', bcrypt.hashpw('root'.encode('utf-8'), bcrypt.gensalt())))
    conn.commit()

user['login']()