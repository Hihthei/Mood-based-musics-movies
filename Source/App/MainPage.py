import customtkinter as ctk
import random
import json


class MainPage(ctk.CTkFrame):  # Conversion en CTkFrame
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
        frames.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        frames.grid_rowconfigure(0, weight=1)
        frames.grid_columnconfigure(0, weight=1)

        self.__tree = ctk.CTkScrollableFrame(frames, width=600, height=300)
        self.__tree.grid(row=0, column=0, sticky="nsew")

        self.__load_data()

        for i, (key, (title, content_type, mood)) in enumerate(self.__data.items()):
            ctk.CTkLabel(self.__tree, text=title).grid(row=i, column=0, padx=5, pady=5)
            ctk.CTkLabel(self.__tree, text=content_type).grid(row=i, column=1, padx=5, pady=5)
            ctk.CTkLabel(self.__tree, text=mood).grid(row=i, column=2, padx=5, pady=5)

        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=1, column=2, padx=10, pady=10, sticky="ns")

        playlist_button = ctk.CTkButton(button_frame, text="Playlist manager", command=lambda: self.controller.show_frame("Playlist"))
        playlist_button.pack(pady=5)

        search = ctk.CTkButton(button_frame, text="Search", command=lambda: self.__search())
        search.pack(pady=5)

        shuffle = ctk.CTkButton(button_frame, text="Shuffle", command=lambda: self.__shuffle())
        shuffle.pack(pady=5)

    def __load_data(self):
        try:
            with open('tmp_songs_base.json', 'r') as file:
                self.__data = json.load(file)
        except FileNotFoundError:
            self.__data = {}

    def __search(self):
        pass

    def __shuffle(self):
        data = [
                (
                    self.__label.grid_info()['row'],[label.cget("text")
                        for label in self.__tree.winfo_children()
                        if label.grid_info()['row'] == row]
            )
            for row in range(len(self.__tree.winfo_children()))
        ]
        random.shuffle(data)

        for i, (row, values) in enumerate(data):
            for col, value in enumerate(values):
                self.__label = [widget for widget in self.__tree.winfo_children() if widget.grid_info()['row'] == row and widget.grid_info()['column'] == col][0]
                self.__label.grid(row=i, column=col)
