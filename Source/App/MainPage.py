import tkinter as tk


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Cry in my SQL", font=("Arial", 16))
        label.pack(pady=30, anchor="center")

        disconnect = tk.Button(
            self, text="Disconnect", command=lambda: controller.show_frame("FirstPage")
        )
        disconnect.pack(pady=30)

        quit_button = tk.Button(self, text="Quit", command=controller.destroy)
        quit_button.pack(pady=30)
