"""You have created the foundation of our banking system. Now let's take the opportunity to deposit money into an account, make transfers and close an account if necessary.

Now your menu should look like this:

1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
If the user asks for Balance, you should read the balance of the account from the database and output it into the console.

Add income item should allow us to deposit money to the account.

Do transfer item should allow transferring money to another account. You should handle the following errors:

If the user tries to transfer more money than he/she has, output: Not enough money!
If the user tries to transfer money to the same account, output the following message: You can't transfer money to the same account!
If the receiver's card number doesn’t pass the Luhn algorithm, you should output: Probably you made a mistake in the card number. Please try again!
If the receiver's card number doesn’t exist, you should output: Such a card does not exist.
If there is no error, ask the user how much money they want to transfer and make the transaction.
If the user chooses the Close account item, you should delete that account from the database."""

import itertools
import random
import string
import sqlite3


def create_db():
    global conn, cur
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    try:
        cur.execute("""CREATE TABLE card(id INTEGER primary key, number TEXT NOT NULL, 
    pin TEXT NOT NULL, balance INTEGER default 0, UNIQUE(number));""")
        conn.commit()
    except sqlite3.OperationalError:
        pass


def print_menu():
    print("1. Create an account\n2. Log into account\n0. Exit")


def check_bs(card_for_check):
    freq_dict = {}
    i = 1
    for u in card_for_check:
        freq_dict[i] = u
        i += 1
    for a in freq_dict.keys():
        if a % 2 == 1:
            freq_dict[a] = 2 * freq_dict[a]
            if freq_dict[a] > 9:
                freq_dict[a] = freq_dict[a] - 9
    new_list = ''.join([str(a) for a in freq_dict.values()])
    return new_list


def generator_bs():
    print("Your card has been created\nYour card number:")
    inn = 400000
    bin_bank = ''.join(random.sample(string.digits, 9))
    new_card = str(inn) + str(bin_bank)
    list_num = [int(a) for a in (str(inn) + str(bin_bank))]
    new_list = check_bs(list_num)
    for a in range(10):
        list_for_sum = [int(a) for a in new_list + str(a)]
        if sum(list_for_sum) % 10 == 0:
            new_card = int(new_card + str(a))
            break
    print(new_card)
    return new_card


def generator_pin():
    print("Your card PIN:")
    pins = [''.join(x) for x in itertools.permutations('0123456789', 4)]
    pin = str(random.choice(pins))
    print(pin)
    return pin


def check_balance(card_user):
    print()
    print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
    choose_add_menu = int(input())
    while choose_add_menu != 0:
        if choose_add_menu == 1:
            print()
            cur.execute(f"""SELECT balance FROM card WHERE number = '{card_user}'""")
            balance_user = cur.fetchone()[0]
            print(f"Balance: {balance_user}")
        elif choose_add_menu == 2:
            print()
            print("Enter income:")
            income = int(input())
            cur.execute(f"UPDATE card SET balance = balance + {income} WHERE number = '{card_user}'")
            conn.commit()
            print("Income was added!")
        elif choose_add_menu == 3:
            print()
            print("Transfer\nEnter card number:")
            number_card = input()
            number_for_check = ' '.join(number_card).split()
            last_num = number_for_check.pop(-1)
            list_for_check = [int(a) for a in number_for_check]
            new_list = check_bs(list_for_check)
            list_for_sum = [int(a) for a in new_list + str(last_num)]
            if sum(list_for_sum) % 10 == 0:
                try:
                    cur.execute(f"SELECT balance FROM card WHERE number = '{number_card}'")
                    balance_for_transfer = cur.fetchone()[0]
                    print("Enter how much money you want to transfer:")
                    transfer_user = int(input())
                    cur.execute(f"SELECT balance FROM card WHERE number = '{card_user}'")
                    balance_user = cur.fetchone()[0]
                    if transfer_user > balance_user:
                        print("Not enough money!")
                    else:
                        cur.execute(f"UPDATE card SET balance = {transfer_user} WHERE number = '{number_card}'")
                        conn.commit()
                        cur.execute(f"UPDATE card SET balance = balance - {transfer_user} WHERE number = '{card_user}'")
                        conn.commit()
                        print("Success!")
                except TypeError:
                    print("Such a card does not exist.")
            else:
                print("Probably you made a mistake in the card number. Please try again!")

        elif choose_add_menu == 4:
            cur.execute(f"DELETE FROM card WHERE number = '{card_user}'")
            conn.commit()
            print()
            print("The account has been closed!")
            break
        elif choose_add_menu == 5:
            print()
            print("You have successfully logged out!")
            break
        print()
        print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
        choose_add_menu = int(input())
    return choose_add_menu


def input_card():
    print("Enter your card number:")
    card_for_check = input()
    print("Enter your PIN:")
    pin_for_check = input()
    try:
        cur.execute(f"SELECT pin FROM card WHERE number = '{card_for_check}'")
        pin_from_bd = cur.fetchone()[0]
        if pin_from_bd == pin_for_check:
            print()
            print("You have successfully logged in!")
            return check_balance(card_for_check)
        else:
            print()
            print("Wrong card number or PIN!")
    except TypeError:
        print()
        print("Wrong card number or PIN!")


def main_menu():
    card_dict = {}
    print_menu()
    choose_menu = int(input())
    print()
    while choose_menu != 0:
        if choose_menu == 1:
            user_card = generator_bs()
            user_pin = generator_pin()
            card_dict[user_card] = user_pin
            cur.execute(f"""INSERT INTO card(number, pin) 
                           VALUES 
                           ({user_card}, {user_pin})""")
            conn.commit()
        elif choose_menu == 2:
            if input_card() == 0:
                break
        elif choose_menu == 0:
            break
        print()
        print_menu()
        choose_menu = int(input())
    print()


def main():
    create_db()
    main_menu()
    print("Bye!")


if __name__ == "__main__":
    main()
