import tkinter as tk
from tkinter import ttk

import random


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Cry in my SQL", font=("Arial", 16))
        label.grid(row=0, column=0, columnspan=2, pady=20)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.__grid_config()

        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        disconnect = tk.Button(button_frame, text="Disconnect", command=lambda: controller.show_frame("FirstPage"))
        disconnect.grid(row=0, column=2, padx=5)

        quit_button = tk.Button(button_frame, text="Quit", command=controller.destroy)
        quit_button.grid(row=0, column=3, padx=5)

    def __grid_config(self):
        frames = tk.Frame(self)
        frames.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        frames.grid_rowconfigure(0, weight=1)
        frames.grid_columnconfigure(0, weight=1)

        self.__tree = ttk.Treeview(frames, columns=("Title", "Type", "Mood"), show="headings")
        self.__tree.heading("Title", text="Name")
        self.__tree.heading("Type", text="Type")
        self.__tree.heading("Mood", text="Mood")

        for column, width in zip(self.__tree["columns"], [150, 100, 100]):
            self.__tree.column(column, width=width)

        scrollbar = ttk.Scrollbar(frames, orient="vertical", command=self.__tree.yview)
        self.__tree.configure(yscroll=scrollbar.set)

        self.__tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=2, padx=10, pady=10, sticky="ns")

        playlist_button = tk.Button(button_frame, text="Playlist manager", command=lambda: self.controller.show_frame("Playlist"))
        playlist_button.pack(pady=5)

        search = tk.Button(button_frame, text="Search", command=lambda: self.__search())
        search.pack(pady=5)

        shuffle = tk.Button(button_frame, text="Shuffle", command=lambda: self.__shuffle())
        shuffle.pack(pady=5)


    def __search(self):
        pass

    def __shuffle(self):
        data = [self.__tree.item(row)["values"] for row in self.__tree.get_children()]

        random.shuffle(data)
        self.__tree.delete(*self.__tree.get_children())

        for item in data:
            self.__tree.insert("", "end", values=item)
