import shutil
import math

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
    
    @classmethod
    def terminal_width(cls) -> int:
        return shutil.get_terminal_size().columns

    def __init__(
        self,
        title: str = None,
        show_header: bool = True,
        theme: str = "light",
        beautify_rows: bool = False,
        responsive: bool = True,
        column_separator: str = None # when show_header is false, this feature can be used to replace the typical "line" separator (theme['v']) with a custom separator, for example -> ':'
    ) -> None:
        
        self._title = title
        self._show_header = show_header
        self._theme = theme if theme in Table.THEMES else "light"
        self._beautify_rows = beautify_rows
        self._responsive = responsive
        self._table = None
        self._column_separator = column_separator

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
            text,
            justify if justify in Table.JUSTIFY else "center",
            padding if len(padding) == 2 else (0, 0),
            decorate
        ))

    def add_columns(self, *args: str) -> None:
        for arg in args: self._columns.append((arg, "center", (0, 0), True))

    def add_row(self, *values) -> None:
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
        if (not header_visible) and (not self._column_separator is None): table_ += theme["tl"] + theme["h"]*(table_width-2) + theme["tr"] + "\n"
        else: table_ += theme["tl"] + "".join((theme["h"]*max_column_length[i] + theme.get("t")) for i in range(0, len(max_column_length)))[:-1] + theme["tr"] + "\n"

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

        if (not header_visible) and (not self._column_separator is None):
            for i in range(1 if header_visible else 0, len(table)):
                row = table[i]
                table_ += theme["v"] + ("".join(str(self._column_separator) + elem + "".join(" " for _ in range(len(elem), max_column_length[j])) for j, elem in enumerate(row)))[1:] + theme["v"] + "\n"
        else:
            for i in range(1 if header_visible else 0, len(table)):
                row = table[i]
                table_ += "".join(theme["v"] + elem + "".join(" " for _ in range(len(elem), max_column_length[j])) for j, elem in enumerate(row)) + theme["v"] + "\n"

        if (not header_visible) and (not self._column_separator is None): table_ += theme["bl"] + theme["h"]*(table_width-2) + theme["br"]
        else: table_ += theme["bl"] + "".join((theme["h"]*max_column_length[i] + theme.get("b")) for i in range(0, len(max_column_length)))[:-1] + theme["br"]


        #table_ += "".join(theme["v"] + elem + "".join(" " for _ in range(len(elem), max_column_length[i])) for i, elem in enumerate(table[0])) + theme["v"]

        self._table = table_

