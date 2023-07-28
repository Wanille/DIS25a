import csv
import json


def convert(csv_file):
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row != ['', '', '', '', '']]
        rows = rows[1:]
        _, _, chat_input, chat_output, _ = zip(*rows)
        last_input = ""
        all_langs = {inp: [] for inp in chat_input}
        for inp, out in zip(chat_input, chat_output):
            if inp != "":
                last_input = inp

            all_langs[last_input].append(out)

    with open("lang_file.json", "w") as f:
        json.dump(all_langs, f, indent=4)


if __name__ == "__main__":
    convert("sentences.csv")
