import tkinter as tk
from datetime import datetime
from tkinter.ttk import Checkbutton, Frame
from utils.widgets import (
    backButton,
    create_buttons,
    create_page_numbers,
    createLabel,
    createButton,
)


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

        toolrow.grid_columnconfigure(0, weight=1)
        toolrow.grid_columnconfigure(1, weight=1)
        toolrow.grid_columnconfigure(2, weight=1)
        toolrow.grid_columnconfigure(3, weight=1)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        backButton(self, self.controller)
        today = datetime.today()
        createLabel(toolrow, f'Today:{today.strftime("%Y-%m-%d")}').grid(
            row=1, column=1, columnspan=3, sticky="ew"
        )
        self.customers_frame = Frame(self)
        self.customers_frame.grid(row=2, column=1, sticky="nsew")
        self._config_gridcolumn(self.customers_frame)
        createLabel(self.customers_frame, "Name:").grid(row=1, column=1, sticky="nsew")
        createLabel(self.customers_frame, "Check in:").grid(
            row=1, column=2, sticky="nsew"
        )
        createLabel(self.customers_frame, "Check out:").grid(
            row=1, column=3, sticky="nsew"
        )

        self._display_customers()
        self.row_frame = tk.Frame(self)
        self.row_frame.grid(row=4, column=3, sticky="nsew", pady=20)

        self.sub_row, self.total_buttons, self.prev_button, self.next_button = (
            create_page_numbers(
                self.total_records, self.row_frame, self.change_page, limit=self.limit
            )
        )

    def change_page(self, page):
        self.current_page = page
        self.offset = (page - 1) * self.limit

        self.sub_row.destroy()
        print(self.current_page)
        self._update_page_button_state()
        create_buttons(
            self.row_frame, self.current_page, self.total_buttons, self.change_page
        )
        self._paginate()
        self._update_table()

    def _update_table(self):

        for widget in self.customers_row.winfo_children():
            widget.destroy()

        self._display_customers()

    def _update_page_button_state(self):
        if self.current_page != 1:
            self.has_prev = True
        else:
            self.has_prev = False
        if self.current_page < self.total_buttons:
            self.has_next = True
        else:
            self.has_next = False

        if self.total_buttons > 9:
            self.show_dots = True

        self.prev_button_state = "disabled" if not self.has_prev else "active"

        self.next_button_state = "disabled" if not self.has_next else "active"
        self.prev_button.config(state=self.prev_button_state)
        self.next_button.config(state=self.next_button_state)

    def _config_gridcolumn(self, frame):
        for i in range(4):
            frame.columnconfigure(i, weight=1)

    def _display_customers(self):
        if self.customers:
            self.customers_row = Frame(self.customers_frame)
            self.customers_row.grid(
                row=2, column=1, columnspan=3, sticky="nsew", pady=10
            )
            self._config_gridcolumn(self.customers_row)
            for i, customer in enumerate(self.customers):

                createLabel(self.customers_row, f"{customer[i]}").grid(
                    row=i, column=1, sticky="nsew", pady=10
                )

                checkin_var = tk.BooleanVar(self.customers_row)
                checkin_box = Checkbutton(self.customers_row, variable=checkin_var)
                checkin_box.grid(row=i, column=2, sticky="nsew", pady=10)

                checkout_var = tk.BooleanVar(self.customers_row)
                checkout_box = Checkbutton(self.customers_row, variable=checkout_var)
                checkout_box.grid(row=i, column=3, sticky="nsew", pady=10)

        else:
            createLabel(self, "No customers found").grid(
                row=2, column=1, columnspan=3, sticky="ew"
            )
