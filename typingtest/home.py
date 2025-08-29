"""This file handles all basic commands eg: initializing/navigation, etc etc"""

from .auth import login, create_new_user

# has multiple problems, if the user enters any integers other than 0,1 the code logic fails
# need to solve the problem of multiple printing of the print statement (for eg: when the user makes multiple mistakes while login/signing up)

def initialize():
    try:
        choice = int(input("To get started login (0) or create a new account (1): "))
    except:
        print("You must enter 0 or 1")
        return
    
    if not choice:
        if not login(): initialize()
    else:
        if not create_new_user(): initialize()
    
    # this part of the code will run only when the user has logged in.
    print("This part of the code shall only run when the user has logged in, and must not run multiple times")