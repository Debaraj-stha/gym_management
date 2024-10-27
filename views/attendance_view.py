import tkinter as tk
from datetime import datetime
from tkinter.ttk import Checkbutton
from utils.widgets import backButton, createLabel, createButton


class AttendanceView(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.limit = 1
        self.offset = 0
        self.current_page = 1
        self.total_records = self.db.total_customers()
        self.paginated_members = []
        self.show_dots = False
        self.has_prev = False
        self.has_next = False
        self.total_buttons = None
        self.customers = []
        self._paginate()

        self.create_ui()
        print(self.total_records)

    def _paginate(self):
        end = self.current_page * self.limit
        start = self.offset
        self.customers = self.db.get_customers("name", self.limit, self.offset)

    def create_ui(self):
        toolrow = tk.Frame(self)
        toolrow.grid(row=1, column=1, sticky="ew", pady=(10, 0))
        toolrow.grid_rowconfigure(0, weight=1)
        toolrow.grid_rowconfigure(1, weight=1)
        toolrow.grid_columnconfigure(2, weight=1)
        toolrow.grid_columnconfigure(0, weight=1)
        toolrow.grid_columnconfigure(1, weight=3)
        toolrow.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        backButton(self, self.controller)
        today = datetime.today()
        createLabel(toolrow, f'Today:{today.strftime("%Y-%m-%d")}').grid(
            row=1, column=1, columnspan=3, sticky="ew"
        )
        createLabel(self, "Name:").grid(row=2, column=1, sticky="ew")
        createLabel(self, "Check in:").grid(row=2, column=2, sticky="ew")
        createLabel(self, "Check out:").grid(row=2, column=3, sticky="ew")
        canvas = tk.Canvas(self)
        canvas.grid(row=3, column=1, columnspan=3, sticky="nsew")
        scrollbar = tk.Scrollbar(self, command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=4, sticky="ns")
        self._display_customers()

    def _display_customers(self):
        if self.customers:
            for i, customer in enumerate(self.customers):
                # Display customer name in the correct row and column
                createLabel(self.scrollable_frame, f"{customer[i]}").grid(
                    row=i, column=1, sticky="ew"
                )

                # Check-in checkbox (local variable to avoid overwriting)
                checkin_var = tk.BooleanVar(self.scrollable_frame)
                checkin_box = Checkbutton(self.scrollable_frame, variable=checkin_var)
                checkin_box.grid(row=i, column=2, sticky="ew")

                # Check-out checkbox (local variable to avoid overwriting)
                checkout_var = tk.BooleanVar(self.scrollable_frame)
                checkout_box = Checkbutton(self.scrollable_frame, variable=checkout_var)
                checkout_box.grid(row=i, column=3, sticky="ew")
        else:
            createLabel(self.scrollable_frame, "No customers found").grid(
                row=0, column=1, columnspan=3, sticky="ew"
            )
