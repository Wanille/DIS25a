import os
import time
from pathlib import Path
import textwrap
import json
import random
import re
from typing import Optional, Union
import pickle
import sklearn
from Cleaner import clean_text 
from recommender import recommend_by_str


with open("Pickles/LR_Model", "rb") as f:
    lr_model = pickle.load(f)


with open("Pickles/Vectorizer", "rb") as f:
    vectorizer = pickle.load(f)


with open("Pickles/NB_Model", "rb") as f:
    nb_model = pickle.load(f)

class DocumentWrapper(textwrap.TextWrapper):
    """credit: https://stackoverflow.com/a/45287550/21042595"""
    def wrap(self, text):
        split_text = text.split('\n')
        lines = [line for para in split_text for line in textwrap.TextWrapper.wrap(self, para)]
        return lines


video_folders = {
    "posix": {
        "arrival": "animations/arrival/",
        "exit": "animations/exit/",
        "point_left": "animations/point_left/",
        "point_down": "animations/point_down/",
        "idle": "animations/idle/",
        "read": "animations/read/",
        "scratches": "animations/scratches/",
        "sleepy": "animations/sleepy/",
        "exclamation": "animations/exclamation/",
        "big_eyes": "animations/big_eyes/",
        "idle_img": "animations/clippy_idle.txt"
    },
    "nt": {
        "arrival": "animations/windows/arrival/",
        "exit": "animations/windows/exit/",
        "point_left": "animations/windows/point_left/",
        "point_down": "animations/windows/point_down/",
        "idle": "animations/windows/idle/",
        "read": "animations/windows/read/",
        "scratches": "animations/windows/scratches/",
        "sleepy": "animations/windows/sleepy/",
        "exclamation": "animations/windows/exclamation/",
        "big_eyes": "animations/windows/big_eyes/",
        "idle_img": "animations/windows/clippy_idle.txt"
    }
}



