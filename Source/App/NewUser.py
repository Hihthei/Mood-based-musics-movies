import tkinter as tk
from tkinter import messagebox

from Source.Security.DBCommunicate import DBCommunicate
from Source.Security.HashPswd import hash_pswd, verify_pswd


class NewUser(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="New User", font=("Arial", 16))
        label.pack(pady=20, anchor="center")

        username_label = tk.Label(self, text="Username:", font=("Arial", 16))
        username_label.pack(pady=5, anchor="center")

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5, anchor="center")

        password_label = tk.Label(self, text="Password:", font=("Arial", 16))
        password_label.pack(pady=5, anchor="center")

        self.password_entry = tk.Entry(self, show="*", font=("Arial", 16))
        self.password_entry.pack(pady=5, anchor="center")

        confirm_password_label = tk.Label(self, text="Confirm password::", font=("Arial", 16))
        confirm_password_label.pack(pady=5, anchor="center")

        self.confirm_password_entry = tk.Entry(self, show="*", font=("Arial", 16))
        self.confirm_password_entry.pack(pady=5, anchor="center")

        register_button = tk.Button(
            self, text="Register", command=lambda: self.submit_new_user()
        )
        register_button.pack(pady=5, anchor="center")

        back_button = tk.Button(
            self, text="Back", command=lambda: controller.show_frame("FirstPage")
        )
        back_button.pack(pady=30)

        self.DBCommunicate = DBCommunicate()
        self.hassed_pswd = {}

    def __load_hashed_pswd(self):
        self.hassed_pswd = self.DBCommunicate.load_hashed_pswd()

    def __save_hashed_pswd(self):
        try:
            self.DBCommunicate.save_hashed_pswd(self.hassed_pswd.copy())

            messagebox.showinfo("Success", "Successfully registered!")

            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
            self.confirm_password_entry.delete(0, "end")

            self.controller.show_frame("FirstPage")

        except Exception as e:
            messagebox.showerror("Error", f"Could not save user: {e}")

    def submit_new_user(self):
        self.__load_hashed_pswd()

        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields must be filled!")
            return

        if username in self.hassed_pswd:
            messagebox.showerror("Error", "Username already exists")
            return

        password = hash_pswd(password)

        if not verify_pswd(confirm_password, password):
            messagebox.showerror("Error", "Passwords do not match")
            return

        self.hassed_pswd[username] = password

        self.__save_hashed_pswd()
