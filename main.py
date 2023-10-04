import customtkinter as ctk
import pandastable as pdt
import pandas as pd
import tkinter as tk
import re
from tkinter import filedialog
from os.path import expanduser
from collections import Counter


class VerbosityMeter:
    def __init__(self) -> None:
        self.WINDOW = ctk.CTk()
        self.WINDOW.title("VerbosityMeter")
        self.WINDOW.geometry('425x384')

        self.label = ctk.CTkTextbox(
            master=self.WINDOW,
            activate_scrollbars=False,
            wrap=tk.NONE,
            font=(None, 12)
        )

        self.label.insert(tk.END, "Choose a file so that the program counts the most common words")
        self.label.configure(
            state='disabled',
            width=ctk.CTkFont().measure("Choose a file so that the program counts the most common words") + 41,
            height=10,
        )

        self.button = ctk.CTkButton(
            master=self.WINDOW,
            text="Open File...",
            command=self.count_words,
            height=60
        )

        self.label.pack()

        self.button.pack(anchor=tk.N, pady=30)

    def set_table(self, data: pd.DataFrame):

        try:
            self.table_frame.destroy()
        except AttributeError:
            pass

        self.table_frame = ctk.CTkFrame(self.WINDOW)
        self.table_frame.pack(
            anchor=tk.CENTER,
        )
        self.table = pdt.Table(
            self.table_frame,
            dataframe=data,
            editable=False,
        )
        self.table.show()

    def get_filepath():
        filepath = filedialog.askopenfilename(
            initialdir=expanduser("~"),
            title="Select a File.",
            filetypes=[('Text Files', '.txt'), ('Any Files', '*')]
        )
        return filepath

    def count_words(self, filepath=None):
        if not filepath:
            filepath = VerbosityMeter.get_filepath()

        word_counter = Counter()
        with open(filepath) as textfile:
            for line in textfile:
                words = re.findall(r'[a-zA-Z]+', line.upper())
                word_counter.update(words)

        most_common_words = word_counter.most_common(10)
        data = pd.DataFrame(
            most_common_words,
            columns=['Word', 'Frequency']
        )

        self.set_table(data)


ROOT = VerbosityMeter()
ROOT.WINDOW.mainloop()
