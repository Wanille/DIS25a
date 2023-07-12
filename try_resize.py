import os
import time
from pathlib import Path
import climage
import textwrap

term_size = os.get_terminal_size()


def pad_image(image, height_term, width_term, message=None):
    image = image.split("\n")[:-1]

    height_image = len(image)
    width_to_add = width_term - 100

    if message:
        message_dict = {}
        message_wrapped = textwrap.wrap(message, width=width_to_add)
        for idx, m in enumerate(message_wrapped):
            if len(m) != width_to_add:
                width_to_add_left = (width_to_add - len(m)) // 2
                width_to_add_right = width_to_add - len(m) - width_to_add_left
                message_wrapped[idx] = " "*width_to_add_left + m + " "*width_to_add_right
        message_wrapped = ["\x1b[42;40m" + m for m in message_wrapped]
        line_idx = (height_term - len(message_wrapped)) // 2
        for line in message_wrapped:
            message_dict[line_idx] = line
            line_idx += 1

    height_to_add = height_term - len(image)
    height_above = height_to_add // 2
    height_below = height_to_add - height_above
    
    empty_line = "\x1b[48;5;15m\x1b[38;5;15m▄"*width_term
    output = []
    im_lines = 0
    for total_image in range(height_term):
        if total_image <= height_above:
            output.append(empty_line)
        
        if total_image > height_above and total_image <= height_above + height_image:
            line_input = "\x1b[48;5;15m\x1b[38;5;15m▄"*width_to_add
            if message and im_lines in message_dict.keys():
                line_input = message_dict[im_lines]

            output.append(line_input + image[im_lines])
            im_lines += 1

        if total_image > height_above + height_image:
            output.append(empty_line)
    return "\n".join(output)


def play_video(folder, fps=12, with_padding=True):

    height_term = os.get_terminal_size().lines

    files = list(Path(folder).iterdir())
    for file in sorted(files):
        image = open(file, "r").read()
        image_padded = pad_image(image, height_term, 130, message=None) 
        print(image_padded)
        time.sleep(1/fps)



def pad_message(width, height, message):
    height_to_add = height - 2
    height_above = height_to_add // 2
    height_below = height_to_add - height_above
    message_padded_width = width - len(message)
    message_padded_width_left = message_padded_width // 2
    message_padded_width_right = message_padded_width - message_padded_width_left
    
    new_message = [" " for _ in range(height_above)]
    new_message.extend([" "*message_padded_width_left + message + " "*message_padded_width_right])
    new_message.extend([" " for _ in range(height_below)])
    return "\n".join(new_message)



while term_size.lines != 45 or term_size.columns != 130:
    os.system("clear")
    term_size = os.get_terminal_size()
    print(pad_message(term_size.columns, term_size.lines, f"Window size {term_size.columns}x{term_size.lines} please resize to 130x45"))
    time.sleep(1)

print(pad_message(term_size.columns, term_size.lines, "Welcome to the chatbot!"))
time.sleep(2)
play_video("animations/arrival/", fps=12)
time.sleep(1)
print(pad_image(open("animations/clippy_idle.txt", "r").read(), 42, 130, "Hello, I am Clippy! I am here to help you with your work! What is your name?"))  
print("\x1b[42;40m\n")
input("\x1b[38;5;118m>>> \x1b[37;40m")
print(pad_image(open("animations/clippy_idle.txt", "r").read(), 42, 130, "Too long didn't read! I will call you 'User'!"))  
print("\x1b[42;40m\n")
input("\x1b[38;5;118m>>> \x1b[37;40m")


# play_video("nggyu/txt_convert", fps=12)