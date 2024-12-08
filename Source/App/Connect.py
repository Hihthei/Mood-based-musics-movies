import customtkinter as ctk
from tkinter import messagebox

from Source.Database.DBCommunicate import DBCommunicateError, DBCommunicate
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

        self.DBCommunicate = parent.DBCommunicate

    def submit_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            information = self.DBCommunicate.connect_User(username)

            if verify_pswd(password, information[1]):
                _ = information[0]

                self.username_entry.delete(0, "end")
                self.password_entry.delete(0, "end")

                self.controller.show_frame("MainPage")
            else:
                messagebox.showerror("Error", "Password incorrect")

        except DBCommunicateError as e:
            messagebox.showerror("Error", e)
