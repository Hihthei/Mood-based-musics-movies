import customtkinter as ctk
from tkinter import messagebox

from Source.Security.DBCommunicate import DBCommunicate
from Source.Security.HashPswd import verify_pswd


class Connect(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Login Interface", font=("Arial", 24))
        label.pack(pady=30, anchor="center")

        username_label = ctk.CTkLabel(self, text="Username:", font=("Arial", 16))
        username_label.pack(pady=5, anchor="center")

        self.username_entry = ctk.CTkEntry(self, width=200, font=("Arial", 14))
        self.username_entry.pack(pady=5, anchor="center")

        password_label = ctk.CTkLabel(self, text="Password:", font=("Arial", 16))
        password_label.pack(pady=5, anchor="center")

        self.password_entry = ctk.CTkEntry(self, width=200, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5, anchor="center")

        connect_button = ctk.CTkButton(
            self, text="Connect", command=self.submit_login, width=150
        )
        connect_button.pack(pady=10, anchor="center")

        back_button = ctk.CTkButton(
            self, text="Back", command=lambda: controller.show_frame("FirstPage"), width=150
        )
        back_button.pack(pady=20, anchor="center")

        self.DBCommunicate = DBCommunicate()
        self.__hassed_pswd = {}

    def __load_hashed_pswd(self):
        self.__hassed_pswd = self.DBCommunicate.load_hashed_pswd()

    def submit_login(self):
        self.__load_hashed_pswd()

        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.__hassed_pswd and verify_pswd(password, self.__hassed_pswd[username]):
            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")

            self.controller.show_frame("MainPage")

        else:
            messagebox.showerror("Error", "Username or password incorrect")
