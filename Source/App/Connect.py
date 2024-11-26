import tkinter as tk
from tkinter import messagebox

from Source.Security.DBCommunicate import DBCommunicate
from Source.Security.HashPswd import verify_pswd


class Connect(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Login interface", font=("Arial", 16))
        label.pack(pady=30, anchor="center")

        username_label = tk.Label(self, text="Username:", font=("Arial", 16))
        username_label.pack(pady=5, anchor="center")

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5, anchor="center")

        password_label = tk.Label(self, text="Password:", font=("Arial", 16))
        password_label.pack(pady=5, anchor="center")

        self.password_entry = tk.Entry(self, show="*", font=("Arial", 16))
        self.password_entry.pack(pady=5, anchor="center")

        connect_button = tk.Button(
            self, text="Connect", command=lambda: self.submit_login()
        )
        connect_button.pack(pady=5, anchor="center")

        back_button = tk.Button(
            self, text="Back", command=lambda: controller.show_frame("FirstPage")
        )
        back_button.pack(pady=30)

        self.DBCommunicate = DBCommunicate()
        self.hassed_pswd = {}

    def __load_hashed_pswd(self):
        self.hassed_pswd = self.DBCommunicate.load_hashed_pswd()

    def submit_login(self):
        self.__load_hashed_pswd()

        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.hassed_pswd and verify_pswd(password, self.hassed_pswd[username]):
            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")

            self.controller.show_frame("MainPage")
        else:
            messagebox.showerror("Error", "Username or password incorrect")