class Chatbot:
    def __init__(self):
        self.term_size = (150, 45)
        self.history = {"user": [], "bot": []}
        self.bot_name = None
        self.user_name = None
        self.user_input = None
        self.plattform = os.name
        self.video_locations = video_folders[self.plattform]
        self.sentences = json.load(open("lang_file.json", "r"))
        self.wrapper = DocumentWrapper(width=self.term_size[0] - 100)

    def resize_terminal(self, width, height):
        term_size = os.get_terminal_size()
        while term_size.lines != height or term_size.columns != width:
            os.system("clear")
            term_size = os.get_terminal_size()
            print(self.pad_message_middle(term_size.columns, term_size.lines, f"Window size {term_size.columns}x{term_size.lines} please resize to {width}x{height}"))
            time.sleep(1)


    def pad_message_middle(self, width, height, message):
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


    def pad_image(self, image, height_term, width_term, message=None):

        image = image.split("\n")[:-1]

        height_image = len(image)
        width_to_add = width_term - 100

        if message:
            message_dict = {}
            message_wrapped = self.wrapper.wrap(message)
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


    def play_video(self, folder, fps=12, with_padding=True, message: Optional[Union[str, list]]=None):
        
        try:
            if self.history["bot"][-1] != message:
                self.history["bot"].append(message)
        except IndexError:
            pass
        height_term = os.get_terminal_size().lines
        files = list(Path(folder).iterdir())
        
        if isinstance(message, list):
            video_length = len(files)
            message_per_frames = video_length // len(message)
            counter = 0
            for idx, file in enumerate(sorted(files)):
                if idx > 0 and idx % message_per_frames == 0:
                    counter += 1

                image = open(file, "r").read()
                image_padded = self.pad_image(image, height_term, self.term_size[0], message=message[counter])
                print(image_padded)
                time.sleep(1/fps)
        else:
            for idx, file in enumerate(sorted(files)):
                image = open(file, "r").read()
                image_padded = self.pad_image(image, height_term, self.term_size[0], message=message)
             
                print(image_padded)
                time.sleep(1/fps)

    def assign_username(self):
        self.user_name = self.get_sentence("user_name")
        print(self.pad_image(open(self.video_locations["idle_img"], "r").read(), self.term_size[1] - 2, self.term_size[0], self.get_sentence("ask_user_name")))
        time.sleep(1)
        print("\x1b[42;40m\n")
        self.user_input = input("\x1b[38;5;118m➜ \x1b[37;40m")
        username_message = re.sub(r"\$user_name\$", self.user_name, self.get_sentence("user_name_message"))
        self.play_video(self.video_locations["scratches"], message=username_message)
        time.sleep(2)

    def print_welcome_message(self):
        # TODO Display welcome message with held information about bot
        self.resize_terminal(150, 45)
        self.play_video(self.video_locations["arrival"], message=None)
        time.sleep(1)
        self.assign_username()
        print(self.pad_image(open(self.video_locations["idle_img"], "r").read(), self.term_size[1] - 2, self.term_size[0], self.get_sentence("welcome_message")))
        time.sleep(1)
        self.play_video(self.video_locations["point_left"], message=self.get_sentence("welcome_message"))


    def analyse_input(self, user_input: str):
    
        # sentiment
        if (match := re.match(r'^(analyse|evaluate|check|determine|tell me).*:\s?(.+)?((using|with) (nb|lr))?$', user_input, re.IGNORECASE)):
            sentiment_sentence = match.group(2)
            model = match.group(5)
            if model not in ["nb", "lr"]:
                model = None
            return "sentiment", (sentiment_sentence, model)
        
        # jokes
        elif (match := re.match(r'.*[Jj]oke.*', user_input)):
            return "joke", None
        
        # quit
        elif (match := re.match(r'.*[Qq]uit', user_input)):
            return "exit", None
        
        # help
        elif (match := re.match(r'.*[Hh]elp', user_input)):
            return "help", None

        # recommendations
        elif (match := re.match(r'.*[Rr]ecommend.*', user_input)):
            return "recommend", user_input

        # error 
        else:
            return "error", None


    def dialog(self, task, context):
        # TODO Craft response with correct output
        if task == "exit":
            message = self.get_sentence("goodbye_message")
            print(self.pad_image(open(self.video_locations["idle_img"], "r").read(), self.term_size[1] - 2, self.term_size[0], message))
            time.sleep(1)
            self.play_video(self.video_locations["exit"], message=message)
            print("\x1b[42;0m\n")
            os.system("clear")
            os.system("clear")
            exit()
        
        if task == "help":
            animation = random.choice(["idle", "scratches", "exclamation", "big_eyes"])
            self.play_video(self.video_locations[animation], message=self.get_sentence("help_message"))

        if task == "joke":
            self.play_video(self.video_locations["idle"], message=self.get_sentence("print_joke"))

        if task == "sentiment":
            text = context[0]
            model = context[1]

            if model == None:
                model = "nb"
            
            text_clean = clean_text(text)
            text_vectorized = vectorizer.transform([text_clean])
            
            if model == "lr":
                prediction = lr_model.predict(text_vectorized)
            elif model == "nb":
                prediction = nb_model.predict(text_vectorized)
            
            if prediction == 1:
                sentiment = "sentiment_positiv"
            else:
                sentiment = "sentiment_negativ"

            if sentiment == "sentiment_negativ":
                sent_query = "sentiment_query_neg"
            else:
                sent_query = "sentiment_query_pos"
            sentence = self.get_sentence(sentiment)
            new_sentence = re.sub(r"\$input_user\$", text.rstrip(), sentence)
            self.play_video(self.video_locations["read"], message=new_sentence + "\n" + self.get_sentence(sent_query))
            print(self.pad_image(open("animations/clippy_idle.txt", "r").read(), self.term_size[1] - 2, self.term_size[0], new_sentence + "\n" + self.get_sentence(sent_query)))
            while True:
                print("\x1b[42;40m\n")
                self.user_input = input(f"\x1b[37;40m({self.user_name}) \x1b[38;5;118m➜ \x1b[37;40m")
                
                if self.user_input in ["1", "2"]:
                    self.play_video(self.video_locations["idle"], message=self.get_sentence(sent_query + "_" + self.user_input))
                    break
                elif self.user_input == "quit":
                    self.dialog("exit", None)
                    break
                else:
                    print("\x1b[42;40minhere")
                    self.play_video(self.video_locations["exclamation"], message=[self.get_sentence("error_message"), new_sentence + "\n" + self.get_sentence(sent_query)])     
            
        if task == "recommend":
            movies = recommend_by_str(context)
            if movies == []:
                self.play_video(self.video_locations["exclamation"], message=self.get_sentence("recommend_empty"))
                
            else:
                movie = random.sample(movies, 1)
                movie = movie[0]
                movie_title = movie["Title"]
                actors = ", ".join(movie["Cast"]["Stars"])
                director = ", ".join(movie["Cast"]["Director"])
                meta_score = movie["Metascore"]
                genre = ", ".join(movie["Genre"])
                
                msg = self.get_sentence("recommend_movie")
                msg = re.sub(r"\$movie_rec\$", movie_title, msg)
                msg = re.sub(r"\$actor\$", actors, msg)
                msg = re.sub(r"\$director\$", director, msg)
                msg = re.sub(r"\$meta_score\$", str(meta_score), msg)
                msg = re.sub(r"\$genre\$", genre, msg)
                
                self.play_video(self.video_locations["read"], message=msg)

        if task == "error":
            self.play_video(self.video_locations["scratches"], message=self.get_sentence("error_message"))

        # if task == "history":
        #     print(self.pad_image(open("animations/clippy_idle.txt", "r").read(), self.term_size[1] - 2, self.term_size[0], "\n".join(self.history["bot"])))


    def get_sentence(self, task):
        sentence = random.choice(self.sentences[task])
        return sentence

    def start_loop(self, skip=False):
        
        if not skip:

            self.print_welcome_message()

        print(self.pad_image(open(self.video_locations["idle_img"], "r").read(), self.term_size[1] - 2, self.term_size[0], self.get_sentence("welcome_message")))
       
        print("\x1b[42;40m\n")
        self.user_input = input(f"\x1b[37;40m({self.user_name}) \x1b[38;5;118m➜ \x1b[37;40m")
        self.history["user"].append(self.user_input)
        
        while True:
            todo, context = self.analyse_input(self.user_input)
            self.dialog(todo, context)
            print("\x1b[42;40m\n")
            self.user_input = input(f"\x1b[37;40m({self.user_name}) \x1b[38;5;118m➜ \x1b[37;40m")


if __name__ == "__main__":
    cb = Chatbot()
    cb.start_loop(skip=True)