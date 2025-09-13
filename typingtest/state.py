"""This file handles all basic commands eg: initializing/navigation, etc etc"""

from .auth import login, create_new_user
from .session import session
from .user import User
from .test import start_test

def initialize():
    while True:
        choice = str(input("To get started login (0) or create a new account (1): "))

        if choice not in ["0", "1"]:
            print("You must enter 0/1")
            return
        
        if not int(choice):
            if not login():
                continue
            else: break
        else:
            create_new_user()

    """
        Will be first displaying the user information, like:
        username: qwerty443
        average:
        average(last 10):
        current universe: play/longtexts/numbers/dictionary

        commands:
        Start test (0)
        change universe (1)
        see leaderboard (2)
        logout (3)
        exit (anything else)
    """


    print(f"welcome {session.get_current_user().username}!\nTo get started, call one of the commands mentioned below!: ")

    #this loop is going to be the parent loop, all the iteration will be performed here, there will be child loops for typing test or to take some intput
    while True:
        #initially putting the user in home state
        choice = home_state()

        if choice == "0": test_state()
        elif choice == "1":
            # will directly add the command to change the universe here, and once the task is done, just continue with the loop so that the user goes back to home page
            pass
        elif choice == "2": setting_state()
        elif choice == "3": leaderboard_state()
        else: break

def home_state():
    print("You're currently in the home state!\n")

    session.set_current_state("HOME")
    user: User = session.get_current_user()

    user_data = user.fetch_user_detail()
    if user_data is not None: print(user_data)

    print("Current Universe: " + str(session.universe), end= "\n\n")
    print("Commands:\nTyping Test Menu (0)\nChange Universe (1)\nSettings (2)\nLeaderboard (3)\nLogout/exit (4)")
    choice = ""

    while True:
        choice = str(input())

        if choice not in ["0", "1", "2", "3", "4"]:
            print("You must enter 0/1/2/3/4\nEnter your choice: ", end="")
            continue
        else: break

    return choice

def test_state():
    print("You're currently in the Typing test state!\n")

    session.set_current_state("TEST")

    print("Current Universe: " + session.universe, end="\n\n")
    print("Commands:\nStart Test in Flow State (0)\nChange Universe (1)\nReturn to Home Page (2)\n")
    choice = ""

    while True:
        choice = str(input())

        if choice not in ["0", "1", "2"]:
            print("You must enter 0/1/2\nEnter your choice: ", end="")
            continue
        else: break
    
    if choice == "0":
        start_test(session.universe, session.get_current_user())
    elif choice == "1":
        pass
    else: return
    

def setting_state():
    print("You're currently in the settings state!")

def leaderboard_state():
    print("You're currently in leaderboard state!")

def statistics_state():
    print("You're currently in statistic state!")




# First it will print the user data, and then move into a while loop where user will be able to perform various task and start race
# perhaps defining mode/state would help for example: mode: testmode, idlemode (when at home page)
# or maybe something like, state = test, home, etc.