class Panel:
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
    DEFAULT_WIDTH = ["inner_text", "terminal"]
    OVERFLOW = ["hidden", "new_line"]
    JUSTIFY = ["start", "end", "center"]

    @classmethod
    def get_theme(cls, name: str) -> str | None:
        return cls.THEMES.get(name)

    @classmethod
    def terminal_width(cls) -> int:
        return shutil.get_terminal_size().columns

    def __init__(
            self,
            title: str = None,
            justify_title: str = "center",
            title_padding: tuple = (0, 0), # left, right
            header_text: str = None, # if header is added, title won't be visible.
            justify_header: str = "center",
            header_padding: tuple = (0, 0, 0, 0), # left, right, top, bottom
            inner_text: str = None,
            inner_text_padding: tuple = (0, 0, 0, 0), # left, right, top, bottom
            theme: str = "light",
            width: int = None,
            default_width = "inner_text",
            height: int = None,
            overflow: str = "hidden", # values possible: hidden, dotted, new_line
            automatic_padding_reduction: bool = False # setting this to true would help in cases where the inner text is not that big and the user wants to add more padding to beautify the output, but since it can cause problems in small terminals, user wants to reduce the padding instead of compressing the text in cases of small terminals
        ) -> None:
        self._title = title
        self._justify_title = justify_title if justify_title in Panel.JUSTIFY else "center"
        self._title_padding = title_padding if len(title_padding) == 2 else (0, 0)
        self._header_text = header_text
        self._justify_header = justify_header if justify_header in Panel.JUSTIFY else "center"
        self._header_padding = header_padding if len(header_padding) == 4 else (0, 0, 0, 0)
        self._theme = theme if theme in Panel.THEMES else "light"
        self._width = width
        self._default_width = default_width if default_width in Panel.DEFAULT_WIDTH else "inner_text"
        self._height = height
        self._overflow = overflow if overflow in Panel.OVERFLOW else "hidden"
        self._automatic_padding_reduction = automatic_padding_reduction

        self.__panel = ""
        self.__inner_text_list = [[inner_text.split("\n"), inner_text_padding if len(inner_text_padding) == 4 else (0, 0, 0, 0), overflow if overflow in Panel.OVERFLOW else "hidden"]] if inner_text is not None else []
    
    def __str__(self):
        self.__update_panel()
        return self.__panel

    def set_title(self, title: str = None, justify: str = "center", padding: tuple = (0, 0)) -> None:
        self._title = title
        self._justify_title = justify if justify in Panel.JUSTIFY else "center"
        self._title_padding = padding if len(padding) == 2 else (0, 0)
    
    def set_header(self, text: str = None, justify: str = "center", padding: tuple = (0, 0, 0, 0)) -> None:
        self._header_text = text
        self._justify_header = justify if justify in Panel.JUSTIFY else "center"
        self._header_padding = padding if len(padding) == 4 else (0, 0, 0, 0)
    
    def add_inner_text(self, inner_text: str = None, inner_text_padding: tuple = (0, 0, 0, 0), overflow: str = "hidden") -> None:
        self.__inner_text_list.append([inner_text.split("\n") if inner_text is not None else "", inner_text_padding if len(inner_text_padding) == 4 else (0, 0, 0, 0), overflow if overflow in Panel.OVERFLOW else "hidden"])

    def __update_panel(self) -> None:
        
        inner_text_list = self.__inner_text_list
        terminal_width = shutil.get_terminal_size().columns

        header_text = self._header_text
        justify_header = self._justify_header
        header_padding = self._header_padding

        title = self._title
        justify_title = self._justify_title
        title_padding = self._title_padding

        theme = Panel.THEMES[self._theme]
        panel = ""

        # first maximum table width will be calculated

        # setting the maximum length of the table as the lenght of the max(header, title), and will be comparing it with the inner texts length in the for loop
        max_panel_length = max(len(header_text) + header_padding[0] + header_padding[1] + 2 if header_text is not None else 0, len(title) + 2 if title is not None else 0)
        
        # to do so, first we need to check and compress if the inner text exceeds the terminal width or the width specified by the user
        for i, inner_text_ in enumerate(inner_text_list):

            inner_text = inner_text_[0]
            inner_text_padding = inner_text_[1]
            overflow = inner_text_[2]
            max_inner_text_length = len(max(inner_text, key=len))

            if max_inner_text_length + 2 + inner_text_padding[0] + inner_text_padding[1] > terminal_width:

                # first checking whether if changing the inner text padding would solve the issue or not
                if max_inner_text_length < terminal_width and self._automatic_padding_reduction:
                    # only reducing the right padding
                    inner_text_padding = (inner_text_padding[0], (inner_text_padding[1] - (max_inner_text_length + 2 + inner_text_padding[0] + inner_text_padding[1] - terminal_width) if not (max_inner_text_length+ 2 + inner_text_padding[0] + inner_text_padding[1]-terminal_width) > inner_text_padding[1] else 0), inner_text_padding[2], inner_text_padding[3])

                # changing the lines which would cause a problem:
                new_inner_text = []
                for line in inner_text:
                    if len(line) + 2 + inner_text_padding[0] + inner_text_padding[1] > terminal_width:
                        if overflow == "new_line": new_inner_text += self.__beautify(text = line, width = (terminal_width - 2 - inner_text_padding[0] - inner_text_padding[1])).split("\n")
                        else: new_inner_text.append(line[0:(terminal_width - 2 - inner_text_padding[0] - inner_text_padding[1] - 3)] + "...")
                    else:
                        new_inner_text.append(line)

                inner_text_list[i] = [new_inner_text, inner_text_padding, overflow]
            
            # getting the maximum length for this inner text and comparing it with max_panel_length
            max_panel_length = max(max_panel_length, (len(max(inner_text_list[i][0], key=len)) + 2 + inner_text_padding[0] + inner_text_padding[1]))

        # till here we have the maximum panel length, before starting with table building we need to take care of the default_width

        if len(inner_text_list) == 0 and self._default_width == "inner_text": self._width = terminal_width
        elif self._default_width == "inner_text" and self._width is None: self._width = max_panel_length
        elif self._default_width == "terminal" and self._width is None: self._width = terminal_width
        width = self._width

        # now that we have the table width, we can proceed with table building

        # first taking care of the first line/header stuff
        first_line = ""
        if self._header_text is None:
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
        else:
            if justify_header == "start": header_position = (1+header_padding[0]) # since justify is start, we're only considering the left padding
            elif justify_header == "end": header_position = ((width-1) - len(header_text) - header_padding[1])
            else: header_position = math.floor((width-len(header_text))/2.0)

            first_line = theme["tl"] + theme["h"]*(width-2) + theme["tr"] + "\n"
            first_line += (theme["v"] + " "*int(header_position) + header_text + " "*((width-2) - len(header_text) - int(header_position)) + theme['v'] + "\n")
            first_line += theme["l"] + theme["h"]*(width-2) + theme["r"]
        
        panel += (first_line + "\n")

        # starting with the middle lines, since it involves inner_text, will be iterating through a for loop through inner_text_list
        for i, inner_text_ in enumerate(inner_text_list):

            inner_text = inner_text_[0]
            inner_text_padding = inner_text_[1]
            height = self._height if (self._height != 0 and self._height is not None) else len(inner_text)+2

            middle_lines = ""
            middle_lines += (theme["v"] + " "*(width-2) + theme["v"] + "\n")*inner_text_padding[2]

            for j in range(0, height-2):
                line = theme["v"]
                line += " "*inner_text_padding[0]
                line += inner_text[j]
                line += " "*(width-2 - inner_text_padding[0] - len(inner_text[j]))
                line += theme["v"]
                middle_lines += (line + "\n")
            
            middle_lines += (theme["v"] + " "*(width-2) + theme["v"] + "\n")*inner_text_padding[3]

            panel += middle_lines
            panel += (theme["l"] + theme["h"]*(width-2) + theme["r"] + "\n") if i != len(inner_text_list)-1 else (theme["bl"] + theme["h"]*(width-2) + theme["br"])

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
    
