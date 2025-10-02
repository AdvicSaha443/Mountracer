"""This file handles all basic commands eg: initializing/navigation, etc etc"""

from typingtest.auth import login, create_new_user
from typingtest.session import session
from typingtest.user import User
from typingtest.test import start_test
import time
import csv

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
        elif choice == "5": past_test_state()
        else: break

def home_state():
    print("You're currently in the home state!\n")

    session.set_current_state("HOME")
    user: User = session.get_current_user()

    user_data = user.fetch_user_detail()
    if user_data is not None: print(user_data)

    print("Current Universe: " + str(session.universe), end= "\n\n")
    print("Commands:\nTyping Test Menu (0)\nChange Universe (1)\nSettings (2)\nStatistics (3)\nLeaderboard (4)\nHistory (5)\nLogout/exit (6)")
    choice = ""

    while True:
        choice = str(input())

        if choice not in ["0", "1", "2", "3", "4", "5", "6"]:
            print("You must enter 0/1/2/3/4/5/6\nEnter your choice: ", end="")
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
    
    if choice == "0": start_test(session.universe, session.get_current_user())
    elif choice == "1": start_test(session.universe, session.get_current_user(), True)
    elif choice == "2": change_universe()
    else: return

def setting_state():
    print("You're currently in the settings state!")
    session.set_current_state("SETTINGS")

    #will be accessing the settings table in the database, will store user's information and preferences.
    user_settings: dict = session.get_current_user().get_user_settings()

    print(f"\nUser id: {user_settings.get('user_id')}\nUsername: {user_settings.get('username')}\nCurrent Universe: {session.universe}\nPreferred Universe: {user_settings.get('preferred_universe')}\nDictionary Mode Word Limit: {user_settings.get('dictionary_word_limit')}")
    print("\nChange Preferred Universe (1)\nChange Dictionary mode word limit (2)\nReturn Back to Home Page (3 or Enter)\n")
    choice = input()

    if choice == '1':
        print("\nHere is the list of universe available:\nPlay (0)\nLong Text (1)\nDictionary (2)\n")
        choice = input("Enter your choice: ")

        if choice in ['0', '1', '2']:
            #session.set_current_universe(int(choice))
            session.get_current_user().set_preferred_universe(int(choice))
        else:
            print("You must enter 0/1/2\n")

    elif choice == '2':
        try:
            choice = input("Enter the new limit (10 < limit < 150): ")

            if int(choice) <= 150 and int(choice) >= 10:
                session.get_current_user().set_dictionary_word_limit(int(choice))
                print(f"Your Dictionary Word Limit has been set to: {choice}")
            else:
                print("You must enter a number within 10 and 150")
        except:
            print("You must enter a number within 10 and 150")

    else: return

def leaderboard_state():
    print("You're currently in leaderboard state!")
    print("To view leaderboard, enter a universe:\nPlay (0)\nLong Text (1)\nDictionary (2)\nBack To Home Page (3)\n")

    choice = ""
    while True:
        choice = str(input())

        if choice not in ["0", "1", "2", "3"]:
            print("You must enter 0/1/2/3\nEnter your choice: ", end="")
            continue
        else: break
    
    universe = ""
    if choice == "0": universe = "play"
    elif choice == "1": universe = "longtext"
    elif choice == "2": universe = "dictionary"
    else: return

    leaderboard_data = session.get_current_user().fetch_race_info(universe)

    if leaderboard_data is None:
        input("There's no race data in the database!\nPress Enter to go back!")
        return

    useful_leaderboard_data = []

    user_added = []
    for elem in leaderboard_data:
        if not elem[1] in user_added:
            useful_leaderboard_data.append(elem)
            user_added.append(elem[1])

    # displaying the table
    # start = len(useful_leaderboard_data)
    start = 0
    while True:
        required_leaderboard_info = useful_leaderboard_data[start:start+10]

        # [["Rank", "username", "Text ID", "WPM", "Accuracy", "Time Stamp"]]
        table = [["Rank", "Username", "Text ID", "WPM", "Accuracy", "Time Stamp"]]
        
        for i, race in enumerate(required_leaderboard_info):
            table.append([(start + (i+1)), race[2], race[4], race[5], round((race[6]*100), 4), time.strftime('%d %b %y %I:%M %p', time.localtime(int(float(race[7]))))])

        max_column_width = [max([len(str(x[i])) for x in table]) for i in range(0, len(table[0]))]
        for elem in table: print(" | ".join(str(val) + "".join(" " for _ in range(0, max_column_width[i]-len(str(val)))) for i, val in enumerate(elem)))

        if (start+10) >= len(useful_leaderboard_data): break
        choice = input("\nSee 10 races after this (y/n): ")
        
        if choice.lower() in ["yes", "y"]: start+=10
        else: break

    input("\nPress enter to go back")

def past_test_state(): #alt: history state
    race_info: list = session.get_current_user().fetch_user_race_info()

    if race_info is None:
        input("You have performed no test yet!\nPress Enter to go Back")
        return

    end = len(race_info)
    while True:
        if (end-10) < 0: required_race_info = race_info[:end]
        else: required_race_info = race_info[end-10:end]

        table = [["Race No.", "Universe", "Text ID", "WPM", "Accuracy", "Time Stamp"]]
        
        for i, race in enumerate(required_race_info):
            table.append([(end + ((i+1) - len(required_race_info))), race[3], race[4], race[5], round((race[6]*100), 4), time.strftime('%d %b %y %I:%M %p', time.localtime(int(float(race[7]))))])

        max_column_width = [max([len(str(x[i])) for x in table]) for i in range(0, len(table[0]))]
        for elem in table: print(" | ".join(str(val) + "".join(" " for _ in range(0, max_column_width[i]-len(str(val)))) for i, val in enumerate(elem)))

        # first need to check whether there are any races left to be displayed
        # will then just change the end value, and everything else be taken care of
        if (end-10) <= 0: break
        choice = input("\nSee 10 races before this (y/n): ")
        
        if choice.lower() in ["yes", "y"]: end-=10
        else: break

    if input("\nTo View All the races, download csv file (1)\nPress enter to go back\n") == '1':
        with open('races.csv', 'w', newline = '') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['Race No.', 'Universe', 'Text ID', 'WPM', 'Accuracy', 'Epoch'])

            for i, races in enumerate(race_info):
                csv_writer.writerow((i+1,) + races[3:])
        
        input("The CSV file has been downloaded in the project's directory\nPress Enter to go back")


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

def text_information_state():
    pass

def help_state():
    pass


def change_universe():
    print("Here is the list of universe available:\nPlay (0)\nLong Text (1)\nDictionary (2)\n")

    choice = input("Enter your choice: ")

    if choice in ['0', '1', '2']:
        session.set_current_universe(int(choice))
        print(f"The current universe has been changed to: {session.universe}")
    else:
        print("You must enter 0/1/2\n")
