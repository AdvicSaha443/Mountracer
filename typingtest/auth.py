""" This files handles the authentication commands"""

from typingtest.database import get_connection
from typingtest.session import session
from typingtest.user import User

def login():
    username = str(input("\nEnter your username: "))
    password = str(input("Password: "))

    cursor = get_connection().cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(64) UNIQUE, password VARCHAR(64), email VARCHAR(254));")
    cursor.execute("SELECT * FROM users;") # selecting all the data, and then checking as to add the ability to tell the user whether the username/password is wrong
    users_data = cursor.fetchall()
    cursor.close()

    for user in users_data:
        if user[1] == username:
            if user[2] != password:
                print("Wrong password entered!\nDirecting back to login page\n")
                break
            else:
                session.set_current_user(User(userid = user[0], username=username, password=password, email = user[3]))
                return 1
    else: print("User does not exist!\nDirecting back to login page\n")
    
    return 0

def create_new_user():
    username = input("\nEnter username you want: ")
    password = input("Enter password: ") # not checking the password format for now

    if username is None or password is None:
        print("\nUsername/Pasword cannot be None")
        return 0

    if len(username) > 16 or len(password) > 16:
        print("\nThe Username/Password can consist maximum of 16 letters")
        return 0

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(64) UNIQUE, password VARCHAR(64), email VARCHAR(254));")
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}';")

    if len(cursor.fetchall()) == 1:
        print("\nA user with this username already exists!\nDirecting back to login page")
        return 0
    
    cursor.execute(f"INSERT INTO users (username, password) VALUES('{username}', '{password}')")
    cursor.close()
    conn.commit()

    print("\nYou have signed up!\nLog in to use your account")
    return 0