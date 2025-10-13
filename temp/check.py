import shutil
import math
text = "She had never observed his face more composed and she grabbed his hand and held it to her heart. It was resistless and dry. The outline of a skull was plain under his skin and the deep burned eye sockets seemed to lead into the dark tunnel where he had disappeared. She leaned closer and closer to his face, looking deep into them, trying to see how she had been cheated or what had cheated her, but she couldn't see anything. She shut her eyes and saw the pin point of light but so far away that she could not hold it steady in her mind. She felt as if she were blocked at the entrance of something. She sat staring with her eyes shut, into his eyes, and felt as if she had finally got to the beginning of something she couldn't begin, and she saw him moving farther and farther away, farther and farther into the darkness until he was the pin point of light."

class Table:
    DEFAULT_WIDTH = ["inner_text", "terminal"]
    JUSTIFY = ["start", "end", "center"]
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

    def __init__(
        self,
        title: str = None,
        show_header: bool = True,
        theme: str = "light",
        beautify_rows: bool = False,
        responsive: bool = True
    ) -> None:
        
        self._title = str(title)
        self._show_header = show_header
        self._theme = theme if theme in Table.THEMES else "light"
        self._beautify_rows = beautify_rows
        self._responsive = responsive
        self._table = None

        self._columns = []
        self._rows = []

    def __str__(self):
        self.__update_table()
        return self._table
    
    @property
    def columns(self) -> list:
        return self._columns

    @property
    def rows(self) -> list:
        return self._rows 
    
    def add_column(self, text: str = None, justify: str = "center", padding: tuple = (0, 0), decorate: bool = False) -> None:
        self._columns.append((
            str(text),
            justify if justify in Table.JUSTIFY else "center",
            padding if len(padding) == 2 else (0, 0),
            decorate
        ))

    def add_row(self, *values):
        self._rows.append([str(x) for x in values])

    def __update_table(self) -> None:
        title = self._title
        theme = Table.THEMES[self._theme]
        header_visible = self._show_header

        columns = [x[0] for x in self._columns]
        columns_settings = self._columns
        rows = self._rows

        # checking the maximum number of row/header row and empty elements will be added accordingly.
        # maximum_columns = max(len(max(columns, key = len)), len(max(rows, key = len)))
        maximum_columns = max(len(columns), len(max(rows, key = len)))
        table = []

        if header_visible: table.append(columns) if len(columns) == maximum_columns else table.append(columns + [""]*(maximum_columns-len(columns)))
        for i, row in enumerate(rows): table.append(row) if len(row) == maximum_columns else table.append(row + [""]*(maximum_columns-len(row)))

        for i, column in enumerate(columns_settings):
            if column[3] or self._beautify_rows: # decorate is true
                for j in range(1 if header_visible else 0, len(table)): table[j][i] = " " + str(table[j][i]).strip() + " "

        if not header_visible and len(columns_settings) == 0 and self._beautify_rows:
            for i in range(0, len(table)):
                for j in range(0, len(table[i])):
                    table[i][j] = " " + table[i][j] + " "

        # calculating the maximum admissible length for each column
        max_column_length = [max([len(str(x[i])) for x in table]) for i in range(0, len(table[0]))]
        table_ = ""

        table_width = sum(max_column_length) + 1 + len(table[0]) # constant values added for borders
        terminal_width = shutil.get_terminal_size().columns

        #check whether if table_width is greater than the terminal width

        if terminal_width < table_width and self._responsive:
            diff = table_width - terminal_width

            if (diff/maximum_columns) < 1:
                max_length = max(max_column_length)
                pos = max_column_length.index(max_length)
                max_limit = max_length - diff

                if max_limit > 0:
                    for i, elem in enumerate(table):
                        if len(elem[pos]) > max_limit: table[i][pos] = table[i][pos][0:(max_limit - 3)] + "..."
            else:
                column_diff = math.floor(diff/maximum_columns) + 1

                # will be required to check each element i*j and compress the element which exceeds the column_diff
                for i in range(0, len(table[0])):
                    column_max_limit = max_column_length[i] - column_diff

                    for j in range(0, len(table)):
                        if len(table[j][i]) > column_max_limit: table[j][i] = table[j][i][0:(column_max_limit-3)] + "..."

            # recalculating the maximum column width, table_width
            max_column_length = [max([len(str(x[i])) for x in table]) for i in range(0, len(table[0]))]
            table_width = sum(max_column_length) + 1 + len(table[0])


        # building the table:
        if title is not None:
            if table_width%2 != 0:
                if len(title)%2 != 0: title_position = ((table_width-1)/2) - (len(title)-1)/2
                else: title_position = (table_width-1)/2 - len(title)/2
            else:
                if len(title)%2 == 0: title_position = (table_width/2) - len(title)/2
                else: title_position = table_width/2 - (len(title)-1)/2

            table_ += " "*(int(title_position)) + title + "\n"
        
        #table_ += theme["tl"] + ((theme["h"]*max_column_length[i] + theme["t"]) for i in range(0, len(max_column_length)))[:-1] + theme["tr"]
        table_ += theme["tl"] + "".join((theme["h"]*max_column_length[i] + theme.get("t")) for i in range(0, len(max_column_length)))[:-1] + theme["tr"] + "\n"

        # calculating justified position for each column header:
        justified_header = []
        if header_visible:
            for i, elem in enumerate(table[0]):
                if not elem == "":
                    if columns_settings[i][1] == "start": justified_header.append(elem + "".join(" " for _ in range(len(elem), max_column_length[i])))
                    elif columns_settings[i][1] == "end": justified_header.append("".join(" " for _ in range(0, max_column_length[i]-len(elem))) + elem)
                    elif columns_settings[i][1] == "center":
                        current_column_width = max_column_length[i]

                        if current_column_width%2 != 0:
                            if len(elem)%2 != 0: title_position = ((current_column_width-1)/2) - (len(elem)-1)/2
                            else: title_position = (current_column_width-1)/2 - len(elem)/2
                        else:
                            if len(elem)%2 == 0: title_position = (current_column_width/2) - len(elem)/2
                            else: title_position = current_column_width/2 - (len(elem)-1)/2

                        justified_header.append(" "*(int(title_position)) + elem + " "*(current_column_width - len(elem) - int(title_position)))
                else: justified_header.append(" "*max_column_length[i])
        
        if header_visible:
            table_ += theme["v"] + theme["v"].join(justified_header) + theme["v"] + "\n"
            table_ += theme["l"] + "".join((theme["h"]*max_column_length[i] + theme.get("c")) for i in range(0, len(max_column_length)))[:-1] + theme["r"] + "\n"

        for i in range(1 if header_visible else 0, len(table)):
            row = table[i]
            table_ += "".join(theme["v"] + elem + "".join(" " for _ in range(len(elem), max_column_length[j])) for j, elem in enumerate(row)) + theme["v"] + "\n"

        table_ += theme["bl"] + "".join((theme["h"]*max_column_length[i] + theme.get("b")) for i in range(0, len(max_column_length)))[:-1] + theme["br"]


        #table_ += "".join(theme["v"] + elem + "".join(" " for _ in range(len(elem), max_column_length[i])) for i, elem in enumerate(table[0])) + theme["v"]

        self._table = table_

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
        self._inner_text = str(inner_text)
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

    def set_title(self, title: str = None, justify: str = "center", padding: tuple = (0, 0)) -> None:
        self._title = str(title)
        self._justify_title = justify if justify in Panel.JUSTIFY else "center"
        self._title_padding = padding if len(padding) == 2 else (0, 0)
    
    def set_inner_text(self, inner_text: str = None, inner_text_padding: tuple = (0, 0, 0, 0), default_width: str = "inner_text", overflow: str = "hidden") -> None:
        self._inner_text = str(inner_text)
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
    justify_title="start",
    title_padding=(10, 0),
    inner_text_padding=(1, 0, 10, 1), # left, right, top, bottom
    inner_text = "This is a sample line!\nThis is another sample line!\nThis is reallllllllyyyyyyyyyyyyyyyyyyy looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong textttttt\n\nShe had never observed his face more composed and she grabbed his hand and held it to her heart. It was resistless and dry. The outline of a skull was plain under his skin and the deep burned eye sockets seemed to lead into the dark tunnel where he had disappeared. She leaned closer and closer to his face, looking deep into them, trying to see how she had been cheated or what had cheated her, but she couldn't see anything. She shut her eyes and saw the pin point of light but so far away that she could not hold it steady in her mind. She felt as if she were blocked at the entrance of something. She sat staring with her eyes shut, into his eyes, and felt as if she had finally got to the beginning of something she couldn't begin, and she saw him moving farther and farther away, farther and farther into the darkness until he was the pin point of light.",
    theme = "rounded", 
    default_width="",
    overflow="new_line"
)
panel2 = Panel(
    inner_text = "This is a sample text!",
    theme = "heavy",
    default_width = "terminal"
)

