"""This file handles all basic commands eg: initializing/navigation, etc etc"""

from .auth import login, create_new_user

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

    #start_typing_session()

    

def start_typing_session():
    while True:

        print("\nYou've Logged in! Welcome to Mount Racer!")
        break

        

        

































# this solution solves the issue, but since it relies on recursion, after a few interations, it will raise RecursionError. Thus sticking to while loop.
# def initialize(base: bool = False):
#     try:
#         choice = int(input("To get started login (0) or create a new account (1): "))
#     except:
#         print("You must enter 0 or 1")
#         return
    
#     if not choice:
#         if not login(): initialize(base = False)
#     else:
#         if not create_new_user(): initialize(base = False)

#     if base:
#         # this part of the code will run only when the user has logged in.
#         print("This part of the code shall only run when the user has logged in, and must not run multiple times")


# def initialize():
#     def ask_user():
#         choice = str(input("To get started login (0) or create a new account (1): "))
#         return choice
#     choice = ask_user()

#     if choice not in ["0", "1"]:
#         print("You must enter 0 or 1")
#         return

#     if int(choice):
#         while(create_new_user()):
#             pass
#     else:
#         pass # user wants to log in

