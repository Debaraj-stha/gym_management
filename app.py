import tkinter as tk
from tkinter import ttk
from utils.environment_file import get_env, set_env
from views.dashboard import Dashboard
from views.member_view import MembersView
from views.attendance_view import AttendanceView
from views.billing_view import BillingView
from views.class_schedule_view import ClassScheduleView
from dotenv import load_dotenv
import os


class GymManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
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

        bg_key = "BACKGROUND_COLOR"
        bg = get_env(bg_key)
        if bg is None:
            set_env(
                bg_key, "#d4d4d4"
            )  # setting default backgroud color to environment variable if not set background color

        # Create a container for the main content
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

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
        ):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
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
        print(f"Theme changed to: {theme}")
        print(self.style.theme_names())

        # Load the new theme if not already loaded
        theme_path = os.path.join(os.getcwd(), f"theme/{theme}.tcl")
        if theme not in self.style.theme_names():
            print("Loading theme:", theme)
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


if __name__ == "__main__":
    app = GymManagementApp()
    app.mainloop()
