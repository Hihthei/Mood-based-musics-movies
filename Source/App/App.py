import customtkinter as ctk

from Source.App.FirstPage import FirstPage
from Source.App.NewUser import NewUser
from Source.App.Connect import Connect
from Source.App.MainPage import MainPage
from Source.App.PlaylistManager import Playlist


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cry in my SQL")
        self.geometry("800x600")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.pages = (
            FirstPage,
            NewUser,
            Connect,
            MainPage,
            Playlist
        )

        for Page in self.pages:
            page_name = Page.__name__
            frame = Page(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("FirstPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


app = App()
app.mainloop()
