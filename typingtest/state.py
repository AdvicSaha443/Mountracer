"""This file handles all basic commands eg: initializing/navigation, etc etc"""

from typingtest.auth import login, create_new_user
from typingtest.ui_components import Table, Panel, Line
from typingtest.session import session
from typingtest.user import User
from typingtest.test import start_test
import math
import time
import csv
import re

def initialize():
    while True:
        panel = Panel(
            header_text = "Welcome to Mountracer!",
            justify_header = "center",
            inner_text = "[1] Login\n[2] Create a new Account",
            inner_text_padding = (1, 16, 0, 0),
            overflow = "new_line",
            theme = "rounded",
            automatic_padding_reduction = True
        )
        choice = str(input("\n" + str(panel) + "\nEnter your choice: "))
        # choice = str(input("To get started login (0) or create a new account (1): "))

        if choice not in ["1", "2"]:
            print("You must enter 0/1")
            return
        else: choice = int(choice) - 1
        
        if not choice:
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

    #this loop is going to be the parent loop, all the iteration will be performed here, there will be child loops for typing test or to take some intput
    while True:
        #initially putting the user in home state
        choice = home_state()

        if choice == "1": test_state()
        elif choice == "2":
            # will directly add the command to change the universe here, and once the task is done, just continue with the loop so that the user goes back to home page
            change_universe()
        elif choice == "3": setting_state()
        elif choice == "4": statistics_state()
        elif choice == "5": leaderboard_state()
        elif choice == "6": past_test_state()
        # elif choice == "7": user_dashboard_state()
        else: break

def home_state():
    # user: User = session.get_current_user()

    # print("Current Universe: " + str(session.universe), end= "\n\n")
    # print("Commands:\nTyping Test Menu (0)\nChange Universe (1)\nSettings (2)\nStatistics (3)\nLeaderboard (4)\nHistory (5)\nYour Profile (6)\nLogout/exit (7)")
    Line.print_line(line_padding = (0, 0, 1, 2), theme = "dashed")
    print(Panel(
        header_text = f"Welcome {session.get_current_user().username}!",
        justify_header = "center",
        inner_text = "[1] Typing Menu\n[2] Change Universe\n[3] Settings\n[4] Statistics\n[5] Leaderboard\n[6] History\n[7] Logout/Exit",
        inner_text_padding = (1, 16, 0, 0),
        overflow = "new_line",
        theme = "rounded",
        automatic_padding_reduction = True
    ))
    choice = ""

    while True:
        choice = str(input("Enter your choice: "))

        if choice not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("You must enter 0/1/2/3/4/5/6/7\nEnter your choice: ", end="")
            continue
        else: break

    return choice

def test_state():
    while True:
        Line.print_line(line_padding=(0, 0, 1, 2), theme = "dashed")
        print("Current Universe: " + session.universe, end="\n")
        # print("Commands:\nStart Test in Flow State (0)\nStart Test in Practice mode (1)\nChange Universe (2)\nView Text Data (3)\nReturn to Home Page (4 or Enter)\n")

        print(Panel(
            inner_text = "[1] Start Test (Flow State)\n[2] Start Test (Practice State)\n[3] Change Universe\n[4] View Text Data\n[5] Back to Home Page",
            inner_text_padding = (1, 16, 0, 0),
            overflow = "new_line",
            theme = "rounded",
            automatic_padding_reduction = True
        ))
        choice = ""

        while True:
            choice = str(input("Enter your choice: "))

            if choice not in ["1", "2", "3", "4", "5"]:
                print("You must enter 1/2/3/4/5\n", end="")
                continue
            else: break
        
        if choice == "1": start_test(session.universe, session.get_current_user())
        elif choice == "2": start_test(session.universe, session.get_current_user(), True)
        elif choice == "3": change_universe()
        elif choice == "4": text_information_state()
        else: break

