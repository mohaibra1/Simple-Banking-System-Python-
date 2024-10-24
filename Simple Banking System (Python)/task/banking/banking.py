# Write your code here
import random, sqlite3

ext = False
bank = {}
balance = 0
logged = False
INN = '400000'
account_number = '493832089'
id_sq = 1
def create_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect('card.s3db')

    # Create a cursor object
    cursor = connection.cursor()

    # Create a table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS card (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number  TEXT NOT NULL,
        pin TEXT NOT NULL,
        balance INTEGER default 0)
    ''')

    # Commit the changes
    connection.commit()

    # Close the connection
    connection.close()

    print("Table created successfully.")


def save_card(card, password):
    global id_sq
    cursor = sqlite3.connect('card.s3db')
    cursor.execute('''
    insert into card (number, pin, balance)
    values (?,?,?)
    ''', (card, password, balance))

    cursor.commit()

    # Close the connection
    cursor.close()
    id_sq += 1
    print("Data inserted successfully.")
def update_info(bal, card):
    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect('card.s3db')

    # Create a cursor object
    cursor = connection.cursor()

    cursor.execute('''
    update card
    set balance = balance + ?
    where number = ?
    ''', (bal, card))

    connection.commit()
    connection.close()
def withdraw(bal, card):
    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect('card.s3db')

    # Create a cursor object
    cursor = connection.cursor()

    cursor.execute('''
    update card
    set balance = balance - ?
    where number = ?
    ''', (bal, card))

    connection.commit()
    connection.close()
def transfer(card, other_card, money):
    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect('card.s3db')

    # Create a cursor object
    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM card WHERE number = ?
        ''', (card,))

    result_1 = cursor.fetchall()
    withdraw(money, card)

    connection.commit()

    update_info(money, other_card)

    connection.close()
    print('Transferred money')

def fetch_info(card):
    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect('card.s3db')

    # Create a cursor object
    cursor = connection.cursor()
    try:
        cursor.execute('''
        SELECT * FROM card WHERE number = ?
        ''', (card,))

        results = cursor.fetchall()

        card = results[0][1]
        pas = results[0][2]
        bal = results[0][3]
        return card, pas, bal
    except:
        print('Wrong card number or PIN!')


def delete_account(card):
    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect('card.s3db')

    # Create a cursor object
    cursor = connection.cursor()

    cursor.execute('''
    delete from card
    where number = ?
    ''', (card,))

    connection.commit()
    connection.close()
def next_card_number():
    global account_number
    connection = sqlite3.connect('card.s3db')
    # Create a cursor object
    cursor = connection.cursor()

    cursor.execute('select * from card')
    results = cursor.fetchall()

    if results:
        last = results[-1]
        acc_num = int(last[1][:len(last[1]) - 1]) + 1
        account_number = str(acc_num)
        return account_number
    else:
        return INN + account_number

def card_generator():
    global account_number
    account_number = next_card_number()
    n = account_number
    check_sum = 0
    num = [*n]
    for i in range(len(num)):
        if i % 2 == 0:
            temp = int(num[i]) * 2 
            num[i] = str(temp)
    num =  list(map(lambda x: int(x) - 9 if int(x) > 9 else int(x) - 0 , num))
    total = 0
    for j in num:
        total += int(j)
    if total % 10 != 0: 
        check_sum = 10 - (total % 10)
    else:
        check_sum = 0
    card_details = str(n) + str(check_sum)
    account_number = int(account_number) 
    account_number += 1
    account_number = str(account_number)
    return card_details

def create_account():
    global account_number, bank, balance
    card_details = card_generator()
    balance = 0
    pas = create_password()
    bank[card_details] = pas
    save_card(card_details, pas)
    return card_details, pas
    
def create_password():
    pas = []
    for i in range(0,4):
        i = random.randint(0,9)
        pas.append(str(i))
    return ''.join(pas)
def log_in(card, password):
    global logged
    if check_card(card):
        results = fetch_info(card)
        if results:
            card_db = results[0]
            password_db = results[1]
            if card == card_db:
                if password == password_db:
                    print('You have successfully logged in!')
                    logged = True
                else:
                    print('Wrong card number or PIN!')
            else:
                print('Wrong card number or PIN!')
        else:
            logged = False
    else:
        print('Wrong card number or PIN!')
    print()
def check_card(card):
    num = [*card]
    c = num.pop(-1)
    for i in range(len(num)):
        if i % 2 == 0:
            temp = int(num[i]) * 2 
            num[i] = str(temp)
    num =  list(map(lambda x: int(x) - 9 if int(x) > 9 else int(x) - 0 , num))
    total = 0
    for j in num:
        total += int(j)
    check_sum = 10 - (total % 10)
    if int(c) == check_sum:
        return True
    else:
        return False
def account(card, pas):
    global logged, ext
    while logged:
        if logged:
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
            choice = int(input())
            print()
            if choice == 5:
                print('You have successfully logged out!')
                logged = False
            elif choice == 1:
                results = fetch_info(card)
                bal = results[2]
                print(f'Your balance is {bal}')
                print()
            elif choice == 2:
                if check_card(card):
                    c = fetch_info(card)
                    if c[1] == pas:
                        income = int(input('Enter income:'))
                        update_info(income, card)
                        print('Income was added!')
                        print()
                    else:
                        print('Wrong card number or PIN!')
                else:
                    print('Wrong card number or PIN!')
            elif choice == 3:
                print('Transfer')
                card_transfer = input('Enter card number: ')
                check = fetch_info(card_transfer)
                if check_card(card_transfer):
                    if check:
                        t = fetch_info(card)
                        money_transfer = int(input('Enter how much money you want to transfer: '))
                        if money_transfer > t[2]:
                            print('Not enough money!')
                        else:
                            transfer(card, card_transfer, money_transfer)
                        pass
                    else:
                        print('Such a card does not exist')
                else:
                    print('Probably you made a mistake in the card number. Please try again!')
                print()
            elif choice == 4:
                if check_card(card):
                    delete_account(card)
                    print('The account has been closed!')
                    break
            elif choice == 0:
                ext = True
                print('Bye!')
                break

def start():
    create_database()
    while True:
        if ext:
            break
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        choice = int(input())
        print()
        if choice == 1:
            created = create_account()
            print('Your card has been created')
            print('Your card number:')
            print(f'{created[0]}')
            print(f'Your card PIN:')
            print(f'{created[1]}')
            print()
        elif choice == 2:
            card = input('Enter your card number: ')
            pas = input('Enter your PIN: ')
            print()
            log_in(card, pas)
            account(card, pas)
            print()
        elif choice == 0:
            print('Bye!')
            break

start()