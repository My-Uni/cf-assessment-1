#   Imports
import datetime
from prettytable import PrettyTable
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

def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            userid   INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer (
            customerid INTEGER PRIMARY KEY AUTOINCREMENT,
            customerusername TEXT NOT NULL UNIQUE,
            forename TEXT NOT NULL,
            surname TEXT,
            dob DATE NOT NULL
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
        CREATE TABLE IF NOT EXISTS transact (
            transactionid INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            date DATE NOT NULL,
            accountid INTEGER NOT NULL,
            reference TEXT NULL,
            FOREIGN KEY(accountid) REFERENCES account(accountid)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account (
            accountid INTEGER PRIMARY KEY AUTOINCREMENT,
            balance REAL NOT NULL DEFAULT 0.00,
            opendate DATE NOT NULL,
            closedate DATE NULL,
            status TEXT NOT NULL DEFAULT "ACTIVE",
            customerid INTEGER NOT NULL,
            FOREIGN KEY(customerid) REFERENCES customer(customerid)
        );
    ''')

#############
#   Menus   #
#############

def _main_menu():
    os.system('clear')
    print("".center(80, "*"))
    print(" MAIN MENU ".center(80, "*"))
    print("".center(80, "*"))

    print('''\n
[1] Customers
[2] Users
[3] Accounts
[4] Transactions
[5] Logout
[6] Logout & Exit
    ''')

    while True:
        user_choice = input()

        try:
            user_choice = int(user_choice)
            print(user_choice)
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
                os.system('clear')
                print('Exiting Program...')
                os._exit(0)
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
[3] View ALL Customer Details
[4] Update Customer Details
[5] Delete Customer
[6] Main Menu
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
                customer['delete']()
                break
            elif user_choice == 6:
                display_menu['main']()
            else:
                print('Please choose a valid option\n')
        except:
            print('Please choose a valid option\n')

def _users_menu():
    os.system('clear')
    print("".center(80, "*"))
    print(" USERS ".center(80, "*"))
    print("".center(80, "*"))

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
    os.system('clear')
    print("".center(80, "*"))
    print(" ACCOUNTS ".center(80, "*"))
    print("".center(80, "*"))

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
    os.system('clear')
    print("".center(80, "*"))
    print(" TRANSACTIONS ".center(80, "*"))
    print("".center(80, "*"))

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
#####################3

def _create_user():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" CREATE USER ".center(80, "*"))
        print("".center(80, "*"))

        username = input('Enter new users username: ')
        password = maskpass.askpass(prompt="Enter new users password: ",mask="*")
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor.execute('''INSERT INTO user (username, password) VALUES (?, ?)''', (username, password))
            conn.commit()
            print(f'\nUser ({username}) created sucessfully')
            time.sleep(1)
            display_menu['users']()
            break
        except:
            print(f'Username ({username}) already exists, try again\n')

def _login():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" SYSTEM LOGIN ".center(80, "*"))
        print("".center(80, "*"))

        username = input('\nEnter username: ')
        password = maskpass.askpass(prompt="Enter password: ",mask="*")
        password = password.encode('utf-8')
        cursor.execute('''SELECT password FROM user WHERE username = ?''', (username,))
        try:
            hashed = cursor.fetchone()[0]
            if bcrypt.checkpw(password, hashed):
                print('\nSucessfully logged in...')
                time.sleep(1)
                display_menu['main']()
                break
            else:
                print('Login failed, try again\n')
        except:
            print('Login failed, try again\n')

def _view_user():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" VIEW USER ".center(80, "*"))
        print("".center(80, "*"))

        username = input('\nEnter users username: ')
        try:
            cursor.execute('''SELECT * FROM user WHERE username = ?''', (username,))
            customer = cursor.fetchone()
            os.system('clear')
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

def _view_all_users():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" VIEW ALL USERS ".center(80, "*"))
        print("".center(80, "*"))

        cursor.execute('''SELECT * FROM user''')
        users = cursor.fetchall()
        
        if users == None:
            print(f'No users exist, try again\n')
            time.sleep(1)
            display_menu['users']()
            break

        tbl = PrettyTable()
        tbl._title = "All Users"
        tbl.field_names = ["ID", "Username", "Password"]

        for user in users:
            tbl.add_row([user[0], user[1], "********"])

        print(f'\n{tbl}')
        
        input('\nPress any button to continue...')
        display_menu['users']()
        
def _update_user():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" UPDATE USER ".center(80, "*"))
        print("".center(80, "*"))

        username = input('\nEnter username: ')
        collumn = input('What would you like to update? : ')
        value = input('Enter new value: ')

        if collumn == 'userid':
            print('You cannot change the userid\n')
            time.sleep(1)
            continue
        elif collumn == 'password':
            value = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())

        try:
            cursor.execute(f'''UPDATE user SET {collumn} = ? WHERE username = ?''', (value, username))
            conn.commit()
            print(f'\nUser ({username}) has been updated successfully\n ')
            time.sleep(1)
            display_menu['users']()
            break
        except:
            print(f'User ({username}) or collum ${collumn} does not exist, try again\n')

def _delete_user():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" DELETE USER ".center(80, "*"))
        print("".center(80, "*"))

        username = input('\nEnter username: ')
        try:
            # Confirm with the user if they would like to delete, if not go back to menu
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

def _create_customer():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" CREATE CUSTOMER ".center(80, "*"))
        print("".center(80, "*"))

        forename = input('\nEnter new customers forename: ')
        lastname = input('Enter new customers last name: ')
        dob = input('Enter new customers date of birth (MM-DD-YYYY): ')
        username = forename[0] + lastname + dob[-2:]
        username = username.lower()
        
        try:
            cursor.execute('''INSERT INTO customer (customerusername, forename, surname, dob) VALUES (?, ?, ?, ?)''', (username, forename, lastname, dob))
            conn.commit()
            print(f'\nCustomer ({username}) created successfully with id {cursor.lastrowid}')
            time.sleep(1)
            display_menu['customers']()
            break
        except Exception as err:
            time.sleep(1)
            print(f'Username ({username}) already exists, try again\n')

def _view_customer():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" VIEW CUSTOMER ".center(80, "*"))
        print("".center(80, "*"))

        customerusername = input('\nEnter customer username: ')
        try:
            cursor.execute('''SELECT * FROM customer WHERE customerusername = ?''', (customerusername,))
            customer = cursor.fetchone()
            os.system('clear')
            print(f'''
Customer ID: {customer[0]}
Customer Username: {customer[1]}
Forename: {customer[2]}
Surname: {customer[3]}
Date of Birth: {customer[4]}
            ''')
            input('\nPress any button to continue...')
            display_menu['customers']()
            break
        except:
            print(f'Customer ({customerusername}) does not exist, try again\n')

def _view_all_customers():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" VIEW ALL CUSTOMERS ".center(80, "*"))
        print("".center(80, "*"))

        cursor.execute('''SELECT * FROM customer''')
        customers = cursor.fetchall()

        if customers == None:
            print(f'No customers exist, try again\n')
            time.sleep(1)
            display_menu['customers']()
            break
        
        tbl = PrettyTable()
        tbl._title = "All Customers"
        tbl.field_names = ["ID", "Username", "Forename", "Surname", "Date of Birth"]

        for customer in customers:
            tbl.add_row([customer[0], customer[1], customer[2], customer[3], customer[4]])

        print(f'\n{tbl}')
        
        input('\nPress any button to continue...')
        display_menu['customers']()

def _update_customer():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" UPDATE CUSTOMER ".center(80, "*"))
        print("".center(80, "*"))

        customerusername = input('\nEnter customer username: ')
        collumn = input('What would you like to update? : ')
        value = input('Enter new value: ')

        if collumn == 'dob':
            try:
                datetime.datetime.strptime(value, '%m-%d-%Y')
            except ValueError:
                print('Incorrect date format, should be MM-DD-YYYY\n')
                time.sleep(1)
                continue
        if collumn == 'customerid':
            print('You cannot change the customerid\n')
            time.sleep(1)
            continue

        try:
            cursor.execute(f'''UPDATE customer SET {collumn} = ? WHERE customerusername = ?''', (value, customerusername))
            conn.commit()
            print(f'\nCustomer ({customerusername}) has been updated successfully\n ')
            time.sleep(1)
            display_menu['customers']()
            break
        except:
            print(f'Customer ({customerusername}) or collum ${collumn} does not exist, try again\n')

def _delete_customer():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" DELETE CUSTOMER ".center(80, "*"))
        print("".center(80, "*"))

        customerusername = input('\nEnter customer username: ')
        try:
            # Confirm with the user if they would like to delete, if not go back to menu
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
            
customer = {
    'create': _create_customer,
    'view': _view_customer,
    'update': _update_customer,
    'viewall': _view_all_customers,
    'delete': _delete_customer
}

#########################
#   Account Functions   #
#########################

def _create_account():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" CREATE ACCOUNT ".center(80, "*"))
        print("".center(80, "*"))

        username = input('\nEnter holder (customer) username: ')

        cursor.execute('''SELECT customerid FROM customer WHERE customerusername = ?''', (username,))
        customerid = cursor.fetchone()
        
        if customerid == None:
            print(f'Customer ({username}) does not exist, try again\n')
            time.sleep(1)
            continue
        customerid = customerid[0]

        opendate = datetime.datetime.now().strftime('%d-%m-%Y')

        try:
            cursor.execute('''INSERT INTO account (customerid, opendate) VALUES (?, ?)''', (customerid, opendate))
            conn.commit()
            print(f'\nAccount ({cursor.lastrowid}) created successfully for customer {username}')
            time.sleep(1)
            display_menu['accounts']()
            break
        except Exception as err:
            print(err)
            print(f'There seems to be an internal error, please try again\n')
            time.sleep(1)

def _view_account():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" VIEW ACCOUNT ".center(80, "*"))
        print("".center(80, "*"))

        accountid = input('\nEnter Account ID: ')
        try:
            cursor.execute('''SELECT account.accountid, account.balance, account.opendate, account.closedate, account.status, customer.customerusername FROM account 
            JOIN customer 
            ON account.customerid = customer.customerid 
            WHERE accountid = ?''', (accountid,))
            account = cursor.fetchone()
            os.system('clear')
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
            print(err)
            print(f'Account ({accountid}) does not exist, try again\n')
            time.sleep(1)

def _view_all_accounts():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" VIEW ALL ACCOUNTS ".center(80, "*"))
        print("".center(80, "*"))

        cursor.execute('''SELECT account.accountid, account.balance, account.opendate, account.closedate, account.status, customer.customerusername FROM account 
        JOIN customer 
        ON account.customerid = customer.customerid''')
        accounts = cursor.fetchall()
        
        if accounts == None:
            print(f'No accounts exist, try again\n')
            time.sleep(1)
            display_menu['accounts']()
            break

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
        os.system('clear')
        print("".center(80, "*"))
        print(" UPDATE ACCOUNT ".center(80, "*"))
        print("".center(80, "*"))

        accountid = input('\nEnter account id: ')
        collumn = input('What would you like to update? : ')
        value = input('Enter new value: ')

        if collumn == 'opendate':
            try:
                datetime.datetime.strptime(value, '%m-%d-%Y')
            except ValueError:
                print('Incorrect date format, should be MM-DD-YYYY\n')
                time.sleep(1)
                continue
        if collumn == 'closedate':
            try:
                datetime.datetime.strptime(value, '%m-%d-%Y')
            except ValueError:
                print('Incorrect date format, should be MM-DD-YYYY\n')
                time.sleep(1)
                continue
        if collumn == 'accountid':
            print('You cannot change the accountid\n')
            time.sleep(1)
            continue

        try:
            cursor.execute(f'''UPDATE account SET {collumn} = ? WHERE accountid = ?''', (value, accountid))
            conn.commit()
            print(f'\nAccount ({accountid}) has been updated successfully\n ')
            time.sleep(1)
            display_menu['accounts']()
            break
        except:
            print(f'Account ({accountid}) or collum ${collumn} does not exist, try again\n')

def _close_account():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" CLOSE ACCOUNT ".center(80, "*"))
        print("".center(80, "*"))

        accountid = input('\nEnter account id: ')
        closedate = datetime.datetime.now().strftime('%d-%m-%Y')

        try:
            # Confirm with the user if they would like to delete, if not go back to menu
            if input(f'\n[IMPORTANT] Do you wish to close this account ({accountid})? (y/n): ').lower() == 'n':
                display_menu['accounts']()
                break

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
    try:
        cursor.execute('''UPDATE account SET balance = balance + ? WHERE accountid = ?''', (amount, accountid,))
        conn.commit()
        time.sleep(1)
        return True
    except Exception as err:
        time.sleep(1)
        return False

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

def _create_transaction():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" CREATE TRANSACTION ".center(80, "*"))
        print("".center(80, "*"))

        accountid = input('\nEnter account id: ')
        amount = input('Enter amount (- if this is a debit transaction, + if this is a credit transaction): ')
        reference = input('Enter reference: ')
        transactiontype = 'DEBIT' if float(amount) < 0 else 'CREDIT'
        transactiondate = datetime.datetime.now().strftime('%d-%m-%Y')

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
            print(err)
            print(f'There seems to be an internal error, please try again\n')
            time.sleep(1)

def _view_account_transactions():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" VIEW ACCOUNT TRANSACTIONS ".center(80, "*"))
        print("".center(80, "*"))

        accountid = input('\nEnter account id: ')

        try:
            cursor.execute('''SELECT * FROM transact WHERE accountid = ?''', (accountid,))
            transactions = cursor.fetchall()
            os.system('clear')

            ## use pretty tables
            tbl = PrettyTable()
            tbl._title = f'Account ({accountid}) Transactions'
            tbl.field_names = ["ID", "Account ID", "Amount", "Type", "Date", "Reference"]

            for transaction in transactions:
                tbl.add_row([transaction[0], transaction[4], transaction[1], transaction[2], transaction[3], transaction[4]])

            print(f'\n{tbl}')
            input('\nPress any button to continue...')
            display_menu['transactions']()
            break
        except Exception as err:
            print(f'Account ({accountid}) does not exist, try again\n')
            time.sleep(1)

def _view_all_transactions():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" VIEW ALL TRANSACTIONS ".center(80, "*"))
        print("".center(80, "*"))

        try:
            cursor.execute('''SELECT * FROM transact''')
            transactions = cursor.fetchall()
            os.system('clear')

            ## use pretty tables
            tbl = PrettyTable()
            tbl._title = f'All Transactions'
            tbl.field_names = ["ID", "Account ID", "Amount", "Type", "Date", "Reference"]

            for transaction in transactions:
                tbl.add_row([transaction[0], transaction[4], transaction[1], transaction[2], transaction[3], transaction[4]])

            print(f'\n{tbl}')
            input('\nPress any button to continue...')
            display_menu['transactions']()
            break
        except Exception as err:
            print(f'There seems to be an internal error, please try again\n')
            time.sleep(1)

def _view_transaction_by_date():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" VIEW TRANSACTION BY DATE ".center(80, "*"))
        print("".center(80, "*"))

        startdate = input('\nEnter start date (DD-MM-YYYY): ')
        enddate = input('Enter end date (DD-MM-YYYY): ')

        try:
            cursor.execute('''SELECT * FROM transact WHERE date BETWEEN ? AND ?''', (startdate, enddate))
            transactions = cursor.fetchall()
            os.system('clear')

            ## use pretty tables
            tbl = PrettyTable()
            tbl._title = f'Transactions between {startdate} and {enddate}'
            tbl.field_names = ["ID", "Account ID", "Amount", "Type", "Date", "Reference"]

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
        os.system('clear')
        print("".center(80, "*"))
        print(" UPDATE TRANSACTION ".center(80, "*"))
        print("".center(80, "*"))

        transactionid = input('\nEnter transaction id: ')

        # get transaction accountid
        cursor.execute('''SELECT * FROM transact WHERE transactionid = ?''', (transactionid,))
        transaction = cursor.fetchone()

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

        try:
            amount = float(input('Enter amount (- if this is a debit transaction, + if this is a credit transaction): '))
            transactiontype = 'DEBIT' if float(amount) < 0 else 'CREDIT'
            
            cursor.execute('''UPDATE transact SET type = ? WHERE transactionid = ?''', ('UPDATED', transactionid))
            if not account['updatebal'](transaction[4], amount):
                print('Transaction failed, please try again\n')
                break
            cursor.execute('''INSERT INTO transact (type, amount, date, accountid, reference) VALUES(?, ?, ?, ?, ?)''', (transactiontype, amount, datetime.datetime.now().strftime('%d-%m-%Y'), transaction[4], f'Updated transaction {transactionid}'))
            conn.commit()
            print(f'\nTransaction ({transactionid}) updated successfully\n')
            time.sleep(1)
            display_menu['transactions']()
            break
        except Exception as err:
            print(err)
            print(f'Transaction ({transactionid}) does not exist, try again\n')
            time.sleep(1)

def _revoke_transaction():
    while True:
        os.system('clear')
        print("".center(80, "*"))
        print(" REVOKE TRANSACTION ".center(80, "*"))
        print("".center(80, "*"))

        transactionid = input('\nEnter transaction id: ')

        cursor.execute('''SELECT type, amount, accountid FROM transact WHERE transactionid = ?''', (transactionid,))
        transaction = cursor.fetchone()

        if transaction is None:
            print(f'Transaction ({transactionid}) does not exist, try again\n')
            time.sleep(1)
            continue
        
        transactiontype = transaction[0]
        if transactiontype == 'DEBIT':
            amount = abs(transaction[1])
            transactiontype = 'CREDIT'
        elif transactiontype == 'CREDIT':
            amount = -abs(transaction[1])
            transactiontype = 'DEBIT'
        else:
            print(f'Transaction ({transactionid}) could not be revoked.\n')
            time.sleep(1)
            display_menu['transactions']()
            break

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
            print(err)
            print(f'Error occured: {err}\n')
            time.sleep(1)

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