def setting_state():
    while True:
        Line.print_line(line_padding = (0, 0, 1, 2), theme = "dashed")
        user_settings: dict = session.get_current_user().get_user_settings()

        settings_panel = Panel(
            header_text="⚙️ SETTINGS",
            theme="rounded",
            automatic_padding_reduction=True
        )
        user_info = (
            f"User: {user_settings.get('username', 'N/A')}\n"
            f"Email: {user_settings.get('email', 'N/A')}\n"
            f"Current Universe: {session.universe}\n"
            f"Preferred Universe: {user_settings.get('preferred_universe', 'N/A')}\n"
            f"Dictionary Limit: {user_settings.get('dictionary_word_limit', 'N/A')}"
        )
        settings_panel.add_inner_text(
            inner_text=user_info,
            inner_text_padding=(1, 16, 0, 0),
            overflow="new_line"
        )

        menu_options = (
            "[1] " + ('Add' if user_settings.get('email') is None else 'Update') + " Recovery Email\n"
            "[2] Change Preferred Universe\n"
            "[3] Change Dictionary Limit\n"
            "[4] Back to Home"
        )
        settings_panel.add_inner_text(
            inner_text=menu_options,
            inner_text_padding=(1, 16, 0, 0),
            overflow="new_line"
        )
        print(settings_panel)

        # print(f"\nUser id: {user_settings.get('user_id')}\nUsername: {user_settings.get('username')}\nRecovery Email: {user_settings.get('email')}\nCurrent Universe: {session.universe}\nPreferred Universe: {user_settings.get('preferred_universe')}\nDictionary Mode Word Limit: {user_settings.get('dictionary_word_limit')}")
        # print("\n" + ('Add' if user_settings.get('email') is None else 'Update') + " Recovery Email (0)\nChange Preferred Universe (1)\nChange Dictionary mode word limit (2)\nReturn Back to Home Page (3 or Enter)\n")
        choice = input("Enter your choice: ") 

        if choice == '1':
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

        elif choice == '2': 
            Line.print_line(line_padding = (0, 0, 1, 2), theme = "dashed")
            print(Panel(
                header_text = "Available Universes",
                inner_text = "[1] Play\n[2] Long Text\n[3] Dictionary",
                inner_text_padding = (1, 16, 0, 0),
                theme = "rounded",
                automatic_padding_reduction = True
            ))
            choice = input("Enter your choice: ")

            if choice in ['1', '2', '3']:
                #session.set_current_universe(int(choice))
                session.get_current_user().set_preferred_universe(int(choice)-1)
                print(f"Your preferred Universe has been set to: {['play', 'long text', 'dictionary'][int(choice)-1]}")
            else:
                print("You must enter 0/1/2\n")
        elif choice == '3':
            try:
                choice = input("Enter the new limit (10 < limit < 150): ")

                if int(choice) <= 150 and int(choice) >= 10:
                    session.get_current_user().set_dictionary_word_limit(int(choice))
                    print(f"Your Dictionary Word Limit has been set to: {choice}")
                else:
                    print("You must enter a number within 10 and 150")
            except:
                print("You must enter a number within 10 and 150")
        else: break

def leaderboard_state():
    # print("To view leaderboard, enter a universe:\nPlay (0)\nLong Text (1)\nDictionary (2)\nBack To Home Page (3)\n")

    Line.print_line(line_padding = (0, 0, 1, 2), theme = "dashed")
    print(Panel(
        header_text = "Select Universe to display Leaderboard",
        inner_text = "[1] Play\n[2] Long Text\n[3] Dictionary\n[4] Exit",
        inner_text_padding = (1, 25, 0, 0),
        theme = "rounded",
        automatic_padding_reduction = True
    ))

    choice = ""
    while True:
        choice = str(input())

        if choice not in ["1", "2", "3", "4"]:
            print("You must enter 1/2/3/4\nEnter your choice: ", end="")
            continue
        else: break
    
    universe = ""
    if choice == "1": universe = "play"
    elif choice == "2": universe = "longtext"
    elif choice == "3": universe = "dictionary"
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
    total_pages = math.ceil(len(useful_leaderboard_data)/10.0)
    while True:
        required_leaderboard_info = useful_leaderboard_data[start:start+10]

        table_ = Table(
            title = f"Table {math.ceil(start/10.0) + 1} of {total_pages}",
            beautify_rows = True,
            theme = "rounded"
        )

        # [["Rank", "username", "Text ID", "WPM", "Accuracy", "Time Stamp"]]
        table_.add_columns("Rank", "Username", "Text ID", "WPM", "Accuracy", "Time Stamp")
        
        for i, race in enumerate(required_leaderboard_info):
            table_.add_row((start + (i+1)), race[2], race[4], race[5], round((race[6]*100), 4), time.strftime('%d %b %y %I:%M %p', time.localtime(int(float(race[7])))))

        # max_column_width = [max([len(str(x[i])) for x in table]) for i in range(0, len(table[0]))]
        # for elem in table: print(" | ".join(str(val) + "".join(" " for _ in range(0, max_column_width[i]-len(str(val)))) for i, val in enumerate(elem)))

        print(table_)
        if (start+10) >= len(useful_leaderboard_data): break
        choice = input("\n[N] Next     [Enter] Exit\n")
        # choice = input("\nSee 10 races after this (y/n): ")
        
        if choice.lower() in ["next", "n"]: start+=10
        else: break

    input("[Enter] Exit")

