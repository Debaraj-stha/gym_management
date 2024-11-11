import tkinter as tk
from tkinter import OptionMenu, ttk


from utils.widgets import createButton, createLabel
from .setting_view import SettingView
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from tkinter import Scrollbar


class Dashboard(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.create_ui()

    def create_ui(self):
        # Configure the main layout into two frames: left (graph) and right (buttons)
        self.grid_columnconfigure(0, weight=1)  # Left side (graph) with equal weight
        self.grid_columnconfigure(1, weight=1)  # Right side (buttons) with equal weight
        self.grid_rowconfigure(0, weight=1)  # Expand both vertically

        # Left frame for the graph
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Right frame for the buttons
        right_frame = ttk.Frame(self)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Add scrollbar for the graph on the left frame
        canvas = tk.Canvas(left_frame)
        scrollbar = Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Label
        createLabel(scrollable_frame, text=_("Active member on"), fontsize=16).grid(
            row=0, column=0, columnspan=2
        )

        # OptionMenus for month and year, placed closer together using padx
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        row_frame = tk.Frame(scrollable_frame)
        row_frame.grid(row=1, column=1, pady=(5, 0), sticky="nsew")
        month_var = tk.StringVar()
        month_var.set("Jan")  # default value
        month_menu = OptionMenu(row_frame, month_var, *months)
        month_menu.grid(
            row=1, column=0, padx=(0, 5)
        )  # Added small padx for space between month and year

        years = ["2020", "2021", "2022", "2023", "2024"]
        year_var = tk.StringVar()
        year_var.set(years[0])  # default value
        year_menu = OptionMenu(row_frame, year_var, *years)
        year_menu.grid(
            row=1, column=1, padx=(5, 0)
        )  # Small padx on the left to bring year closer to month

        # Add graph to the scrollable frame
        x = ["jan", "feb", "mar"]
        y = [100, 500, 400]
        fig = plt.figure(figsize=(10, 6))
        bar = plt.bar(x, y)
        canvas_graph = FigureCanvasTkAgg(fig, master=scrollable_frame)
        canvas_graph.get_tk_widget().grid(row=2, column=0, columnspan=2, pady=10)
        # Label
        createLabel(scrollable_frame, text=_("Member left on"), fontsize=16).grid(
            row=3, column=0, columnspan=2
        )

        # OptionMenus for month and year, placed closer together using padx

        row_frame = tk.Frame(scrollable_frame)
        row_frame.grid(row=4, column=1, pady=(5, 0), sticky="nsew")
        month_var = tk.StringVar()
        month_var.set("Jan")  # default value
        month_menu = OptionMenu(row_frame, month_var, *months)
        month_menu.grid(
            row=1, column=0, padx=(0, 5)
        )  # Added small padx for space between month and year

        year_var = tk.StringVar()
        year_var.set(years[0])  # default value
        year_menu = OptionMenu(row_frame, year_var, *years)
        year_menu.grid(
            row=1, column=1, padx=(5, 0)
        )  # Small padx on the left to bring year closer to month

        # Add graph to the scrollable frame
        x = ["jan", "feb", "mar"]
        y = [100, 500, 400]
        fig = plt.figure(figsize=(10, 6))
        bar = plt.bar(x, y)
        canvas_graph = FigureCanvasTkAgg(fig, master=scrollable_frame)
        canvas_graph.get_tk_widget().grid(row=5, column=0, columnspan=2, pady=10)

        # Add buttons to the right frame
        button1 = createButton(
            right_frame,
            text=_("Members"),
            command=lambda: self.controller.show_frame("MembersView"),
            width=20,
            height=3,
        )
        button1.pack(pady=10)

        button2 = createButton(
            right_frame,
            text=_("Attendance"),
            command=lambda: self.controller.show_frame("AttendanceView"),
            width=20,
            height=3,
        )
        button2.pack(pady=10)

        button3 = createButton(
            right_frame,
            text=_("Billing"),
            command=lambda: self.controller.show_frame("BillingView"),
            width=20,
            height=3,
        )
        button3.pack(pady=10)

        button4 = createButton(
            right_frame,
            text=_("Class Schedule"),
            command=lambda: self.controller.show_frame("ClassScheduleView"),
            width=20,
            height=3,
        )
        button4.pack(pady=10)
        button5 = createButton(
            right_frame,
            text=_("Instructors"),
            command=lambda: self.controller.show_frame("InstructorView"),
            width=20,
            height=3,
        )
        button5.pack(pady=10)

        button6 = createButton(
            right_frame,
            text=_("Setting"),
            command=lambda: SettingView(parent=self.controller),
            width=20,
            height=3,
        )
        button6.pack(pady=10)
