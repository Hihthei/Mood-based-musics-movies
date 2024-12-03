import tkinter as tk
from tkinter import ttk

import random


class Playlist(tk.Frame):
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

        back_button = tk.Button(button_frame, text="Back", command=lambda: controller.show_frame("MainPage"))
        back_button.grid(row=0, column=1, padx=5)

        disconnect = tk.Button(button_frame, text="Disconnect", command=lambda: controller.show_frame("FirstPage"))
        disconnect.grid(row=0, column=2, padx=5)

        quit_button = tk.Button(button_frame, text="Quit", command=controller.destroy)
        quit_button.grid(row=0, column=3, padx=5)

    def __grid_config(self):
        pass


    def __search(self):
        pass


    def __shuffle(self):
        pass
