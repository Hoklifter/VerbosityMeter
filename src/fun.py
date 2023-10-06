from tkinter import filedialog
from os.path import expanduser, splitext
from unidecode import unidecode
from re import findall
from collections import Counter
from pandas import DataFrame


class FUN:
    def __init__(self) -> None:
        # DataFrame data
        self.data = None

    def get_filepath(self):
        filepath = filedialog.askopenfilename(
            initialdir=expanduser("~"),
            title="Select a File.",
            filetypes=[("Text Files", ".txt"), ("Any Files", "*")]
        )
        return filepath

    # Counts the 10 most commmon words in a readable file and calls table render.
    def count_words(self):
        filepath = self.get_filepath()
        word_counter = Counter()

        with open(filepath) as textfile:
            for line in textfile:
                words = findall(r"[a-zA-Z]+", unidecode(line.upper()))
                word_counter.update(words)

        most_common_words = word_counter.most_common(10)
        if most_common_words:
            self.data = DataFrame(
                most_common_words,
                columns=["Word", "Frequency"]
            )

            self.render_table()
        else:
            self.popup("error", "File is empty or has no words on it.")

    # Generate a new file with the table data on it.

    def export_table(self):
        if isinstance(self.data, DataFrame):
            file = filedialog.asksaveasfile(
                initialdir=expanduser("~"),
                title="Save as...",
                filetypes=[("Text File", ".txt"), ("CSV File", ".csv")]
            )
            if splitext(file.name)[1] == ".csv":
                file.write(self.data.to_csv())
            else:
                file.write(self.data.to_string())
        else:
            print("No table generated.")
            self.popup("error", "No table generated.")
