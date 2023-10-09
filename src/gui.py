import webbrowser
import PIL
import tkinter as tk
import time

import customtkinter as ctk
import pandastable as pdt

class GUI:
    def __init__(self) -> None:
        self.setup_WINDOW()
        self.setup_menubar()
        self.setup_main_interface()
        self.dark_theme()
        self.notification = ctk.CTkLabel(master=self.WINDOW)


    def setup_WINDOW(self):
        # WINDOW
        self.WINDOW = ctk.CTk()
        iconpng = tk.PhotoImage(file="../assets/icons/icon256x256.png")
        self.WINDOW.title("VerbosityMeter")
        self.WINDOW.geometry("600x550")
        self.WINDOW.resizable(False, False)
        self.WINDOW.iconphoto(False, iconpng)
        self.WINDOW.bind("<Alt_L>", self.toggle_menubar)
        self.WINDOW.attributes('-topmost', 1)

    def setup_menubar(self):
        # MENUBAR
        self.menubar = tk.Menu(self.WINDOW, bd=0)

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
        self.help_menubar_menu = tk.Menu(self.menubar,tearoff=False)
        self.help_menubar_menu.add_command(label="Documentation", command=self.open_online_documentation)
        self.help_menubar_menu.add_command(label="About", command=self.create_about)


        self.menubar.add_cascade(label="File", menu=self.file_menubar)
        self.menubar.add_cascade(label="View", menu=self.view_menubar)
        self.menubar.add_cascade(label="Help", menu=self.help_menubar_menu)

        self.WINDOW.config(menu=self.menubar)

    def setup_main_interface(self):
        # Title
        self.label = ctk.CTkLabel(
            master=self.WINDOW,
            font=(None, 12),
            text="Choose a file so that the program counts the most common words"
        )
        self.label.configure(
            width=ctk.CTkFont().measure("Choose a file so that the program counts the most common words") + 41,
        )
        self.label.place(anchor=tk.N, relx=.5, rely=.0)

        # Button
        self.button = ctk.CTkButton(
            master=self.WINDOW,
            text="Open File...",
            command=self.count_words,
            height=60
        )
        self.button.place(anchor=tk.N, relx=.5, rely=.1)

        # Dataframe Frame
        self.table_frame = ctk.CTkFrame(
            master=self.WINDOW,
            width=500,
            height=300
        )
        self.table_frame.place(anchor=tk.N, relx=.5, rely=.25)

        # Theme Switch
        self.switch = ctk.CTkSwitch(
            self.WINDOW,
            command=self.toggle_themes,
            text='Dark',
            switch_width=50,
            switch_height=25
        )
        self.switch.place(anchor=tk.N, relx=.16, rely=.82)

        # RegEx Entry button
        self.regex_button = ctk.CTkButton(
            master=self.WINDOW,
            text="RegEx...",
            command=self.create_regex_entry,
            height=30
        )
        self.regex_button.place(anchor=tk.W, relx=0.3, rely=0.84)

    # Renders DataFrame Table
    def render_table(self):
        try:
            self.data
        except AttributeError:
            return

        self.table = pdt.Table(
            parent=self.table_frame,
            dataframe=self.data,
            cellbackgr='#111111',
            textcolor='white',
            rowselectedcolor='black',
            editable=False,
            cellwidth=200,
            rowheight=25,
            width=420,
            height=250,
        )
        self.table.boxoutlinecolor='grey'
        self.table.grid_color = 'grey'
        self.table.hideRowHeader()
        self.table.show()

        self.table.rowheader.bgcolor = '#111111'
        self.table.rowheader.textcolor = 'white'
        self.table.colheader.bgcolor = '#111111'
        self.table.colheader.textcolor = 'white'

        if not ctk.AppearanceModeTracker.get_mode():
            self.table.textcolor = 'black'
            self.table.cellbackgr = 'lightgray',
            self.table.rowheader.bgcolor = 'lightgray'
            self.table.rowheader.textcolor = 'black'
            self.table.colheader.bgcolor = 'lightgray'
            self.table.colheader.textcolor = 'black'
            self.table.rowselectedcolor='white',

    # Redirects to online doc page.
    def open_online_documentation(self):
        webbrowser.open("https://github.com/Hoklifter/VerbosityMeter/tree/main/docs/user_guide.md")

    # Create the about window
    def create_about(self):
        self.about_window = ctk.CTkToplevel(master=self.WINDOW)
        self.about_window.transient(self.WINDOW)
        self.about_window.title("About")
        self.about_window.geometry("500x300")
        self.about_window.resizable(False, False)

        self.about_img = ctk.CTkLabel(
            self.about_window,
            image=ctk.CTkImage(PIL.Image.open("../assets/icons/icon2048x2048.png"), None, (150, 150)),
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

        self.about_version = ctk.CTkLabel(self.about_window, text="1.0.0")
        self.about_version.pack()

        self.about_desc = ctk.CTkLabel(
            self.about_window,
            text="""Verbosity Meter simplifies the analysis of word frequencies
in text files through an intuitive Tkinter interface."""
        )
        self.about_desc.pack()

    # Notfications to the user
    def push_notification(self, pop_type : "error | info | success", message : str): # type: ignore
        self.notification.destroy()
        colors = {
            "error": "#cc0000",
            "info": "#1e92f4",
            "success": "#00cc00",
        }

        self.notification = ctk.CTkLabel(master=self.WINDOW)

        self.notification.configure(
            text=f"{pop_type.capitalize()}: {message}",
            font=(None, 18),
            fg_color=colors[pop_type],
            text_color='white',
            width=400,
            height=20,
            corner_radius=20
        )

        self.notification_y = 0

        # Go Down
        while self.notification_y < 50:
            self.notification_y += 4
            self.notification.place(y=self.notification_y, relx=.5, anchor=tk.S)
            self.WINDOW.update()
            time.sleep(1/60)

        time.sleep(2)

        # Go Up
        while self.notification_y > 0:
            self.notification_y -= 4
            self.notification.place(y=self.notification_y, relx=.5, anchor=tk.S)
            self.WINDOW.update()
            time.sleep(1/60)

        self.notification.destroy()

    # Change program theme to Dark
    def dark_theme(self):
        ctk.set_appearance_mode("dark")

        menubar_elements = [
            self.menubar,
            self.file_menubar,
            self.view_menubar,
            self.view_theme_menubar,
            self.help_menubar_menu,
        ]

        for element in menubar_elements:
            element.configure(bg="black", fg="white")

        self.render_table()

    # Change program theme to Light
    def light_theme(self):
        ctk.set_appearance_mode("light")

        menubar_elements = [
            self.menubar,
            self.file_menubar,
            self.view_menubar,
            self.view_theme_menubar,
            self.help_menubar_menu,
        ]

        for element in menubar_elements:
            element.configure(bg="white", fg="black")

        self.render_table()

    # Hide/Show Menubar
    def toggle_menubar(self, *args):
        if self.menubar.winfo_exists():
            self.menubar.destroy()
        else:
            self.setup_menubar()

        if ctk.AppearanceModeTracker.appearance_mode:
            self.dark_theme()
        else:
            self.light_theme()

    # Light becomes Dark; Dark becomes Light
    def toggle_themes(self):
        if ctk.AppearanceModeTracker.appearance_mode:
            self.light_theme()
            self.switch.configure(text='Light')
        else:
            self.dark_theme()
            self.switch.configure(text='Dark')

    # Changes the search pattern to set table data.
    def create_regex_entry(self):
        self.regex_entry = ctk.CTkEntry(master=self.WINDOW)
        self.regex_entry.place(anchor=tk.W, relx=0.54, rely=0.84)
        self.regex_set = ctk.CTkButton(
            master=self.WINDOW,
            text='Set',
            command=self.change_regex,
            width=10
        )
        self.regex_set.place(anchor=tk.W, relx=0.779, rely=0.84)
