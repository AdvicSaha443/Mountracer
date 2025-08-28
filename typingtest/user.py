from .database import *

def login():
    print("login function has been called!")

    username = str(input("\nEnter your username: "))
    password = str(input("Password: "))

    cursor = get_connection().cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(64) PRIMARY KEY, password VARCHAR(64));")
    cursor.execute("SELECT * FROM users;") # selecting all the data, and then checking as to add the ability to tell the user whether the username/password is wrong
    users_data = cursor.fetchall()

    for user in users_data:
        if user[0] == username:
            if user[1] != password:
                print("Wrong password entered!\nDirecting back to login page\n")
                break
            else:
                return setuser(username, password)
    else: print("User does not exist!\nDirecting back to login page\n")
    
    cursor.close()
    return 0

def setuser(username: str, password: str):
    print(f"User has logged in with username: {username} and password: {password}")

    return 1

def create_new_user():
    print("Create new user function has been called!")

    username = input("\nEnter usename you want: ")
    password = input("Enter password: ") # not checking the password format for now

    if username is None or password is None:
        print("\nUsername/Pasword cannot be None")
        return 0

    if len(username) > 64 or len(password) > 64:
        print("\nThe Username/Password can consist maximum of 64 letters")
        return 0

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(64) PRIMARY KEY, password VARCHAR(64));")
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}';")

    if len(cursor.fetchall()) == 1:
        print("\nThe user with this username already exists!\nDirecting back to login page")
        return 0
    
    cursor.execute(f"INSERT INTO users VALUES('{username}', '{password}')")
    cursor.close()
    conn.commit()

    print("\nYou have signed up!\nLog in to user your account")