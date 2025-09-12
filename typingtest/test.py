import time

def start_test():
    print("THIS IS SAMPLE TEXT!")

    print("Your time starts now! You may start typing, and once you're done press Enter!\n\n")

    start_ = time.perf_counter()
    user_text_input = str(input(""))
    end_ = time.perf_counter()

    print(end_)
    time_difference = round(end_ - start_, 3)
    print(time_difference)

start_test()