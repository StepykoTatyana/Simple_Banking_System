import itertools
import random
import string
import sqlite3

conn = sqlite3.connect('card.s3db')

cur = conn.cursor()
try:
    cur.execute("""CREATE TABLE card(id INTEGER primary key AUTOINCREMENT NOT NULL, number TEXT NOT NULL, 
pin TEXT NOT NULL, balance INTEGER default 0, UNIQUE(number));""")
    conn.commit()
except sqlite3.OperationalError:
    pass


def print_menu():
    print("1. Create an account\n2. Log into account\n0. Exit")


def generator_bs():
    print("Your card has been created\nYour card number:")
    inn = 400000
    bin_bank = ''.join(random.sample(string.digits, 9))
    new_card = str(inn) + str(bin_bank)
    list_num = [int(a) for a in (str(inn) + str(bin_bank))]
    freq_dict = {}
    i = 1
    for u in list_num:
        freq_dict[i] = u
        i += 1
    for a in freq_dict.keys():
        if a % 2 == 1:
            freq_dict[a] = 2 * freq_dict[a]
            if freq_dict[a] > 9:
                freq_dict[a] = freq_dict[a] - 9
    new_list = ''.join([str(a) for a in freq_dict.values()])

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
    pin = random.choice(pins)
    print(pin)
    return pin


def check_balance():
    print()
    print("1. Balance\n2. Log out\n0. Exit")
    choose_add_menu = int(input())
    while choose_add_menu != 0:
        if choose_add_menu == 1:
            print()
            print("Balance: 0")
        elif choose_add_menu == 2:
            print()
            print("You have successfully logged out!")
            break
        print()
        print("1. Balance\n2. Log out\n0. Exit")
        choose_add_menu = int(input())
    return choose_add_menu


def input_card(dictionary_cards):
    print()
    print("Enter your card number:")
    card_for_check = int(input())
    print("Enter your PIN:")
    pin_for_check = input()
    try:
        if dictionary_cards[card_for_check] == pin_for_check:
            print()
            print("You have successfully logged in!")
            return check_balance()
        else:
            print()
            print("Wrong card number or PIN!")
    except KeyError:
        print()
        print("Wrong card number or PIN!")


def main():
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
            if input_card(card_dict) == 0:
                break
        elif choose_menu == 0:
            break
        print()
        print_menu()
        choose_menu = int(input())
    print()
    print("Bye!")


if __name__ == "__main__":
    main()
