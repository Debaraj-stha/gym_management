import tkinter as tk

from utils.widgets import createButton
from .setting_view import SettingView


class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_ui()

    def create_ui(self):
        # Configure grid layout to center everything
        self.grid_rowconfigure(0, weight=1)  # Empty row at top
        self.grid_rowconfigure(1, weight=1)  # Row for the label
        self.grid_rowconfigure(2, weight=1)  # Row for the buttons
        self.grid_rowconfigure(3, weight=1)  # Row for the buttons
        self.grid_rowconfigure(4, weight=1)  # Empty row at bottom
        self.grid_rowconfigure(5, weight=1)  # Empty row at bottom

        self.grid_columnconfigure(0, weight=1)  # Empty column at left
        self.grid_columnconfigure(1, weight=1)  # Column for buttons
        self.grid_columnconfigure(2, weight=1)  # Empty column at right

        # Title label
        label = tk.Label(self, text="Gym Management", font=("Arial", 24, "bold"))
        label.grid(
            row=1, column=1, sticky="nsew", pady=(20, 10)
        )  # Vertical padding to space out

        # Buttons styled as "cards" with larger width and height
        button1 = createButton(
            self,
            text="Members",
            command=lambda: self.controller.show_frame("MembersView"),
            width=20,
            height=3,  # Adjusting size to look like a card
        )
        button1.grid(row=2, column=1, sticky="nsew", padx=20, pady=10)

        button2 = createButton(
            self,
            text="Attendance",
            command=lambda: self.controller.show_frame("AttendanceView"),
            width=20,
            height=3,
        )
        button2.grid(row=3, column=1, sticky="nsew", padx=20, pady=10)

        button3 = createButton(
            self,
            text="Billing",
            command=lambda: self.controller.show_frame("BillingView"),
            width=20,
            height=3,
        )
        button3.grid(row=4, column=1, sticky="nsew", padx=20, pady=10)

        button4 = createButton(
            self,
            text="Class Schedule",
            command=lambda: self.controller.show_frame("ClassScheduleView"),
            width=20,
            height=3,
        )
        button4.grid(row=5, column=1, sticky="nsew", padx=20, pady=10)
        button5 = createButton(
            self,
            text="Setting",
            command=lambda: SettingView(parent=self.controller),
            width=20,
            height=3,
        )
        button5.grid(row=6, column=1, sticky="nsew", padx=20, pady=10)

        # Expand the layout vertically and horizontally
        self.grid_rowconfigure(6, weight=1)  # Empty row at bottom
        self.grid_columnconfigure(
            1, weight=1
        )  # Make sure buttons are centered in the middle
