import shutil
import math
text = "She had never observed his face more composed and she grabbed his hand and held it to her heart. It was resistless and dry. The outline of a skull was plain under his skin and the deep burned eye sockets seemed to lead into the dark tunnel where he had disappeared. She leaned closer and closer to his face, looking deep into them, trying to see how she had been cheated or what had cheated her, but she couldn't see anything. She shut her eyes and saw the pin point of light but so far away that she could not hold it steady in her mind. She felt as if she were blocked at the entrance of something. She sat staring with her eyes shut, into his eyes, and felt as if she had finally got to the beginning of something she couldn't begin, and she saw him moving farther and farther away, farther and farther into the darkness until he was the pin point of light."

class Table:
    def __init__(self):
        pass

class Panel:
    THEMES = {
        "light": {"h": "─", "v": "│", "tl": "┌", "tr": "┐", "bl": "└", "br": "┘"},
        "double": {"h": "═", "v": "║", "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝"},
        "rounded": {"h": "─", "v": "│", "tl": "╭", "tr": "╮", "bl": "╰", "br": "╯"},
    }

    @classmethod
    def get_theme(cls, name: str) -> str | None:
        return cls.THEMES.get(name)

    def __init__(
            self,
            title: str = None,
            justify_title: str = "center",
            title_padding: tuple = (0, 0), #left, right
            inner_text: str = None,
            theme: str = "round",
            width: int = None,
            default_width = "inner_text",
            height: int = None
        ) -> None:
        self.title = title
        self.justify_title = justify_title
        self.title_padding = title_padding if len(title_padding) == 2 else (0, 0)
        self.inner_text = inner_text
        self.theme = theme if theme in Panel.THEMES else "round"
        self.width = shutil.get_terminal_size().columns if width is None else width
        self.default_width = default_width if default_width in ["inner_text", "terminal"] else "inner_text"
        self.height = height

        self.__panel = ""
    
    def __str__(self):
        self.__update_panel()
        return self.__panel

    @property
    def maximum_line_length() -> int:
        pass

    def __update_panel(self) -> None:
        inner_text = self.inner_text.split("\n")
        title = self.title
        justify_title = self.justify_title
        title_padding = self.title_padding

        width = self.width
        height = self.height if self.height != 0 else len(inner_text)+2
        theme = Panel.THEMES[self.theme]
        panel = ""

        # dealing with first line
        # the position variables considers the literal position (first place is zero)
        first_line = ""
        if title is not None:
            if justify_title == "start": title_position = (1+title_padding[0]) # since justify is start, we're only considering the left padding
            elif justify_title == "end": title_position = ((width-1-1) - title_padding[1])
            else:
                if width%2 != 0:
                    if len(title)%2 != 0: title_position = ((width-1)/2) - (len(title)-1)/2
                    else: title_position = (width-1)/2 - len(title)/2
                else:
                    if len(title)%2 == 0: title_position = (width/2 - 1) - len(title)/2
                    else: title_position = width/2 - (len(title)-1)/2

            first_line = theme["tl"]
            first_line += "".join(theme["h"] for _ in range(1, title_position)) # replace these with string multiplication
            first_line += title
            first_line += "".join(theme["h"] for _ in range(title_position+len(title), width-1))
            first_line += theme["tr"]
        else: pass


        # dealing with the intermediate lines

        # dealing with last line

        # for i in range(0, height):
        #     if i == 0:
        #         pass
        #     else:
        #         pass

        #     panel+="\n"

    
panel = Panel()
print(panel)
    

# def beautify(text: str):
#     width = shutil.get_terminal_size().columns

#     text_ = text.split(" ")
#     final_text_list = []
#     current_sentence_length = 0
    
#     for word in text_:
#         if current_sentence_length + len(word) >= width:
#             final_text_list.append("\n" + word)
#             current_sentence_length = len(word)+1 # 1 is added to factor in the space which will be added later
#         else:
#             final_text_list.append(word)
#             current_sentence_length+=len(word)+1

#     return "".join((word+ " ") for word in final_text_list)


# terminal_dimensions = shutil.get_terminal_size()

# print(f"Width: {terminal_dimensions.columns}")
# print("".join("=" for _ in range(0, terminal_dimensions.columns)))
# print(beautify(text))
# print("".join("=" for _ in range(0, terminal_dimensions.columns)))
# print(text)