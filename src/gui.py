import webbrowser
import PIL
import tkinter as tk

import customtkinter as ctk
import pandastable as pdt

class GUI:
    def __init__(self) -> None:
        self.setup_WINDOW()
        self.setup_menubar()
        self.setup_main_interface()
        self.dark_theme()
        self.table_frame = None
        self.table = None

    def setup_WINDOW(self):
        # WINDOW
        self.WINDOW = ctk.CTk()
        self.WINDOW.title("VerbosityMeter")
        self.WINDOW.geometry("425x384")
        self.WINDOW.bind("<Alt_L>", self.toggle_menubar)
        iconpng = tk.PhotoImage(file="../assets/icons/icon256x256.png")
        self.WINDOW.iconphoto(False, iconpng)

    def setup_menubar(self):
        # MENUBAR
        self.menubar = tk.Menu(self.WINDOW, bd=0)
        self.WINDOW.config(menu=self.menubar)

        # FILE
        self.file_menubar = tk.Menu(self.menubar, tearoff=False)
        self.file_menubar.add_command(label="Open File...", command=self.count_words)
        self.file_menubar.add_command(label="Export table as...", command=self.export_table)
        self.file_menubar.add_command(label="Exit", command=quit)

        # VIEW
        self.view_menubar = tk.Menu(self.menubar, tearoff=False)
        self.view_menubar.add_command(label="Hide menubar", accelerator="Alt", command=self.toggle_menubar)
        self.view_theme_menubar = tk.Menu(self.view_menubar, tearoff=False)
        self.view_theme_menubar.add_command(label="Dark", command=self.dark_theme)
        self.view_theme_menubar.add_command(label="Light", command=self.light_theme)

        self.view_menubar.add_cascade(label="Theme", menu=self.view_theme_menubar)


        # HELP
        self.help_menubar_menu = tk.Menu(self.menubar,tearoff=False        )
        self.help_menubar_menu.add_command(label="Documentation", command=self.open_online_documentation)
        self.help_menubar_menu.add_command(label="About", command=self.create_about)


        self.menubar.add_cascade(label="File", menu=self.file_menubar)
        self.menubar.add_cascade(label="View", menu=self.view_menubar)
        self.menubar.add_cascade(label="Help", menu=self.help_menubar_menu)

    def setup_main_interface(self):
        # Title
        self.label = ctk.CTkTextbox(
            master=self.WINDOW,
            activate_scrollbars=False,
            wrap=tk.NONE,
            font=(None, 12)
        )
        self.label.insert(
            tk.END, "Choose a file so that the program counts the most common words")
        self.label.configure(
            state="disabled",
            width=ctk.CTkFont().measure(
                "Choose a file so that the program counts the most common words") + 41,
            height=10,
        )
        self.label.pack()

        # Button
        self.button = ctk.CTkButton(
            master=self.WINDOW,
            text="Open File...",
            command=self.count_words,
            height=60
        )
        self.button.pack(anchor=tk.N, pady=30)

    def render_table(self):
        if self.table_frame:
            self.table_frame.destroy()
            self.table.destroy()

        self.table_frame = ctk.CTkFrame(self.WINDOW)
        self.table_frame.pack(
            anchor=tk.CENTER,
        )
        self.table = pdt.Table(
            self.table_frame,
            dataframe=self.data,
            editable=False,
            rows=10,
            cols=2
        )
        self.table.show()

    def open_online_documentation(self):
        webbrowser.open(
            "https://github.com/Hoklifter/VerbosityMeter/tree/main/docs/user_guide.md")

    def create_about(self):
        self.about_window = ctk.CTkToplevel(master=self.WINDOW)
        self.about_window.transient(self.WINDOW)
        self.about_window.title("About")
        self.about_window.geometry("500x300")
        self.about_window.resizable(False, False)

        self.about_img = ctk.CTkLabel(
            self.about_window,
            image=ctk.CTkImage(
                PIL.Image.open("../assets/icons/icon2048x2048.png"),
                None,
                (150, 150)
            ),
            text="",
            height=170
        )
        self.about_img.pack()

        self.about_title = ctk.CTkLabel(
            self.about_window,
            text="VerbosityMeter",
            font=ctk.CTkFont(weight="bold")
        )
        self.about_title.pack()

        self.about_version = ctk.CTkLabel(
            self.about_window,
            text="1.0.0"
        )
        self.about_version.pack()

        self.about_desc = ctk.CTkLabel(
            self.about_window,
            text="""Verbosity Meter simplifies the analysis of word frequencies
in text files through an intuitive Tkinter interface."""
        )
        self.about_desc.pack()

    # Pop-ups to send messages to the user
    def popup(self, type, message):
        colors = {
            "error": "#FF0000",  # Red
            "warning": "#FFFF00",  # Yellow
            "success": "#00FF00",  # Green
        }

        pass

    # Change program theme to Dark
    def dark_theme(self):
        ctk.set_appearance_mode("dark")

        menubar_elements = [
            self.menubar,
            self.file_menubar,
            self.view_menubar,
            self.view_theme_menubar,
            self.help_menubar_menu
        ]

        for element in menubar_elements:
            element.config(
                bg="black",
                fg="white"
            )

    # Change program theme to Light
    def light_theme(self):
        ctk.set_appearance_mode("light")

        menubar_elements = [
            self.menubar,
            self.file_menubar,
            self.view_menubar,
            self.view_theme_menubar,
            self.help_menubar_menu
        ]

        for element in menubar_elements:
            element.config(
                bg="white",
                fg="black"
            )

    def toggle_menubar(self, *args):
        if self.menubar.winfo_exists():
            self.menubar.destroy()
            self.WINDOW.config(menu=tk.Label())
        else:
            self.setup_menubar()

        if ctk.AppearanceModeTracker.appearance_mode:
            self.dark_theme()
        else:
            self.light_theme()
