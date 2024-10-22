import tkinter as tk


class BillingView(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
