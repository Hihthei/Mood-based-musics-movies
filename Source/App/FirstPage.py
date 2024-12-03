import customtkinter as ctk


class FirstPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Cry in my SQL", font=("Arial", 24))
        label.pack(pady=30)

        dark_mode_var = ctk.BooleanVar(value=True)

        dark_mode_switch = ctk.CTkSwitch(
            self,
            text="Dark Mode",
            variable=dark_mode_var,
            command=lambda: controller.set_dark_mode(dark_mode_var.get())
        )
        dark_mode_switch.pack(pady=10)

        new_user_button = ctk.CTkButton(
            self, text="New User", command=lambda: controller.show_frame("NewUser")
        )
        new_user_button.pack(pady=20)

        connect = ctk.CTkButton(
            self, text="Connect", command=lambda: controller.show_frame("Connect")
        )
        connect.pack(pady=20)

        quit_button = ctk.CTkButton(self, text="Quit", command=controller.destroy)
        quit_button.pack(pady=20)
