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
            change_universe()
        elif choice == "2": setting_state()
        elif choice == "3": statistics_state()
        elif choice == "4": leaderboard_state()
        else: break

def home_state():
    print("You're currently in the home state!\n")

    session.set_current_state("HOME")
    user: User = session.get_current_user()

    user_data = user.fetch_user_detail()
    if user_data is not None: print(user_data)

    print("Current Universe: " + str(session.universe), end= "\n\n")
    print("Commands:\nTyping Test Menu (0)\nChange Universe (1)\nSettings (2)\nStatistics (3)\nLeaderboard (4)\nLogout/exit (5)")
    choice = ""

    while True:
        choice = str(input())

        if choice not in ["0", "1", "2", "3", "4", "5"]:
            print("You must enter 0/1/2/3/4/5\nEnter your choice: ", end="")
            continue
        else: break

    return choice

def test_state():
    print("You're currently in the Typing test state!\n")

    session.set_current_state("TEST")

    print("Current Universe: " + session.universe, end="\n\n")
    print("Commands:\nStart Test in Flow State (0)\nStart Test in Practice mode (1)\nChange Universe (2)\nReturn to Home Page (3)\n")
    choice = ""

    while True:
        choice = str(input())

        if choice not in ["0", "1", "2", "3"]:
            print("You must enter 0/1/2/3\nEnter your choice: ", end="")
            continue
        else: break
    
    if choice == "0":
        start_test(session.universe, session.get_current_user())
    elif choice == "1":
        start_test(session.universe, session.get_current_user(), True)
    elif choice == "2":
        change_universe()
    else: return
    

def setting_state():
    print("You're currently in the settings state!")
    session.set_current_state("SETTINGS")

    #will be accessing the settings table in the database, will store user's information and preferences.
    user_settings: dict = session.get_current_user().get_user_settings()

    print(f"User id: {user_settings.get('user_id')}\nUsername: {user_settings.get('username')}\nCurrent Universe: {session.universe}\nPreferred Universe: {user_settings.get('preferred_universe')}\nDictionary Mode Word Limit: {user_settings.get('dictionary_word_limit')}")
    choice = input("\nDo you want to change your preferred universe/dictionary mode word limit? (y/n): ")

    if choice.lower() in ['yes', 'y']:
        print("\nChange Universe (0)\nChange Dictionary Mode Word Limit (1)\nExit (2): ")
        choice = input()

        if choice in ['0', '1']:
            if choice == '0':
                print("Here is the list of universe available:\nPlay (0)\nLong Text (1)\nDictionary (2)\n")

                choice = input("Enter your choice: ")

                if choice in ['0', '1', '2']:
                    #session.set_current_universe(int(choice))
                    session.get_current_user().set_preferred_universe(int(choice))
                else:
                    print("You must enter 0/1/2\n")
            else:
                # adding code to change the dictionary mode word limit
                try:
                    choice = input("Enter the new limit (10 < limit < 150): ")

                    if int(choice) <= 150 and int(choice) >= 10:
                        session.get_current_user().set_dictionary_word_limit(choice)
                        print(f"Your Dictionary Word Limit has been set to: {choice}")
                    else:
                        print("You must enter a number within 10 and 150")
                except:
                    print("You must enter a number within 10 and 150")



def leaderboard_state():
    print("You're currently in leaderboard state!")

def statistics_state():
    print("You're currently in statistic state!")
    race_info = session.get_current_user().fetch_user_race_info()

    if race_info is None:
        print("You have performed no test yet!")
        return

    print("\nTotal race performed: " + str(len(race_info)))
    average_wpm = 0
    average_acc = 0
    play = 0
    longtext = 0
    dictionary = 0

    for race in race_info:
        average_wpm += race[5]
        average_acc += race[6]

        if race[3] == "play": play+=1
        elif race[3] == "longtext": longtext+=1
        elif race[3] == "dictionary": dictionary+=1
    else:
        average_wpm /= len(race_info)
        average_acc /= len(race_info)

    print("Race performed in play mode: " + str(play))
    print("Race performed in longtext mode: " + str(longtext))
    print("Race performed in dictionary mode: " + str(dictionary), end="\n\n")

    print("Average wpm: " + str(average_wpm))
    print("Average acc: " + str(average_acc*100.0))

    input("\nPress Enter to go back")


def change_universe():
    print("Here is the list of universe available:\nPlay (0)\nLong Text (1)\nDictionary (2)\n")

    choice = input("Enter your choice: ")

    if choice in ['0', '1', '2']:
        session.set_current_universe(int(choice))
        print(f"The current universe has been changed to: {session.universe}")
    else:
        print("You must enter 0/1/2\n")
