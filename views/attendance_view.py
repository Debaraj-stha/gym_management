import tkinter as tk
from datetime import datetime
from tkinter.ttk import Checkbutton, Frame
from utils.logger import logger
from utils.widgets import (
    backButton,
    create_buttons,
    create_page_numbers,
    createButton,
    createLabel,
)
from views.single_customer_attendance import SingleCustomer


class AttendanceView(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.limit = 3
        self.offset = 0
        self.current_page = 1
        self.total_records = self.db.total_records()
        self.paginated_members = []
        self.show_dots = False
        self.has_prev = False
        self.has_next = False
        self.total_buttons = None
        self.customers = []
        self._paginate()

        # res = self.db.delete(("id",), (7,), table_name="attendance")
        # print(res)
        self.create_ui()
        print(self.total_records)

    def _paginate(self):
        self.customers = self.db.join(
            ["customers", "attendance"], self.limit, self.offset
        )

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
            row=1, column=1, sticky="w"
        )
        self.customers_frame = Frame(self)
        self.customers_frame.grid(row=2, column=1, sticky="nsew")
        self._config_gridcolumn(self.customers_frame)
        createLabel(self.customers_frame, "Id").grid(row=1, column=1, sticky="nsew")
        createLabel(self.customers_frame, "Name").grid(row=1, column=2, sticky="nsew")
        createLabel(self.customers_frame, "Check in").grid(
            row=1, column=3, sticky="nsew"
        )
        createLabel(self.customers_frame, "Check out").grid(
            row=1, column=4, sticky="nsew"
        )
        createLabel(self.customers_frame, "Action").grid(row=1, column=5, sticky="nsew")

        self._display_customers()
        self.row_frame = tk.Frame(self)
        self.row_frame.grid(row=4, column=3, sticky="nsew", pady=20)

        self.sub_row, self.total_buttons, self.prev_button, self.next_button = (
            create_page_numbers(
                self.total_records, self.row_frame, self.change_page, limit=self.limit
            )
        )

    def change_page(self, page):
        if page == self.current_page:
            return
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
        for i in range(6):
            frame.columnconfigure(i, weight=1)

    def _display_customers(self):
        print(self.customers)
        if self.customers:
            self.customers_row = Frame(self.customers_frame)
            self.customers_row.grid(
                row=2, column=0, columnspan=6, sticky="nsew", pady=10
            )
            self._config_gridcolumn(self.customers_row)

            for i, customer in enumerate(self.customers):
                # Create a container frame for each row to bind the click event
                row_frame = Frame(self.customers_row)
                self._config_gridcolumn(row_frame)
                row_frame.grid(row=i, column=0, columnspan=6, sticky="nsew", pady=10)
                row_frame.bind(
                    "<Button-1>",
                    lambda e, customer=customer: self._on_row_click(customer),
                )

                createLabel(row_frame, f"{customer[0]}").grid(
                    row=0, column=1, sticky="nsew", pady=10
                )
                createLabel(row_frame, f"{customer[1]}").grid(
                    row=0, column=2, sticky="nsew", pady=10
                )

                checkin_var = tk.BooleanVar(row_frame)
                checkin_box = Checkbutton(
                    row_frame,
                    variable=checkin_var,
                    command=lambda customer_id=customer[0]: self._check_in(customer_id),
                )
                checkin_box.grid(row=0, column=3, sticky="nsew", pady=10)

                checkout_var = tk.BooleanVar(row_frame)
                checkout_box = Checkbutton(
                    row_frame,
                    variable=checkout_var,
                    command=lambda customer_id=customer[0]: self._check_out(
                        customer_id
                    ),
                )

                checkout_box.grid(row=0, column=4, sticky="nsew", pady=10)
                createButton(
                    row_frame,
                    "View Attendance",
                    command=lambda customer=customer: self._on_row_click(customer),
                ).grid(row=0, column=5, sticky="nsew")

                # Disabling checkboxes if already checked
                today = datetime.now().strftime("%Y-%m-%d")

                if customer[2] is not None:
                    checkin_var.set(True)
                    checkin_box.config(state="disabled")
                if customer[3] is not None:
                    checkout_var.set(True)
                    checkout_box.config(state="disabled")

        else:
            createLabel(self, "No customers found").grid(
                row=2, column=1, columnspan=3, sticky="ew"
            )

    def _on_row_click(self, customer):
        try:

            SingleCustomer(self.db, customer)
        except Exception as e:
            logger.info(f"An exception occurred:{e}")

    # Implement the logic for what should happen when the row is clicked

    def _check_in(self, customer_id):
        table_name = "attendance"
        col = ["check_in", "customer_id"]
        check_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = (check_in, customer_id)
        res = self.db.insert(values, col, table_name)
        if res:
            print(f"res:{res}")

    def _check_out(self, customer_id):
        table_name = "attendance"
        col = ["checkout", "customer_id"]
        check_out = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        today_date = datetime.now()

        formatted_date = today_date.strftime("%Y-%m-%d")

        attendance_id = self.db.get_specific(
            ("customer_id", "DATE(check_in)"),
            (customer_id, formatted_date),
            ("id",),
            table_name,
        )[0][0]
        res = self.db.update(
            ["checkout"],
            (check_out,),
            attendance_id,
            table_name=table_name,
            where="id",
        )
