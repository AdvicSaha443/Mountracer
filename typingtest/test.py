from .user import User
import random
import time
import csv

def start_test(universe: str, user: User):
    # test is being start in flow state, hence using while loop
    choice = ""

    while True:
        if choice == "exit": break

        text = select_text(universe)
        print("Your time starts now! You may start typing, and once you're done press Enter!\n\n")
        print(text[0], end = "\n\n")

        #taking user input
        start_time = time.perf_counter()
        user_text_input = str(input())
        end_time = time.perf_counter()

        choice = input("Do you want to exist?: (exit): ")

        #calling methods to calculate data about the race


    # print("THIS IS SAMPLE TEXT!")
    # print("Your time starts now! You may start typing, and once you're done press Enter!\n\n")

    # start_ = time.perf_counter()
    # user_text_input = str(input(""))
    # end_ = time.perf_counter()

    # print(end_)
    # time_difference = round(end_ - start_, 3)
    # print(time_difference)

def select_text(universe: str):

    with open(f"./csv_files/text_{universe}.csv", "r") as f:
        csv_reader = csv.reader(f)

        if universe != "dictonary":
            texts = list(csv_reader)
            return texts[random.randint(0, len(texts)-1)]
        else:
            pass