def past_test_state():
    race_info: list = session.get_current_user().fetch_user_race_info()
    Line.print_line(line_padding = (0, 0, 1, 2), theme = "dashed")

    if race_info is None:
        input("You have performed no test yet!\nPress Enter to go Back")
        return

    end = len(race_info)
    total_pages = math.ceil(end/10.0)
    
    while True:
        if (end-10) < 0: required_race_info = race_info[:end]
        else: required_race_info = race_info[end-10:end]

        # table = [["Race No.", "Universe", "Text ID", "WPM", "Accuracy", "Time Stamp"]]
        table = Table(
            title = f"Table {total_pages - math.ceil(end/10.0) + 1} of {total_pages}",
            beautify_rows = True,
            theme = "rounded"
        )

        table.add_columns("Race No.", "Universe", "Text ID", "WPM", "Accuracy", "Time Stamp")
        
        for i, race in enumerate(required_race_info):
            table.add_row((end + ((i+1) - len(required_race_info))), race[3], race[4], race[5], round((race[6]*100), 4), time.strftime('%d %b %y %I:%M %p', time.localtime(int(float(race[7])))))

        # max_column_width = [max([len(str(x[i])) for x in table]) for i in range(0, len(table[0]))]
        # for elem in table: print(" | ".join(str(val) + "".join(" " for _ in range(0, max_column_width[i]-len(str(val)))) for i, val in enumerate(elem)))
        print(table)

        # first need to check whether there are any races left to be displayed
        # will then just change the end value, and everything else be taken care of
        if (end-10) <= 0: break
        choice = input("\n[N] Next     [Enter] Exit\n")
        
        if choice.lower() in ["next", "n"]: end-=10
        else: break

    if input("\n[1] Download History in CSV file format\n[Enter] Exit\n") == '1':
        with open('races.csv', 'w', newline = '') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['Race No.', 'Universe', 'Text ID', 'WPM', 'Accuracy', 'Epoch'])

            for i, races in enumerate(race_info):
                csv_writer.writerow((i+1,) + races[3:])
        
        input("The CSV file has been downloaded in the project's directory\nPress Enter to go back")

def statistics_state():
    race_info = session.get_current_user().fetch_user_race_info()
    Line.print_line(line_padding = (0, 0, 1, 2), theme = "dashed")

    if race_info is None:
        input("You have performed no test yet!\nPress Enter to go back")
        return

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

    table1 = Table(
        title = "Race Count",
        show_header = False,
        beautify_rows = True,
        column_separator = ":",
        theme = "rounded"
    )

    table1.add_row("Total race performed", str(len(race_info)))
    table1.add_row("", "")
    table1.add_row("Race performed in play mode", str(play))
    table1.add_row("Race performed in longtext mode", str(longtext))
    table1.add_row("Race performed in dictionary mode", str(dictionary))

    table2 = Table(
        title = "Avg Stats",
        show_header = False,
        beautify_rows = True,
        column_separator = ":",
        theme = "rounded"
    )

    table2.add_row("Average wpm", str(round(average_wpm, 4)))
    table2.add_row("Average acc", str(round(average_acc*100.0, 2)))

    print(table1, end = "\n\n")
    print(table2, end = "\n")

    input("\nPress Enter to go back")

