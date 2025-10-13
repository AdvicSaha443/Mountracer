"""This file handles all basic commands eg: initializing/navigation, etc etc"""

from typingtest.auth import login, create_new_user
from typingtest.ui_components import Table, Panel
from typingtest.session import session
from typingtest.user import User
from typingtest.test import start_test
import time
import csv
import re

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
        elif choice == "6": account_state()
        else: break

def home_state():
    print("You're currently in the home state!\n")

    session.set_current_state("HOME")
    user: User = session.get_current_user()

    user_data = user.fetch_user_detail()
    if user_data is not None: print(user_data)

    print("Current Universe: " + str(session.universe), end= "\n\n")
    print("Commands:\nTyping Test Menu (0)\nChange Universe (1)\nSettings (2)\nStatistics (3)\nLeaderboard (4)\nHistory (5)\nYour Profile (6)\nLogout/exit (7)")
    choice = ""

    while True:
        choice = str(input())

        if choice not in ["0", "1", "2", "3", "4", "5", "6", "7"]:
            print("You must enter 0/1/2/3/4/5/6/7\nEnter your choice: ", end="")
            continue
        else: break

    return choice

def test_state():
    print("You're currently in the Typing test state!\n")
    session.set_current_state("TEST")

    print("Current Universe: " + session.universe, end="\n\n")
    print("Commands:\nStart Test in Flow State (0)\nStart Test in Practice mode (1)\nChange Universe (2)\nView Text Data (3)\nReturn to Home Page (4 or Enter)\n")
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
    elif choice == "3": text_information_state()
    else: return

def setting_state():
    print("You're currently in the settings state!")
    session.set_current_state("SETTINGS")

    settings_table = Table(
        title = "Settings: ",
        show_header = False,
        beautify_rows = True,
        theme = "rounded"
    )

    #will be accessing the settings table in the database, will store user's information and preferences.
    user_settings: dict = session.get_current_user().get_user_settings()

    settings_table.add_row("User ID", user_settings.get('user_id'))
    settings_table.add_row("Username", user_settings.get('username'))
    settings_table.add_row("Recovery Email", user_settings.get('email'))
    settings_table.add_row("Current Universe", session.universe)
    settings_table.add_row("Preferred Universe", user_settings.get('preferred_universe'))
    settings_table.add_row("Dictionary Word Limit", user_settings.get('dictionary_word_limit'))

    print(settings_table)

    # print(f"\nUser id: {user_settings.get('user_id')}\nUsername: {user_settings.get('username')}\nRecovery Email: {user_settings.get('email')}\nCurrent Universe: {session.universe}\nPreferred Universe: {user_settings.get('preferred_universe')}\nDictionary Mode Word Limit: {user_settings.get('dictionary_word_limit')}")
    print("\n" + ('Add' if user_settings.get('email') is None else 'Update') + " Recovery Email (0)\nChange Preferred Universe (1)\nChange Dictionary mode word limit (2)\nReturn Back to Home Page (3 or Enter)\n")
    choice = input() 

    if choice == '0':
        email_input = input("Enter new recovery email: ")
        email_validation = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if len(email_input) >= 254:
            input("The email length must be less than 254 characters!\nPress Enter to go back")
            return
        
        if re.match(email_validation, email_input) is not None:
            session.get_current_user().set_user_email(email_input)
            input(f"Your Recovery Email has been set to: {email_input}!\nPress Enter to go back")
        else:
            input("Invalid Email Entered!\nPress Enter to go back")

    elif choice == '1':
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

    print("Average wpm: " + str(round(average_wpm, 4)))
    print("Average acc: " + str(round(average_acc*100.0, 2)))

    input("\nPress Enter to go back")

