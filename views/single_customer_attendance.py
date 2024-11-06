import tkinter as tk

from utils.widgets import create_buttons, create_page_numbers, createLabel


class SingleCustomer(tk.Tk):
    def __init__(self, db, customer):
        super().__init__()
        self.db = db
        self.customer = customer
        self.limit = 3
        self.offset = 0
        self.current_page = 1
        self.has_next = False
        self.has_prev = False
        self.total_records = self.db.total_records(
            ("customer_id",),
            (customer[0],),
            table_name="attendance",
        )
        self.config(padx=10, pady=10)
        self.attendance = []
        self.title(f"{customer[1]}")
        self.geometry("500x500")
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)
        self.resizable(False, False)
        self._paginate()
        self.create_widgets()

    def create_widgets(self):
        self.tool_frame = tk.Frame(self)
        self.tool_frame.grid(
            row=0, column=0, sticky="nsew"
        )  # Change column=1 to column=0
        self.tool_frame.grid_rowconfigure(0, weight=1)
        self.tool_frame.grid_rowconfigure(1, weight=1)
        self.tool_frame.grid_rowconfigure(2, weight=1)
        self.tool_frame.grid_rowconfigure(3, weight=1)
        self._config_columns(self.tool_frame)

        createLabel(self.tool_frame, f"Attendance of {self.customer[1]}").grid(
            row=1,
            column=0,
            sticky="w",  # Change column=1 to column=0, sticky="w" for left alignment
        )
        createLabel(self.tool_frame, "Date:").grid(
            row=2, column=0, sticky="w"
        )  # Left align Date label

        self.date_entry_field = tk.Entry(self.tool_frame)
        self.date_entry_field.grid(
            row=2, column=1, sticky="ew"
        )  # Entry field can remain stretched
        self.date_entry_field.insert(0, "2024-9")
        createLabel(self.tool_frame, "ID").grid(row=3, column=0, sticky="ew", pady=10)
        createLabel(self.tool_frame, "Check In").grid(
            row=3, column=1, sticky="ew", pady=10
        )
        createLabel(self.tool_frame, "Check Out").grid(
            row=3, column=2, sticky="ew", pady=10
        )
        self._display_attendance()
        self.row_frame = tk.Frame(self)
        self.row_frame.grid(row=5, column=0, columnspan=5, sticky="nsew", pady=20)

        self.sub_row, self.total_buttons, self.prev_button, self.next_button = (
            create_page_numbers(
                self.total_records,
                self.row_frame,
                self.change_page,
                limit=self.limit,
                row_index=1,
            )
        )

    def change_page(self, page):
        try:
            if page == self.current_page:
                return

            self.current_page = page
            self.offset = (page - 1) * self.limit
            self.sub_row.destroy()  # Remove old page buttons

            self._paginate()  # Fetch new data based on updated offset
            self._update_table()  # Refresh the table with new data

            # Re-render page numbers
            self.sub_row, self.total_buttons, self.prev_button, self.next_button = (
                create_page_numbers(
                    self.total_records,
                    self.row_frame,
                    self.change_page,
                    limit=self.limit,
                    current_page=self.current_page,
                    row_index=1,
                )
            )
        except Exception as e:
            print(f"Error occurred while changing page: {e}")

    def _update_table(self):
        for widget in self.row_frame.winfo_children():
            widget.destroy()

        self._display_attendance()

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

    def _display_attendance(self):
        self.attendance_frame = tk.Frame(self.tool_frame)
        self._config_columns(self.attendance_frame)
        self.attendance_frame.grid(row=4, column=0, columnspan=3, sticky="nsew")
        for i, attendance in enumerate(self.attendance):
            self._display_row(i + 1, attendance)

    def _display_row(self, index: int, attendance: tuple):

        check_in = attendance[1] if attendance[1] else "N/A"
        check_out = attendance[2] if attendance[2] else "N/A"
        createLabel(self.attendance_frame, str(index), fontsize=11).grid(
            row=index, column=0
        )
        createLabel(self.attendance_frame, check_in, fontsize=11).grid(
            row=index, column=1, sticky="ew"
        )
        createLabel(self.attendance_frame, check_out, fontsize=11).grid(
            row=index, column=2, sticky="ew"
        )

    def _config_columns(self, frame: tk.Frame):
        for i in range(7):
            frame.grid_columnconfigure(i, weight=1)

    def _paginate(self):
        self.attendance = self.db.get_specific(
            ("customer_id",),
            (self.customer[0],),
            limit=self.limit,
            offset=self.offset,
            table_name="attendance",
        )
