"""This file will handle all basic commands eg: initializing/navigation, etc etc"""

from .user import *

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

    