def text_information_state():
    print("\nhere you can check data related to tests performed for a specific text using its text id!")
    print("\nSelect Text Universe:\nPlay (0)\nLong Texts (1)\nDictionary (2)")
    choice = input()
    universe = ""

    if choice == "0": universe = "play"
    elif choice == "1": universe = "longtext"
    elif choice == "2": universe = "dictionary"
    else:
        input("Invalid Number Entered!\nPress Enter to go back!")
        return

    try:
        text_id = int(input("Enter the Text id: " if universe != "dictionary" else "Enter The word limit (between 10 and 150): "))
    except:
        print("Invalid data entered! You must enter an Integer!")
        return

    text_data = get_text_data(universe, text_id)
    print(text_data)

    if len(text_data) == 1:
        input(text_data.get('err'))
        return

    if universe != "dictionary":
        text_detail = text_data.get("text_data")

        text_panel = Panel(
            title = " Text Details ",
            justify_title = "center",
            inner_text = f"{text_detail[1]}\n\nfrom: " + ((text_detail[2][2:] if text_detail[2][0].startswith('\u2014') else text_detail[2])) + f"\nby: {text_detail[3]}",
            inner_text_padding = (0, 0, 1, 1),
            default_width = "inner_text",
            overflow = "new_line",
            theme = "rounded"
        )

        print("\n" + str(text_panel) + "\n")
    else:
        print("Word Limit: " + str(text_id) + "\n")

    user_text_table = Table(
        title = "Your Statistics",
        show_header = False,
        beautify_rows = True,
        responsive = True
    )

    user_text_table.add_row("Average WPM:", text_data.get("user_average")[0])
    user_text_table.add_row("Average ACC:", text_data.get("user_average")[1])

    print(user_text_table)

    user_best_table = Table(
        title = "Your Best",
        beautify_rows = True
    )
    user_best_table.add_column("Text ID")
    user_best_table.add_column("WPM")
    user_best_table.add_column("Accuracy")
    user_best_table.add_column("Time Stamp")

    # perhaps change this to user top 5
    user_best = text_data.get('user_best')
    if user_best is not None:
        user_best_table.add_row(user_best[4], user_best[5], str(round(user_best[6]*100, 3)) + "%", time.strftime('%d %b %y %I:%M %p', time.localtime(int(float(user_best[7])))))
        print(user_best_table)

    general_info_table = Table(
        title = "Overall Statistics",
        show_header = False,
        beautify_rows = True,
        responsive = True
    )

    general_info_table.add_row("Average WPM: ", text_data.get("text_average")[0])
    general_info_table.add_row("Average ACC: ", text_data.get("text_average")[1])

    all_race_info = text_data.get("best_five_races")

    race_info_table = Table(
        title = "Leaderboard for this text" if universe != "dictionary" else "Leaderboard for this word limit",
        beautify_rows = True
    )

    race_info_table.add_column("Rank")
    race_info_table.add_column("Username")
    race_info_table.add_column("Text ID")
    race_info_table.add_column("WPM")
    race_info_table.add_column("Accuracy")
    race_info_table.add_column("Time Stamp")

    for i, race in enumerate(all_race_info): race_info_table.add_row(i+1, race[2], race[4], race[5], race[6], time.strftime('%d %b %y %I:%M %p', time.localtime(int(float(race[7])))))
    if text_data.get('user_leaderboard_position') is not None:
        if text_data.get('user_leaderboard_position') > 5:
            if text_data.get('user_leaderboard_position') != 6: race_info_table.add_row(":")
            race_info_table.add_row(text_data.get('user_leaderboard_position'), user_best[2], user_best[4], user_best[5], user_best[6], time.strftime('%d %b %y %I:%M %p', time.localtime(int(float(user_best[7])))))

    print(general_info_table)
    print(race_info_table)

    input("Press enter to go back!")

    """Information to be displayed:

        Text will be displayed (if universe != dictionary)
        
        Text Id/word limit: 
        text author:
        text source: 

        your stats:
        your average score for this text: 
        your average accuracy for this text: 
        your best score for this text:

        average score for this text
        average accuracy for this text

        maximum score for this text ___ by username ___ with the accuracy ___

        display the top 5 scores for this text (leaderboard) and at the end display the position of the current user (add dots and stuff to display gap)

    """
    

def account_state():
    print("You're in the account state!")



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

def get_text_data(universe: str, text_id: int) -> dict:

    if universe == "dictionary": text_id = f"dict({text_id})"
    current_user = session.get_current_user()
    test_info = current_user.fetch_race_info(universe, text_id)
    
    if test_info is None: return {
        "err": "No races have been performed for this text!"
    }

    #extracting the text, author, and the source for the book if the universe not equal to dictionary
    text_data = []

    try:
        if universe != "dictionary":
            with open(f"./csv_files/text_{universe}.csv", "r", encoding="utf-8") as f:
                csv_reader = csv.reader(f)
                texts = list(csv_reader)

                text_data = texts[text_id-1]
    except:
        return {
            "err": "The Text does not exist!"
        }
    
    #extracting the top 5 tests for the given text id and also storying the rank of the user in the leaderboard for this particular text
    useful_test_info = []
    rank_position = 0
    user_leaderboard_rank = None

    user_added = set()
    for test in test_info:
        if test[1] == current_user.user_id and test[1] not in user_added: user_leaderboard_rank = rank_position+1

        if not test[1] in user_added:
            rank_position += 1
            user_added.add(test[1])

            if len(useful_test_info) < 5: useful_test_info.append(test)

        if len(useful_test_info) == 5 and user_leaderboard_rank is not None: break
    
    #extracting the average wpm and average accuracy for this text:
    if test_info:
        avg_wpm = round(sum(races[5] for races in test_info)/len(test_info), 4)
        avg_acc = round(sum(races[6] for races in test_info)/len(test_info), 4)
    else:
        avg_wpm = avg_acc = 0
    
    text_average = (avg_wpm, avg_acc)

    #extracting the details regarding the user's text
    user_test_info = current_user.fetch_user_race_info(universe, text_id, True)

    if user_test_info:
        avg_wpm = round(sum(races[5] for races in user_test_info)/len(user_test_info), 4)
        avg_acc = round(sum(races[6] for races in user_test_info)/len(user_test_info), 4)
    else:
        avg_wpm = avg_acc = 0
    
    user_average = (avg_wpm, avg_acc)

    return {
        "text_id": text_id,
        "text_data": text_data,
        "user_average": user_average,
        "user_best": user_test_info[0] if user_test_info is not None else None,
        "text_average": text_average,
        "best_five_races": useful_test_info,
        "user_leaderboard_position": user_leaderboard_rank
    }