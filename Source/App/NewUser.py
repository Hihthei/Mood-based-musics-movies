import customtkinter as ctk
from tkinter import messagebox

from Source.Database.DBCommunicate import DBCommunicate
from Source.Security.HashPswd import hash_pswd, verify_pswd


class NewUser(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="New User", font=("Arial", 24))
        label.pack(pady=20, anchor="center")

        username_label = ctk.CTkLabel(self, text="Username:", font=("Arial", 16))
        username_label.pack(pady=5, anchor="center")

        self.username_entry = ctk.CTkEntry(self, width=200, font=("Arial", 14))
        self.username_entry.pack(pady=5, anchor="center")

        password_label = ctk.CTkLabel(self, text="Password:", font=("Arial", 16))
        password_label.pack(pady=5, anchor="center")

        self.password_entry = ctk.CTkEntry(self, width=200, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5, anchor="center")

        confirm_password_label = ctk.CTkLabel(self, text="Confirm Password:", font=("Arial", 16))
        confirm_password_label.pack(pady=5, anchor="center")

        self.confirm_password_entry = ctk.CTkEntry(self, width=200, show="*", font=("Arial", 14))
        self.confirm_password_entry.pack(pady=5, anchor="center")

        register_button = ctk.CTkButton(
            self, text="Register", command=self.submit_new_user, width=150
        )
        register_button.pack(pady=10, anchor="center")

        back_button = ctk.CTkButton(
            self, text="Back", command=lambda: controller.show_frame("FirstPage"), width=150
        )
        back_button.pack(pady=30, anchor="center")

        self.DBCommunicate = DBCommunicate("root", "!Cd2@5Cprb")

    def __save_new_user(self, username:str, hashpassword:str):
        try:
            self.DBCommunicate.add_User(username, hashpassword)

            messagebox.showinfo("Success", "Successfully registered!")

            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
            self.confirm_password_entry.delete(0, "end")

            self.controller.show_frame("FirstPage")
        except Exception as e:
            messagebox.showerror("Error", f"Username already exists :{e}")

    def submit_new_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields must be filled!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        hashed_password = hash_pswd(password)
        self.__save_new_user(username, hashed_password)