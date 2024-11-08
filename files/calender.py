from datetime import datetime
from tkcalendar import Calendar
import tkinter as tk


class MyCalendar(tk.Toplevel):
    def __init__(self, callback):
        super().__init__()
        self.title("Pick Date")
        self.geometry("300x200")
        self.callback = callback
        self.create_ui()

    def create_ui(self):
        self.calendar = Calendar(
            self, font="Arial 14", selectmode="day", year=2024, month=1, day=1
        )
        self.calendar.pack(pady=20)
        # binding  event to get date on click
        self.calendar.bind("<<CalendarSelected>>", self.get_selected_date)
        self.calendar.config(background="#161D6F", foreground="#FFFFFF")

        self.grab_set()
        self.focus_set()
        self.wait_window()  # waits for user to select a date and then destroys the window.  # It's a blocking call.

    def get_selected_date(self, event):
        selected_date = self.calendar.get_date()
        date_obj = datetime.strptime(selected_date, "%y/%m/%d")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        self.destroy()
        self.callback(formatted_date)
