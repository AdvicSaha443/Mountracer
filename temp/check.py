import shutil
text = "She had never observed his face more composed and she grabbed his hand and held it to her heart. It was resistless and dry. The outline of a skull was plain under his skin and the deep burned eye sockets seemed to lead into the dark tunnel where he had disappeared. She leaned closer and closer to his face, looking deep into them, trying to see how she had been cheated or what had cheated her, but she couldn't see anything. She shut her eyes and saw the pin point of light but so far away that she could not hold it steady in her mind. She felt as if she were blocked at the entrance of something. She sat staring with her eyes shut, into his eyes, and felt as if she had finally got to the beginning of something she couldn't begin, and she saw him moving farther and farther away, farther and farther into the darkness until he was the pin point of light."

class Table:
    THEMES = {
        "light": {
            "h": "─", "v": "│",
            "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
            "t": "┬", "b": "┴", "l": "├", "r": "┤", "c": "┼",
        },
        "double": {
            "h": "═", "v": "║",
            "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝",
            "t": "╦", "b": "╩", "l": "╠", "r": "╣", "c": "╬",
        },
        "rounded": {
            "h": "─", "v": "│",
            "tl": "╭", "tr": "╮", "bl": "╰", "br": "╯",
            "t": "┬", "b": "┴", "l": "├", "r": "┤", "c": "┼",
        },
        "heavy": {
            "h": "━", "v": "┃",
            "tl": "┏", "tr": "┓", "bl": "┗", "br": "┛",
            "t": "┳", "b": "┻", "l": "┣", "r": "┫", "c": "╋",
        },
        "dashed": {
            "h": "╌", "v": "╎",
            "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
            "t": "┬", "b": "┴", "l": "├", "r": "┤", "c": "┼",
        },
        "dotted": {
            "h": "┈", "v": "┊",
            "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
            "t": "┬", "b": "┴", "l": "├", "r": "┤", "c": "┼",
        },
        "mix_heavy_top": {
            "h": "━", "v": "│",
            "tl": "┏", "tr": "┓", "bl": "└", "br": "┘",
            "t": "┳", "b": "┴", "l": "├", "r": "┤", "c": "┼",
        },
        "mix_double_outer": {
            "h": "═", "v": "║",
            "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝",
            "t": "╦", "b": "╩", "l": "╠", "r": "╣", "c": "╬",
        },
        "ascii": {
            "h": "-", "v": "|",
            "tl": "+", "tr": "+", "bl": "+", "br": "+",
            "t": "+", "b": "+", "l": "+", "r": "+", "c": "+",
        },
    }

    @classmethod
    def get_theme(cls, name: str) -> str | None:
        return cls.THEMES.get(name)

    def __init__(self):
        pass

