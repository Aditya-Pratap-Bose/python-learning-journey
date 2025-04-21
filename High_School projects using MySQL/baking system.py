import mysql.connector


db_connection = mysql.connector.connect(
    host="localhost",        
    user="root",              
    password="####",      
)

cur = db_connection.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS banking_system")
cur.execute("USE banking_system")


cur.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    account_number INT PRIMARY KEY,
    account_holder VARCHAR(255) NOT NULL,
    father_name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    aadhar_number VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0
)
''')


def create_account(account_number, account_holder, father_name, age, gender, aadhar_number, address, phone_number):
    try:
        cur.execute("INSERT INTO accounts (account_number, account_holder, father_name, age, gender, aadhar_number, address, phone_number, balance) VALUES ({}, '{}', '{}', {}, '{}', '{}', '{}', '{}', {})".format(account_number, account_holder, father_name, age, gender, aadhar_number, address, phone_number, 0))
        db_connection.commit()
        print("Account created successfully!")
    except Exception as err:
        print(err, "Error creating account. Please try again.")


def deposit(account_number, amount):
    try:
        cur.execute("SELECT balance FROM accounts WHERE account_number = {}".format(account_number))
        row = cur.fetchone()
        if row:
            new_balance = float(row[0]) + amount 
            cur.execute("UPDATE accounts SET balance = {} WHERE account_number = {}".format(new_balance, account_number))
            db_connection.commit()
            print(f"Deposit successful! New balance: {new_balance}")
        else:
            print("Account not found!")
    except Exception as err:
        print(err, "Error during deposit. Please check your inputs.")


def withdraw(account_number, amount):
    try:
        cur.execute("SELECT balance FROM accounts WHERE account_number = {}".format(account_number))
        row = cur.fetchone()
        if row:
            current_balance = float(row[0]) 
            if current_balance >= amount:
                new_balance = current_balance - amount
                cur.execute("UPDATE accounts SET balance = {} WHERE account_number = {}".format(new_balance, account_number))
                db_connection.commit()
                print(f"Withdrawal successful! New balance: {new_balance}")
            else:
                print("Insufficient funds!")
        else:
            print("Account not found!")
    except Exception as err:
        print(err, "Error during withdrawal. Please check your inputs.")


def show_details(account_number):
    try:
        cur.execute("SELECT * FROM accounts WHERE account_number = {}".format(account_number))
        row = cur.fetchone()
        if row:
            print("Account Number: {}".format(row[0]))
            print("Account Holder: {}".format(row[1]))
            print("Father's Name: {}".format(row[2]))
            print("Age: {}".format(row[3]))
            print("Gender: {}".format(row[4]))
            print("Aadhar Number: {}".format(row[5]))
            print("Address: {}".format(row[6]))
            print("Phone Number: {}".format(row[7]))
            print("Account Balance: {}".format(row[8]))

        else:
            print("Account not found!")
    except Exception as err:
        print(err, "Error fetching account details. Please try again.")


def close():
    db_connection.close()

# Main program
if __name__ == "__main__":
    while True:
        print("\n--- Banking System ---")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Show Account Details")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            account_number = int(input("Enter account number: "))
            account_holder = input("Enter account holder name: ")
            father_name = input("Enter father's name: ")
            age = int(input("Enter age: "))
            gender = input("Enter gender: ")
            aadhar_number = input("Enter Aadhar card number: ")
            address = input("Enter address: ")
            phone_number = input("Enter phone number: ")
            create_account(account_number, account_holder, father_name, age, gender, aadhar_number, address, phone_number)
        
        elif choice == '2':
            account_number = int(input("Enter account number: "))
            amount = float(input("Enter deposit amount: "))
            deposit(account_number, amount)
        
        elif choice == '3':
            account_number = int(input("Enter account number: "))
            amount = float(input("Enter withdrawal amount: "))
            withdraw(account_number, amount)
        
        elif choice == '4':
            account_number = int(input("Enter account number: "))
            show_details(account_number)
        
        elif choice == '5':
            close()
            print("Thank you for using the banking system!")
            break
        
        else:
            print("Invalid choice! Please try again.")
