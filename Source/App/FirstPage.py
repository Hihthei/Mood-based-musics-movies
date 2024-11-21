import tkinter as tk


class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Cry in my SQL", font=("Arial", 16))
        label.pack(pady=30, anchor="center")

        new_user_button = tk.Button(
            self, text="New User", command=lambda: controller.show_frame("NewUser")
        )
        new_user_button.pack(pady=30)

        connect = tk.Button(
            self, text="Connect", command=lambda: controller.show_frame("Connect")
        )
        connect.pack(pady=30)

        quit_button = tk.Button(self, text="Quit", command=controller.destroy)
        quit_button.pack(pady=30)