class Panel:
    THEMES = {
        "light": {"h": "─", "v": "│", "tl": "┌", "tr": "┐", "bl": "└", "br": "┘"},
        "double": {"h": "═", "v": "║", "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝"},
        "rounded": {"h": "─", "v": "│", "tl": "╭", "tr": "╮", "bl": "╰", "br": "╯"},
        "heavy": {"h": "━", "v": "┃", "tl": "┏", "tr": "┓", "bl": "┗", "br": "┛"},
        "dashed": {"h": "╌", "v": "╎", "tl": "┌", "tr": "┐", "bl": "└", "br": "┘"},
        "dotted": {"h": "┈", "v": "┊", "tl": "┌", "tr": "┐", "bl": "└", "br": "┘"},
        "mix_heavy_top": {"h": "━", "v": "│", "tl": "┏", "tr": "┓", "bl": "└", "br": "┘"},
        "mix_double_outer": {"h": "═", "v": "║", "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝"},
        "ascii": {"h": "-", "v": "|", "tl": "+", "tr": "+", "bl": "+", "br": "+"},
    }
    DEFAULT_WIDTH = ["inner_text", "terminal"]
    OVERFLOW = ["hidden", "new_line"]
    JUSTIFY = ["start", "end", "center"]

    @classmethod
    def get_theme(cls, name: str) -> str | None:
        return cls.THEMES.get(name)

    def __init__(
            self,
            title: str = None,
            justify_title: str = "center",
            title_padding: tuple = (0, 0), # left, right
            inner_text: str = None,
            inner_text_padding: tuple = (0, 0, 0, 0), # left, right, top, bottom
            theme: str = "light",
            width: int = None,
            default_width = "inner_text",
            height: int = None,
            overflow: str = "hidden" # values possible: hidden, dotted, new_line
        ) -> None:
        self._title = title
        self._justify_title = justify_title if justify_title in Panel.JUSTIFY else "center"
        self._title_padding = title_padding if len(title_padding) == 2 else (0, 0)
        self._inner_text = inner_text
        self._inner_text_padding = inner_text_padding if len(inner_text_padding) == 4 else (0, 0, 0, 0)
        self._theme = theme if theme in Panel.THEMES else "light"
        self._width = width
        self._default_width = default_width if default_width in Panel.DEFAULT_WIDTH else "inner_text"
        self._height = height
        self._overflow = overflow if overflow in Panel.OVERFLOW else "hidden"

        self.__panel = ""
    
    def __str__(self):
        self.__update_panel()
        return self.__panel

    @property
    def maximum_line_length() -> int:
        pass

    def set_title(self, title: str = None, justify_title: str = "center", title_padding: tuple = (0, 0)) -> None:
        self._title = title
        self._justify_title = justify_title if justify_title in Panel.JUSTIFY else "center"
        self._title_padding = title_padding if len(title_padding) == 2 else (0, 0)
    
    def set_inner_text(self, inner_text: str = None, inner_text_padding: tuple = (0, 0, 0, 0), default_width: str = "inner_text", overflow: str = "hidden") -> None:
        self._inner_text = inner_text
        self._inner_text_padding = inner_text_padding if len(inner_text_padding) == 4 else (0, 0, 0, 0)
        self._default_width = default_width if default_width in Panel.DEFAULT_WIDTH else "inner_text"
        self._overflow = overflow if overflow in Panel.OVERFLOW else "hidden"

    def __update_panel(self) -> None:
        inner_text = self._inner_text.split("\n") if self._inner_text is not None else ""
        inner_text_padding = self._inner_text_padding
        terminal_width = shutil.get_terminal_size().columns

        title = self._title
        justify_title = self._justify_title
        title_padding = self._title_padding

        # check here if length of width is greater than the length of terminal, if yes, check overflow and for overflow = newline use beautify function to compress the inner text lines
        if inner_text != "":
            if len(max(inner_text, key=len)) + 2 + inner_text_padding[0] + inner_text_padding[1] > terminal_width:
                # changing the lines which would cause a problem:
                new_inner_text = []
                for line in inner_text:
                    if len(line) + 2 + inner_text_padding[0] + inner_text_padding[1] > terminal_width:
                        if self._overflow == "new_line": new_inner_text += self.__beautify(text = line, width = (terminal_width - 2 - inner_text_padding[0] - inner_text_padding[1])).split("\n")
                        else: new_inner_text.append(line[0:(terminal_width - 2 - inner_text_padding[0] - inner_text_padding[1] - 3)] + "...")
                    else:
                        new_inner_text.append(line)

                inner_text = new_inner_text

        if inner_text == "" and self._default_width == "inner_text": self._width = terminal_width
        elif self._default_width == "inner_text" and self._width is None: self._width = len(max(inner_text, key=len)) + 2 + inner_text_padding[0] + inner_text_padding[1] # +2 since borders also needs to be considered
        elif self._default_width == "terminal" and self._width is None: self._width = terminal_width
        width = self._width

        height = self._height if (self._height != 0 and self._height is not None) else len(inner_text)+2
        theme = Panel.THEMES[self._theme]

        # dealing with first line
        # the position variables considers the literal position (first place is zero)
        first_line = ""
        if title is not None:
            if justify_title == "start": title_position = (1+title_padding[0]) # since justify is start, we're only considering the left padding
            elif justify_title == "end": title_position = ((width-1) - len(title) - title_padding[1])
            else:
                if width%2 != 0:
                    if len(title)%2 != 0: title_position = ((width-1)/2) - (len(title)-1)/2
                    else: title_position = (width-1)/2 - len(title)/2
                else:
                    if len(title)%2 == 0: title_position = (width/2 - 1) - len(title)/2
                    else: title_position = width/2 - (len(title)-1)/2

            first_line = theme["tl"]
            first_line += "".join(theme["h"] for _ in range(1, int(title_position))) # replace these with string multiplication
            first_line += title
            first_line += "".join(theme["h"] for _ in range(int(title_position)+len(title), width-1))
            first_line += theme["tr"]
        else:
            first_line = theme["tl"] + theme["h"]*(width-2) + theme["tr"]

        # dealing with the intermediate lines
        middle_lines = ""
        middle_lines += (theme["v"] + " "*(width-2) + theme["v"] + "\n")*inner_text_padding[2]

        for i in range(0, height-2):
            line = theme["v"]
            line += " "*inner_text_padding[0]
            line += inner_text[i]
            line += " "*(width-2 - inner_text_padding[0] - len(inner_text[i]))
            line += theme["v"]
            middle_lines += (line + "\n")
        
        middle_lines += (theme["v"] + " "*(width-2) + theme["v"] + "\n")*inner_text_padding[3]

        # dealing with last line
        last_line = theme["bl"] + theme["h"]*(width-2) + theme["br"]

        panel = first_line + "\n" + middle_lines + last_line
        self.__panel = panel

        """
        if width is odd:
        -> title is odd: h = (len(title)-1)/2, characters needed to be removed: middle char, (+h and -h) chars
        12345
        starting position of title = ((width-1)/2)-h

        -> title is even: abcd -> h = len(title)/2, (width-1)/2-h = starting position of title
        123456

        if width is even:
        - if title is odd: 12345 -> starting position: starting position of title = (width/2-1)

        - if title is even: 1234 -> h = len(title)/2, starting position = width/2-1-h
        """

    def __beautify(self, text: str, width: int = shutil.get_terminal_size().columns) -> str:
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

