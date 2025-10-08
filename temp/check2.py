theme = {"h": "─", "v": "│", "tl": "┌", "tr": "┐", "bl": "└", "br": "┘"}
width = int(input("Enter width: "))
title = str(input("Enter title: "))

if width%2 != 0:
    if len(title)%2 != 0: title_position = ((width-1)/2) - (len(title)-1)/2
    else: title_position = (width-1)/2 - len(title)/2
else:
    if len(title)%2 == 0: title_position = (width/2) - len(title)/2
    else: title_position = width/2 -1 - (len(title)-1)/2

first_line = theme["tl"]
first_line += "".join(theme["h"] for _ in range(1, int(title_position)))
first_line += title
first_line += "".join(theme["h"] for _ in range(int(title_position)+len(title), width-1))
first_line += theme["tr"]

print(first_line)