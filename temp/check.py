import shutil
text = "She had never observed his face more composed and she grabbed his hand and held it to her heart. It was resistless and dry. The outline of a skull was plain under his skin and the deep burned eye sockets seemed to lead into the dark tunnel where he had disappeared. She leaned closer and closer to his face, looking deep into them, trying to see how she had been cheated or what had cheated her, but she couldn't see anything. She shut her eyes and saw the pin point of light but so far away that she could not hold it steady in her mind. She felt as if she were blocked at the entrance of something. She sat staring with her eyes shut, into his eyes, and felt as if she had finally got to the beginning of something she couldn't begin, and she saw him moving farther and farther away, farther and farther into the darkness until he was the pin point of light."

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


terminal_dimensions = shutil.get_terminal_size()

print(f"Width: {terminal_dimensions.columns}")
print("".join("=" for _ in range(0, terminal_dimensions.columns)))
print(beautify(text))
print("".join("=" for _ in range(0, terminal_dimensions.columns)))
print(text)