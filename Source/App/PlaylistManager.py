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

        self.__data = self.__load_data()
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

    def __load_data(self):
        return []

    def __grid_config(self):
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        for i, (name, description) in enumerate(self.__data):
            ctk.CTkLabel(table_frame, text=name).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(table_frame, text=description).grid(row=i, column=1, padx=10, pady=5, sticky="w")
