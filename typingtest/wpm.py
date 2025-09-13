""" GENERAL COMMANDS """

"""WPM COMMANDS"""
def calculate_wpm(characters: int, time: int):
    pass

""" ACCURACY COMMANDS """


#accuracy checked character to character
def levenshtein_accuracy(a: str, b: str):
    # b (user typed text) -> a (original text)

    if len(a) == 0 or len(b) == 0: return max(len(a), len(b))
    dp = [[0]*(len(b)+1) for i in range(0, len(a)+1)]

    for i in range(0, len(a)+1): dp[i][0] = i
    for i in range(0, len(b)+1): dp[0][i] = i

    for i in range(1, len(a)+1):
        for j in range(1, len(b) + 1):
            if(a[i-1] == b[j-1]): dp[i][j] = dp[i-1][j-1]
            else: dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])
    
    edit_distance =  dp[len(a)][len(b)]
    accuracy = 1.0 - edit_distance/len(a)

    print("Edit Distance: " + str(edit_distance))
    return accuracy

#even if a single mistake exists in a word, the whole word is considered wrong
#will be coding this later
def wordwise_accuracy(a: str, b: str):
    # b (user typed) -> a (original)

    words1 = a.split(" ")
    words2 = b.split(" ")

    for i in range(0, max(len(words1), len(words2))):
        pass