def text_information_state():
    Line.print_line(line_padding = (0, 0, 1, 2), theme = "dashed")
    print("\nhere you can check data related to tests performed for a specific text using its text id!")

    print(Panel(
        header_text = "Available Universes",
        inner_text = "[1] Play\n[2] Long Text\n[3] Dictionary\n[4] Exit",
        inner_text_padding = (1, 16, 0, 0),
        theme = "rounded",
        automatic_padding_reduction = True
    ))
    choice = input()
    universe = ""

    if choice == "1": universe = "play"
    elif choice == "2": universe = "longtext"
    elif choice == "3": universe = "dictionary"
    elif choice == "4": return
    else:
        input("Invalid Number Entered!\nPress Enter to go back!")
        return

    try:
        text_id = int(input("Enter the Text id: " if universe != "dictionary" else "Enter The word limit (between 10 and 150): "))
    except:
        print("Invalid data entered! You must enter an Integer!")
        return

    text_data = get_text_data(universe, text_id)

    if len(text_data) == 1:
        input(text_data.get('err'))
        return

    if universe != "dictionary":
        text_detail = text_data.get("text_data")

        text_panel = Panel(
            title = " Text Details ",
            justify_title = "center",
            inner_text = f"{text_detail[1]}\n\nfrom: " + ((text_detail[2][2:] if text_detail[2][0].startswith('\u2014') else text_detail[2])) + f"\nby: {text_detail[3]}",
            inner_text_padding = (1, 1, 1, 1),
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
        responsive = True,
        theme = "rounded",
        column_separator = ":"
    )

    user_text_table.add_row("Average WPM", text_data.get("user_average")[0])
    user_text_table.add_row("Average ACC", str(round(text_data.get("user_average")[1]*100, 3)) + "%")

    print(user_text_table, end="\n\n")

    user_best_table = Table(
        title = "Your Best",
        beautify_rows = True,
        theme = "rounded"
    )
    user_best_table.add_column("Text ID")
    user_best_table.add_column("WPM")
    user_best_table.add_column("Accuracy")
    user_best_table.add_column("Time Stamp")

    # perhaps change this to user top 5
    user_best = text_data.get('user_best')
    if user_best is not None:
        user_best_table.add_row(user_best[4], user_best[5], str(round(user_best[6]*100, 3)) + "%", time.strftime('%d %b %y %I:%M %p', time.localtime(int(float(user_best[7])))))
        print(user_best_table, end = "\n\n")

    general_info_table = Table(
        title = "Overall Statistics",
        show_header = False,
        beautify_rows = True,
        responsive = True,
        theme = "rounded",
        column_separator = ":"
    )

    general_info_table.add_row("Average WPM", text_data.get("text_average")[0])
    general_info_table.add_row("Average ACC", str(round(text_data.get("text_average")[1]*100, 3)) + "%")

    all_race_info = text_data.get("best_five_races")

    race_info_table = Table(
        title = "Leaderboard for this text" if universe != "dictionary" else "Leaderboard for this word limit",
        beautify_rows = True,
        theme = "rounded"
    )

    race_info_table.add_column("Rank")
    race_info_table.add_column("Username")
    race_info_table.add_column("Text ID")
    race_info_table.add_column("WPM")
    race_info_table.add_column("Accuracy")
    race_info_table.add_column("Time Stamp")

    for i, race in enumerate(all_race_info): race_info_table.add_row(i+1, race[2], race[4], race[5], str(round(race[6]*100, 3)) + "%", time.strftime('%d %b %y %I:%M %p', time.localtime(int(float(race[7])))))
    if text_data.get('user_leaderboard_position') is not None:
        if text_data.get('user_leaderboard_position') > 5:
            if text_data.get('user_leaderboard_position') != 6: race_info_table.add_row(":")
            race_info_table.add_row(text_data.get('user_leaderboard_position'), user_best[2], user_best[4], user_best[5], str(round(user_best[6]*100, 3)) + "%", time.strftime('%d %b %y %I:%M %p', time.localtime(int(float(user_best[7])))))

    print(general_info_table, end = "\n\n")
    print(race_info_table, end = "\n\n")

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
    

def user_dashboard_state():
    while True:
        Line.print_line(line_padding = (0, 0, 1, 2), theme = "dashed")

        print(Panel(
            header_text = "User Dashboard",
            inner_text = "[1] View My Profile\n[2] Edit Profile \n[3] View Other Profiles\n[4] Exit",
            inner_text_padding = (1, 16, 0, 0),
            theme = "rounded",
            overflow = "new_line",
            automatic_padding_reduction = True
        ))
        
        choice = input("Select an Option: ")

        if choice in ['1', '2', '3', '4']:
            if choice == '1': display_profile(session.get_current_user())
            elif choice == '2': pass
            elif choice == '3':
                print("\nto search a profile, you must enter the user ID or username of the profile to be searched")
                user_data = input("Enter username/userid: ")

                try:
                    user_data = int(user_data)
                    user: User = session.fetch_user(user_id = user_data)
                except: user: User = session.fetch_user(username = user_data)

                if user is not None: display_profile(user)
                else: input("\nThe user does not exist!\nPress Enter to go back")
            elif choice == '4': break
        else:
            input("You must enter 1/2/3/4\nPress Enter to go back")
            break

def help_state():
    pass


# assist functions

def display_profile(user: User):
    user_panel = Panel(
        header_text = user.username,
        inner_text = "Some information about the user",
        inner_text_padding = (1, 15, 0, 0),
        theme = "rounded",
        automatic_padding_reduction = True
    )

    print(user_panel)
    input("Press enter to go back!")

def change_universe():
    Line.print_line(line_padding = (0, 0, 1, 2), theme = "dashed")
    print(Panel(
        header_text = "Available Universes",
        inner_text = "[1] Play\n[2] Long Text\n[3] Dictionary",
        inner_text_padding = (1, 16, 0, 0),
        theme = "rounded",
        automatic_padding_reduction = True
    ))

    choice = input("Enter your choice: ")

    if choice in ['1', '2', '3']:
        session.set_current_universe(int(choice))
        print(f"The current universe has been changed to: {session.universe}")
    else:
        print("You must enter 1/2/3\n")

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