panel1 = Panel(
    title=" Sample Title ",
    justify_title="center",
    title_padding=(0, 0),
    inner_text_padding=(1, 0, 2, 1),
    inner_text = "This is a sample line!\nThis is another sample line!\nThis is reallllllllyyyyyyyyyyyyyyyyyyy looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong textttttt\n\nShe had never observed his face more composed and she grabbed his hand and held it to her heart. It was resistless and dry. The outline of a skull was plain under his skin and the deep burned eye sockets seemed to lead into the dark tunnel where he had disappeared. She leaned closer and closer to his face, looking deep into them, trying to see how she had been cheated or what had cheated her, but she couldn't see anything. She shut her eyes and saw the pin point of light but so far away that she could not hold it steady in her mind. She felt as if she were blocked at the entrance of something. She sat staring with her eyes shut, into his eyes, and felt as if she had finally got to the beginning of something she couldn't begin, and she saw him moving farther and farther away, farther and farther into the darkness until he was the pin point of light.",
    theme = "ascii", 
    default_width="",
    overflow="new_line"
)
panel2 = Panel(
    inner_text = "This is a sample text!",
    theme = "heavy",
    default_width = "terminal"
)

panel3 = Panel()

panel3.set_title(
    title = " TITLE "
)
panel3.set_inner_text(
    inner_text = "This is a sample text!",
    default_width = "terminal",
    inner_text_padding= (0, 0, 2, 2)
)

print(panel1)
print(panel2)
print(panel3)



# terminal_dimensions = shutil.get_terminal_size()

# print(f"Width: {terminal_dimensions.columns}")
# print("".join("=" for _ in range(0, terminal_dimensions.columns)))
# print(beautify(text))
# print("".join("=" for _ in range(0, terminal_dimensions.columns)))
# print(text)