class Line:
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
    def terminal_width(cls) -> int:
        return shutil.get_terminal_size().columns

    def __init__(self):
        pass

    @classmethod
    def get_line(
        cls,
        theme: str = "light",
        text: str = None,
        justify_text: str = "center",
        text_padding: tuple = (0, 0), # left, right,
        justify_line: str = "start",
        line_padding: tuple = (0, 0, 0, 0), # left, right, top, bottom
        width: int = None,
        width_percentage: int = None # user enters the percentage of the terminal size the user wants the line to be
    ) -> str:
        theme = cls.THEMES[theme] if theme in cls.THEMES else cls.THEMES["light"]
        justify_text = justify_text if justify_text in cls.JUSTIFY else "center"
        text_padding = text_padding if len(text_padding) == 2 else (0, 0)
        line_padding = line_padding if len(line_padding) == 4 else (0, 0, 0, 0) # left, right, top, bottom
        justify_line = justify_line if justify_line in cls.JUSTIFY else "start"
        terminal_width = shutil.get_terminal_size().columns

        if width_percentage is not None: width = math.floor((width_percentage/100.0)*terminal_width)
        if width is not None and width > terminal_width: width = terminal_width
        if width is None or width == 0: width = terminal_width
        text_position = 0

        if text is not None:
            if justify_text == "center":
                if width%2 != 0:
                    if len(text)%2 != 0: text_position = ((width-1)/2) - (len(text)-1)/2
                    else: text_position = (width-1)/2 - len(text)/2
                else:
                    if len(text)%2 == 0: text_position = (width/2 - 1) - len(text)/2
                    else: text_position = width/2 - (len(text)-1)/2
            elif justify_text == "end": text_position = (width - len(text) - text_padding[1])
            elif justify_text == "start": text_position = text_padding[0]

        text_position = int(text_position)
        line = theme["h"]*width if text is None else theme["h"]*text_position + text + theme["h"]*(width - text_position - len(text))

        if width == terminal_width or justify_line == "start": line = " "*line_padding[0] + line
        elif justify_line == "end": line = " "*(terminal_width - width - line_padding[1]) + line
        else: line = " "*int(math.floor((terminal_width - width)/2.0)) + line

        return "\n"*line_padding[2] + line + "\n"*line_padding[3]

    @classmethod
    def print_line(
        cls,
        theme: str = "light",
        text: str = None,
        justify_text: str = "center",
        text_padding: tuple = (0, 0), # left, right,
        justify_line: str = "start", 
        line_padding: tuple = (0, 0, 0, 0), # left, right, top, bottom
        width: int = None,
    ) -> None:
        print(cls.get_line(theme, text, justify_text, text_padding, justify_line, line_padding, width), end = "")