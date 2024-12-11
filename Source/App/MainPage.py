import customtkinter as ctk

from Source.App.PlaylistManager import Playlist

from Source.Database.DBCommunicate import DBCommunicateError
from tkinter import messagebox


class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.__label = ctk.CTkLabel(self, text="Cry in my SQL", font=("Arial", 24))
        self.__label.grid(row=0, column=0, columnspan=3, pady=20)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.__data = {}
        self.__grid_config()

        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)

        disconnect = ctk.CTkButton(button_frame, text="Disconnect", command=lambda: controller.show_frame("FirstPage"))
        disconnect.grid(row=0, column=2, padx=5)

        quit_button = ctk.CTkButton(button_frame, text="Quit", command=controller.destroy)
        quit_button.grid(row=0, column=3, padx=5)

    def __grid_config(self):
        frames = ctk.CTkFrame(self)
        frames.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        frames.grid_rowconfigure(0, weight=1)
        frames.grid_columnconfigure(0, weight=1)

        self.__tree = ctk.CTkScrollableFrame(frames, width=600, height=300)
        self.__tree.grid(row=0, column=0, sticky="nsew")

        self.__load_data()
        self.__update_tree()

        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=1, column=2, padx=10, pady=10, sticky="ns")

        change_mood = ctk.CTkButton(button_frame, text="Change_Mood", command=lambda: self.__change_mood())
        change_mood.pack(pady=5)
        self.new_mood = ctk.CTkEntry(button_frame, width=200, font=("Arial", 14))
        self.new_mood.pack(pady=5, anchor="center")

        search = ctk.CTkButton(button_frame, text="Search", command=lambda: self.__search())
        search.pack(pady=5)
        self.search_entry = ctk.CTkEntry(button_frame, width=200, font=("Arial", 14))
        self.search_entry.pack(pady=5, anchor="center")

        mood = ctk.CTkButton(button_frame, text="Mood_Generate", command=lambda: self.__mood())
        mood.pack(pady=5)
        self.mood_entry = ctk.CTkEntry(button_frame, width=200, font=("Arial", 14))
        self.mood_entry.pack(pady=5, anchor="center")

        playlist_button = ctk.CTkButton(button_frame, text="Playlist manager", command=lambda: self.controller.show_frame("Playlist"))
        playlist_button.pack(pady=5)

    def __load_data(self):
        try:
            self.__data = self.controller.DBCommunicate.show_Content()

            if self.__data is None:
                self.__data = []

        except Exception as e:
            self.__data = []

    def __playlist_manager(self):
        pass

    def __update_tree(self):
        for widget in self.__tree.winfo_children():
            widget.destroy()

        for i, (title, author, isMusic, moodName) in enumerate(self.__data):
            ctk.CTkLabel(self.__tree, text=title).grid(row=i, column=0, padx=5, pady=5)
            ctk.CTkLabel(self.__tree, text=author).grid(row=i, column=1, padx=5, pady=5)
            ctk.CTkLabel(self.__tree, text="Music" if isMusic else "Movie").grid(row=i, column=2, padx=5, pady=5)
            ctk.CTkLabel(self.__tree, text=moodName).grid(row=i, column=3, padx=5, pady=5)


    def __search(self):
        try:
            self.__data = self.controller.DBCommunicate.show_Content(title=self.search_entry.get())
            self.__update_tree()
        except DBCommunicateError as e:
            self.__data = []


    def __mood(self):
        try:
            self.__data = self.controller.DBCommunicate.show_Content_Mood(self.controller.userID, self.mood_entry.get())
            self.__update_tree()
        except DBCommunicateError as e:
            self.__data = []

    def __change_mood(self):
        try:
            self.controller.DBCommunicate.change_UserMood(self.controller.userID, self.new_mood.get())
            messagebox.showinfo("Mood Changed", "New Mood : " + self.new_mood.get())
        except DBCommunicateError as e:
            raise e