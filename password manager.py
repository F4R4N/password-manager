import random
import string
from passlib.hash import pbkdf2_sha512
import sqlite3

# color table
ENDC = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
YELLOW = '\033[93m'

cnx = sqlite3.connect('password.db')

special_chars = [" ", "!", "\"", "\'", "#", "$", "%", "&", "\'", "(", ")", "*", "=", ",", "-", ".", "/", ":", ";",
                 "<", ">", "?", "@", "\\", "[", "]", "^", "_", "`", "{", "}", "|", "~", "+"]
all_chars = list(string.ascii_lowercase[:26]) + list(string.ascii_uppercase[:26]) + \
            list(str(string.digits[:10])) + special_chars


def initialize():
    cursor = cnx.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS random (name VARCHAR (20), description VARCHAR(50), user VARCHAR(30), "
        "password VARCHAR(255) NOT NULL PRIMARY KEY)")
    cnx.commit()


initialize()


def main_menu():
    while True:
        try:
            main_input = int(input(f"\n{BLUE}1.random password\n2.database history\n3.EXIT\n{ENDC}: "))
            if main_input == 1:
                random_pass_func()
            elif main_input == 2:
                db_history()
            elif main_input == 3:
                exit()
            else:
                print(f"{RED}Invalid Entry !!{ENDC}")
                break
        except ValueError:
            print(f"{RED}Invalid Entry !!{ENDC}")
            break


def random_pass_func():
    while True:
        try:
            rand_input = int(input(f"\n{BLUE}1.full random password\n2.choose the length\n3.Main Menu\n{ENDC}: "))
            if rand_input == 1:
                full_rand()
            elif rand_input == 2:
                choose_length()
            elif rand_input == 3:
                main_menu()
            else:
                print(f"{RED}Invalid Entry !!{ENDC}")
                break
        except ValueError:
            print(f"{RED}Invalid Entry !!{ENDC}")
            break


def full_rand():
    random_pass_1 = random.sample(all_chars, random.randint(14, 25))
    random_pass_2 = random.sample(random_pass_1, len(random_pass_1))
    random_pass_3 = random.sample(random_pass_2, len(random_pass_2))
    random_pass_4_last = random.sample(random_pass_3, len(random_pass_3))
    global all_str
    all_str = ""
    all_str = all_str.join(random_pass_4_last)
    print(F"{BLUE}your password :{ENDC}\n" + all_str)
    # for char in random_pass_4_last:
    #     print(char, end="")
    #

    hash_save_menu()


def hash_save_menu():
    while True:
        try:
            choice = int(input(f"\n{BLUE}1.Hash The Password\n2.Save To Database\n3.Main Menu\n{ENDC}: "))
            if choice == 1:
                hash_pass()
            elif choice == 2:
                save_db()
            elif choice == 3:
                main_menu()
            else:
                print(f"{RED}Invalid Entry !!{ENDC}")
                break
        except ValueError:
            print(f"{RED}Invalid Entry !!{ENDC}")
            break


def hash_pass():
    hash_confirm = input(f"\n{YELLOW}are you sure you want to hash your password ? (y or n){ENDC}:")
    if hash_confirm.lower() == 'y' or hash_confirm == "":
        hashed_pass = pbkdf2_sha512.hash(all_str)
        print(F"\n{BLUE}your original password : {ENDC}\n" + all_str,
              f"\n\n{BLUE}hashed password : {ENDC}\n" + hashed_pass)
        hash_save_menu()
    elif hash_confirm.lower() == 'n':
        hash_save_menu()
    else:
        print(f"{RED}Invalid Entry !!{ENDC}")
        hash_pass()


def save_db():
    initialize()
    # try:
    cursor = cnx.cursor()
    name = input("name your password to easily find it(required): ")
    desc = input("write a description for the password(required): ")
    user = input("enter yor user name (required): ")
    sql_commands = "INSERT INTO random (name, description, user, password) VALUES (?, ?, ?, ?)"
    values = (name, desc, user, all_str)
    cursor.execute(sql_commands, values)
    cnx.commit()


# except Exception:
#     print("something goes wrong !!!")
#     hash_save_menu()


def db_history():
    while True:
        # try:
        cursor = cnx.cursor()
        query_type = int(input(F"{BLUE}\n1.find password by enter the name\n2.show all\n3.main menu\n{ENDC}: "))
        if query_type == 1:
            name = input("enter the name : ")
            cursor.execute("SELECT * FROM random WHERE name = '%s'" % name)
            result_by_name = str(cursor.fetchall())
            if result_by_name == '[]':
                print(F"\n{YELLOW}no password saved by that name !!{ENDC}")
                db_history()
            else:
                print(result_by_name)
        elif query_type == 2:
            cursor.execute("SELECT name, description, user, password FROM random")
            all_in_table = cursor.fetchall()
            # print(all_in_table)
            for i in all_in_table:
                print(F"\n{GREEN}----------------------------------{ENDC}\nname : ", i[0], "\ndescription : ",
                      i[1], "\nusername : ", i[2], "\npassword : ", i[3])
        elif query_type == 3:
            main_menu()
        else:
            print(f"{RED}Invalid Entry !!{ENDC}")
    # except Exception:
    #     print("something goes wrong try again later")


def choose_length():
    while True:
        global length
        length = int(input(F"{BLUE}enter length of the password (less than 40 ){ENDC}: "))
        if length <= 40:
            if length <= 8:
                too_short = input(F"{YELLOW}too short are you sure ? (y or n):{ENDC} ")
                if too_short == 'y':
                    rand()
                elif too_short == 'n':
                    choose_length()
                else:
                    print(F"{RED}Invalid Entry !!{ENDC}")
                    choose_length()
            elif 40 >= length >= 9:
                rand()
            else:
                print(F"{RED}Invalid Entry !!{ENDC}")
        elif length > 40:
            print(F"{YELLOW}too long choose a shorter password !!{ENDC}")
            choose_length()


def rand():
    random_pass_1 = random.sample(all_chars, length)
    random_pass_2 = random.sample(random_pass_1, length)
    random_pass_3 = random.sample(random_pass_2, length)
    random_pass_4_last = random.sample(random_pass_3, length)
    global all_str
    all_str = ""
    all_str = all_str.join(random_pass_4_last)
    print(all_str)
    hash_save_menu()


main_menu()
