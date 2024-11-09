import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv
import os


from files.database_schemas import (
    ATTENDANCE_SCHEMA,
    CLASS_SCHEDULE_INSTRUCTOR_SCHEMA,
    CLASS_SCHEDULE_SCHEMA,
    CUSTOMER_SCHEMA,
    INSTRUCTOR_SCHEMA,
)
from utils.constraints import TABLENAME
from utils.environment_file import get_env, set_env
from views.dashboard import Dashboard
from views.instructor_view import InstructorView
from views.member_view import MembersView
from views.attendance_view import AttendanceView
from views.billing_view import BillingView
from views.class_schedule_view import ClassScheduleView

from utils.logger import logger
from utils.database import Database


class GymManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.db.create_table(TABLENAME.ATTENDANCE.value, ATTENDANCE_SCHEMA)
        self.db.create_table(TABLENAME.CUSTOMERS.value, CUSTOMER_SCHEMA)
        self.db.create_table(TABLENAME.INSTRUCTORS.value, INSTRUCTOR_SCHEMA)
        self.db.create_table(TABLENAME.CLASS_SCHEDULE.value, CLASS_SCHEDULE_SCHEMA)
        self.db.create_table(
            TABLENAME.CLASS_SCHEDULE_INSTRUCTORS.value, CLASS_SCHEDULE_INSTRUCTOR_SCHEMA
        )
        logger.debug("Initializing software")
        # loading environment file
        load_dotenv()
        # App configuration
        self.title("Gym Management Software")
        self.geometry("800x800")
        self.resizable(False, True)
        self.style = ttk.Style()

        self.theme = get_env("THEME")

        if self.theme is None:
            theme_path = os.path.join(os.getcwd(), "theme/forest-dark.tcl")
            set_env(
                "THEME", "forest-dark"
            )  # setting default theme to environment variable if not set theme
        else:
            theme_path = os.path.join(os.getcwd(), f"theme/{self.theme}.tcl")
        self.tk.call("source", theme_path)
        self.style.theme_use(self.theme)
        self.style.configure("Treeview", font="20")
        self.style.configure(
            "Treeview.Heading",
            foreground="#111",
            font="40",
        )

        bg_key = "BACKGROUND_COLOR"
        bg = get_env(bg_key)
        if bg is None:
            set_env(
                bg_key, "#d4d4d4"
            )  # setting default backgroud color to environment variable if not set background color

        # Create a container for the main content
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Configure row/column to expand
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Store all frames (views)
        self.frames = {}

        # Initialize different views and add them to frames
        for F in (
            Dashboard,
            MembersView,
            AttendanceView,
            BillingView,
            ClassScheduleView,
            InstructorView,
        ):
            page_name = F.__name__
            frame = F(parent=container, controller=self, db=self.db)
            self.frames[page_name] = frame

            # Put all frames in the same location
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the dashboard by default
        self.show_frame("Dashboard")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()  # Bring the frame to the top

    def update_theme(self, theme):
        """Switch the application's theme."""

        # Load the new theme if not already loaded
        theme_path = os.path.join(os.getcwd(), f"theme/{theme}.tcl")
        if theme not in self.style.theme_names():

            self.tk.call("source", theme_path)

        # Apply the new theme
        self.style.theme_use(theme)

        # Update the environment variable for theme
        self.theme = theme
        set_env("THEME", theme)

        # Refresh UI by updating all widgets

        # Ensure the UI is updated immediately
        self.update_idletasks()

    def _refresh_widgets(self):
        """Force refresh of the entire UI to reapply styles."""
        # Iterate through all widgets and reconfigure their styles
        for widget in self.winfo_children():
            self._reconfigure_widget(widget)

        self.update_idletasks()

    def _reconfigure_widget(self, widget):
        """Reconfigure widget and its children."""
        # For each widget, check if it has children and reconfigure them
        if isinstance(widget, ttk.Widget):  # Only refresh ttk widgets for theme change
            widget.update_idletasks()

        # Recursively reconfigure child widgets
        if isinstance(widget, tk.Widget):
            for child in widget.winfo_children():
                self._reconfigure_widget(child)

    def on_closing(self):
        self.db.close()


if __name__ == "__main__":
    app = GymManagementApp()

    app.mainloop()
    app.on_closing()
