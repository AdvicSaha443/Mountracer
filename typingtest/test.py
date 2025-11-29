from typingtest.database import get_connection
from typingtest.ui_components import Table, Panel, Line
from typingtest.wpm import calculate_stat
from typingtest.user import User
import random
import shutil
import time
import csv

def start_test(universe: str, user: User, practice: bool = False, beautify_text: bool = True):
    # test is being start in flow state, hence using while loop
    choice = ""

    while True:
        if choice == "1": break
        text: list = select_text(universe, user.dictionary_word_limit)

        Line.print_line(line_padding = (0, 0, 1, 2), theme = "dashed")
        print("Your time starts now! You may start typing, and once you're done press Enter!\n")
        # print(beautify(text[1]) if beautify_text else text[1], end = "\n\n")
        print(Panel(
            inner_text = text[1],
            overflow = "new_line",
            theme = "rounded",
            default_width = 'terminal',
            inner_text_padding = (1, 1, 1, 1)
        ), end="\n\n")

        #taking user input
        start_time = time.perf_counter()
        user_text_input = str(input())

        end_time = time.perf_counter()
        stat = calculate_stat(time.mktime(time.localtime()), (end_time - start_time), text, user_text_input, universe)

        # Display information related to current test
        Line.print_line(line_padding = (0, 0, 1, 2), text = " Test Completed! ", theme = "light")

        # if universe != "dictionary": print(f"You just typed a quote from: {text[2] if text[2][0] != '\u2014' else text[2][3:]}\nAuthor: {text[3]}\n") # backslashes cannot appear inside {} of f strings
        # if universe != "dictionary": print("You just typed a quote from: " + (text[2][2:] if text[2][0].startswith('\u2014') else text[2]) + f"\nAuthor: {text[3]}\n") # had to factor in the error obtained from web scrapping source
        # print(f"wpm: {stat.get('wpm')}\nacc: {stat.get('accuracy')*100.0}%\nraw wpm: {stat.get('raw_wpm')}\ntotal characters/wrong operations: {len(user_text_input)}/{stat.get('edit_distance')}\n")

        if universe != "dictionary":
            table1 = Table(
                title = "Quote Info",
                show_header = False,
                theme = "rounded",
                beautify_rows = True,
                column_separator = ":"
            )

            table1.add_row("Typed From", text[2][2:] if text[2][0].startswith('\u2014') else text[2])
            table1.add_row("Author", text[3])

            print(str(table1) + "\n")

        table2 = Table(
            title = "Performance Stats",
            show_header = False,
            theme = "rounded",
            beautify_rows = True
        )

        table2.add_row("WPM", stat.get('wpm'))
        table2.add_row("Accuracy", str(round(stat.get("accuracy")*100, 2)) + "%")
        table2.add_row("", "")
        table2.add_row("Raw WPM", stat.get('raw_wpm'))
        table2.add_row("Total Characters", len(user_text_input))
        table2.add_row("Mistakes", stat.get("edit_distance"))

        print(table2)

        if practice:
            choice1 = input("\n[1] Save Result\n[Enter] Don't Save\n")
            if choice1.lower() == "1": save_test_result(stat, user)
        else: save_test_result(stat, user)

        choice = input("[1] Exit\n[Enter] Start Another Practice Test\n")

def select_text(universe: str, max_range: int):
    with open(f"./csv_files/text_{universe}.csv", "r", encoding="utf-8") as f:
        csv_reader = csv.reader(f)

        if universe != "dictionary":
            texts = list(csv_reader)
            return texts[random.randint(0, len(texts)-1)]
        else:
            words = list(csv_reader)[0]
            text = [f"dict({str(max_range)})", ("".join((words[random.randint(0, len(words)-1)] + " ") for _ in range(0, max_range)))[:-1], "None", "None"]

            return text

def save_test_result(stat: dict, user: User):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS races (race_number INT AUTO_INCREMENT PRIMARY KEY, user_id INT, username VARCHAR(64), universe VARCHAR(64), text_id VARCHAR(64), wpm FLOAT(7,4), accuracy FLOAT(5, 4), epoch VARCHAR(64));")
    cursor.execute(f"INSERT INTO races (user_id, username, universe, text_id, wpm, accuracy, epoch) VALUES({user.user_id}, '{user.username}', '{stat.get('universe')}', '{stat.get('text')[0]}', {stat.get('wpm')}, {stat.get('accuracy')}, '{stat.get('timestamp')}');")

    cursor.close()
    conn.commit()

def beautify(text: str):
    width = shutil.get_terminal_size().columns

    text_ = text.split(" ")
    final_text_list = []
    current_sentence_length = 0
    
    for word in text_:
        if current_sentence_length + len(word) >= width:
            final_text_list.append("\n" + word)
            current_sentence_length = len(word)+1 # 1 is added to factor in the space which will be added later
        else:
            final_text_list.append(word)
            current_sentence_length+=len(word)+1

    return "".join((word+ " ") for word in final_text_list)