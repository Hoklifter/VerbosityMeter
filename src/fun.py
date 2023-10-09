from tkinter import filedialog
import os.path
from unidecode import unidecode
import re
from collections import Counter

from pandas import DataFrame


class FUN:
    def __init__(self) -> None:
        # DataFrame data
        self.regex = r"[a-zA-Z]+"

    # Generate a new file with the table data on it.
    def get_filepath(self):
        filepath = filedialog.askopenfilename(
            initialdir=os.path.expanduser("~"),
            title="Select a File.",
            filetypes=[("Text Files", ".txt"), ("Any Files", "*")]
        )
        return filepath

    # Counts the 10 most commmon words in a readable file and calls table render.
    def count_words(self):
        filepath = self.get_filepath()
        word_counter = Counter()

        if filepath:
            try:
                with open(filepath) as textfile:
                    textfile.seek(0, 2)
                    filesize=textfile.tell()
                    if filesize/1_000_000 > 2:
                        self.push_notification("error", f"{os.path.basename(filepath)!r} is too big (2MB max)")
                        return
                    textfile.seek(0)
                    for line in textfile:
                        words = re.findall(self.regex, unidecode(line.upper()))
                        word_counter.update(words)

                most_common_words = word_counter.most_common(10)
                if most_common_words:
                    self.data = DataFrame(
                        most_common_words,
                        columns=["Word", "Frequency"]
                    )
                    self.render_table()
                    self.push_notification('info', f"{os.path.basename(filepath)!r} opened")
                else:
                    self.push_notification("error", f"{os.path.basename(filepath)!r} is empty or has no matches.")
            except UnicodeDecodeError:
                self.push_notification("error", f"{os.path.basename(filepath)!r} is not supported")


    # Generate a new file with the table data on it.
    def export_table(self):
        try:
            self.data
        except AttributeError:
            self.push_notification("error", "No table generated.")
            return

        try:
            file = filedialog.asksaveasfile(
                initialdir=os.path.expanduser("~"),
                title="Save as...",
                filetypes=[("Text File", ".txt"), ("CSV File", ".csv")]
            )
        except PermissionError:
            self.push_notification("error", f"Name is invalid or Permision Denied.")
            return

        if file:
            if os.path.splitext(file.name)[1] == ".csv":
                file.write(self.data.to_csv())
            else:
                file.write(self.data.to_string())
            self.push_notification("success", f"{os.path.basename(file.name)} has been saved succesfully.")

    # Changes the search pattern to set table data.
    def change_regex(self):
        if self.regex_entry.get():
            try:
                re.compile(self.regex_entry.get())
                self.regex = self.regex_entry.get()
                self.push_notification('info', f'New RegEx Pattern: {self.regex!r}')
            except re.error:
                self.push_notification('error', 'Invalid RegEx pattern')
        else:
            self.push_notification('error', 'Empty pattern.')