panel3 = Panel(width=25, default_width="inner_text")

panel3.set_title(
    title = " TITLE "
)

panel3.set_inner_text(
    inner_text = "12345678901234567890124",
    default_width = "terminal",
    inner_text_padding= (0, 2, 0, 0)
)

print(panel1)
# print(panel2)
print(panel3)

table1 = Table(
    title="Popular Tech Gadgets of the Decade",
    theme="rounded",
    responsive=True,
    show_header = True
)

table1.add_column(text="Released", justify="center", decorate=False)
table1.add_column(text="Product", justify="center", decorate=False)
table1.add_column(text="Units Sold", justify="center", decorate=False)
table1.add_column(text="Manufacturer", justify="center", decorate=True)

table1.add_row("Nov 10, 2020", "PlayStation 5", "58 million+", "Sony")
table1.add_row("Oct 13, 2020", "iPhone 12", "100 million+", "Apple")
table1.add_row("Oct 6, 2020", "Google Pixel 5", "7 million+", "Google")
table1.add_row("Mar 3, 2017", "Nintendo Switch", "141 million+", "Nintendo")
table1.add_row("Oct 26, 2018", "OnePlus 6T", "15 million+", "OnePlus")
table1.add_row("Mar 25, 2019", "AirPods 2", "90 million+", "Apple")
table1.add_row("Jul 25, 2019", "Samsung Galaxy Note 10", "9 million+", "Samsung")
table1.add_row("Oct 13, 2016", "Google Home", "55 million+", "Google")
table1.add_row("Sep 18, 2015", "Amazon Echo (2nd Gen)", "40 million+", "Amazon")
table1.add_row("Nov 12, 2019", "Disney+ Subscription Launch", "160 million+", "Disney")
table1.add_row("Mar 24, 2021", "Xiaomi Mi 11 Ultra", "4 million+", "Xiaomi")
table1.add_row("Apr 15, 2021", "Huawei P50 Pro", "3 million+", "Huawei")
table1.add_row("Oct 4, 2023", "Meta Quest 3", "1.5 million+", "Meta")
table1.add_row("Nov 3, 2017", "Tesla Model 3", "2 million+", "Tesla")
table1.add_row("Sep 21, 2018", "Apple Watch Series 4", "33 million+", "Apple")

# print(table1)



# terminal_dimensions = shutil.get_terminal_size()

# print(f"Width: {terminal_dimensions.columns}")
# print("".join("=" for _ in range(0, terminal_dimensions.columns)))
# print(beautify(text))
# print("".join("=" for _ in range(0, terminal_dimensions.columns)))
# print(text)