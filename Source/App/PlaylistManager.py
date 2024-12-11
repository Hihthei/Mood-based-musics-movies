import customtkinter as ctk
import random


class Playlist(ctk.CTkFrame):  # Conversion en CTkFrame
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Cry in my SQL - Playlist Manager", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=3, pady=20)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # self.__load_playlist()
        # self.__load_real_data()
        self.__grid_config()

        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)

        back_button = ctk.CTkButton(
            button_frame, text="Back", command=lambda: controller.show_frame("MainPage")
        )
        back_button.grid(row=0, column=0, padx=5)

        disconnect_button = ctk.CTkButton(
            button_frame, text="Disconnect", command=lambda: controller.show_frame("FirstPage")
        )
        disconnect_button.grid(row=0, column=1, padx=5)

        quit_button = ctk.CTkButton(button_frame, text="Quit", command=controller.destroy)
        quit_button.grid(row=0, column=2, padx=5)

    def __load_playlist(self):
        try:
            __playlist = self.controller.DBCommunicate.show_Playlist(self.controller.userID)
            self.__playlist = []
            for playlist in __playlist:
                self.__playlist.append(playlist)

            print(self.__playlist)

        except Exception as e:
            print(e)
            self.__playlist = []

    def __load_data(self):
        try:
            self.__data = self.controller.DBCommunicate.show_Playlist_Content(self.controller.userID, self.__playlist[0])
            if self.__data is None:
                self.__data = []

        except Exception as e:
            self.__data = []

    def __load_real_data(self):
        try:
            self.__data = self.controller.DBCommunicate.show_Content()

            if self.__data is None:
                self.__data = []

        except Exception as e:
            self.__data = []

    def __grid_config(self):
        frames = ctk.CTkFrame(self)
        frames.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        frames.grid_rowconfigure(0, weight=1)
        frames.grid_columnconfigure(0, weight=1)

        self.__tree = ctk.CTkScrollableFrame(frames, width=600, height=300)
        self.__tree.grid(row=0, column=0, sticky="nsew")

        self.__load_real_data()

        for i, (title, author,  isMusic, moodName) in enumerate(self.__data):
            ctk.CTkLabel(self.__tree, text=title).grid(row=i, column=0, padx=5, pady=5)
            ctk.CTkLabel(self.__tree, text=author).grid(row=i, column=1, padx=5, pady=5)
            ctk.CTkLabel(self.__tree, text="Music" if isMusic else "Movie").grid(row=i, column=2, padx=5, pady=5)
            ctk.CTkLabel(self.__tree, text=moodName).grid(row=i, column=3, padx=5, pady=5)

        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=1, column=2, padx=10, pady=10, sticky="ns")

        remove_button = ctk.CTkButton(button_frame, text="Remove from playlist", command=lambda: self.__pass)
        remove_button.pack(pady=5)

        self.search_entry = ctk.CTkEntry(button_frame, width=200, font=("Arial", 14))
        self.search_entry.pack(pady=5, anchor="center")

        search = ctk.CTkButton(button_frame, text="Search", command=lambda: self.__pass())
        search.pack(pady=5)

    def __pass(self):
        pass