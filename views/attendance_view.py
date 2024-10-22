import tkinter as tk


class AttendanceView(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        # self.create_ui()
