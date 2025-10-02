""" GENERAL COMMANDS """
def calculate_stat(timestamp: float, timetaken: int, text: list, user_text_input: str, universe):
    # information required: timetaken, text, user_text_input, start_time

    accuracy_info = levenshtein_accuracy(text[1], user_text_input)
    wpm = calculate_wpm(len(user_text_input), timetaken, accuracy_info[0])
    raw_wpm = calculate_raw_wpm(len(user_text_input), timetaken)

    return {
        "text": text,
        "universe": universe,
        "accuracy": round(accuracy_info[0], 4),
        "wpm": round(wpm, 4),
        "raw_wpm": round(raw_wpm, 4),
        "edit_distance": accuracy_info[1],
        "timestamp": timestamp
    }

"""WPM COMMANDS"""

def calculate_wpm(characters: int, time: int, accuracy: float):
    return ((accuracy/1.0)*(((characters/5.0)/time)*60.0)) # accuracy*raw_wpm

def calculate_raw_wpm(characters: int, time: int):
    return (((characters/5.0)/time)*60.0) #using average length of a word in English Language

""" ACCURACY COMMANDS """

#accuracy checked character to character
def levenshtein_accuracy(a: str, b: str):
    # b (user typed text) -> a (original text)

    if len(a) == 0 or len(b) == 0: return (0, max(len(a), len(b)))
    dp = [[0]*(len(b)+1) for _ in range(0, len(a)+1)]

    for i in range(0, len(a)+1): dp[i][0] = i
    for i in range(0, len(b)+1): dp[0][i] = i

    for i in range(1, len(a)+1):
        for j in range(1, len(b) + 1):
            if(a[i-1] == b[j-1]): dp[i][j] = dp[i-1][j-1]
            else: dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])
    
    edit_distance =  dp[len(a)][len(b)]
    accuracy = 1.0 - edit_distance/len(a)

    print("Edit Distance: " + str(edit_distance))
    return (accuracy, edit_distance)

# even if a single mistake exists in a word, the whole word is considered wrong
# will be coding this later
# def wordwise_accuracy(a: str, b: str):
#     # b (user typed) -> a (original)

#     words1 = a.split(" ")
#     words2 = b.split(" ")

#     for i in range(0, max(len(words1), len(words2))):
#         pass
