import tkinter as tk
from tkinter import messagebox

from files.add_update_instructor import AddUpdateInstructor
from utils.constraints import TABLENAME
from utils.widgets import backButton, create_buttons, create_page_numbers, createButton


class InstructorView(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)

        self.controller = controller
        self.db = db
        self.instructors = []
        self.limit = 10
        self.offset = 0
        self.current_page = 0
        self.total_buttons = 0
        self.total_records = self.db.total_records(
            table_name=TABLENAME.INSTRUCTORS.value
        )
        print(self.total_records)
        self._get_instructors()
        self._config_grid(self, 8)
        self.create_ui()

    def _get_instructors(self):
        res = self.db.get_customers(
            table_name=TABLENAME.INSTRUCTORS.value, limit=self.limit, offset=self.offset
        )
        self.instructors = res

    def create_ui(self):
        toolrow = tk.Frame(self)
        backButton(toolrow, self.controller).grid(row=1, column=1, sticky="ew")
        toolrow.grid(row=2, column=1, sticky="ew", pady=(10, 10))
        createButton(
            toolrow,
            "Add Instructor",
            state="active",
            command=lambda: AddUpdateInstructor(self.db),
        ).grid(row=3, column=1, sticky="w", pady=10)
        createButton(
            toolrow,
            "Refresh",
            command=lambda: self._refresh,
        ).grid(row=3, column=2, sticky="w")

        columns = ["ID", "NAME", "EMAIL", "PHONE", "JOINED AT", "RATE"]
        self.tree = tk.ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            self.tree.heading(column, text=column, anchor="center")
            self.tree.column(column, anchor="center")
        self._fill_tree()
        self.tree.grid(row=4, column=1, columnspan=len(columns), sticky="nsew")
        # binding events
        self.tree.bind("<Double-Button-1>", self._update_instructor)
        self.tree.bind("<Double-Button-3>", self._delete_instructor)

        # frame to hold pagination button
        self.row_frame = tk.Frame(self)
        self.row_frame.grid(
            row=6, column=1, columnspan=len(columns), sticky="ew", pady=(30, 10)
        )

        # pagination button
        self.sub_row, self.total_buttons, self.prev_button, self.next_button = (
            create_page_numbers(
                self.total_records, self.row_frame, self.change_page, limit=self.limit
            )
        )

    def _fill_tree(self):
        if self.instructors is not None:
            # deleting tree row and then updating the records
            self.tree.delete(*self.tree.get_children())

            for instructor in self.instructors:
                self.tree.insert("", "end", values=instructor)

    def _refresh(self):
        # refresh the records
        self.offset = 0
        self._get_instructors()
        self._fill_tree()

    def _config_grid(self, frame: tk.Frame, col, row=5):
        for i in range(col):
            frame.columnconfigure(i, weight=1)

    def change_page(self, page):
        if page == self.current_page:
            return
        self.current_page = page
        self.offset = (page - 1) * self.limit

        # destoying previuos button pagination
        self.sub_row.destroy()
        self._update_page_button_state()
        create_buttons(
            self.row_frame, self.current_page, self.total_buttons, self.change_page
        )
        self._get_instructors()
        self._fill_tree()

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

    def _update_instructor(self, *args):
        try:
            values = self._get_selected_item_values()
            AddUpdateInstructor(self.db, values)
        except Exception as e:
            print(f"Error in updating instructor: {e}")

    def _delete_instructor(self, *args):
        try:
            conf = messagebox.askyesnocancel(
                "Conform", "Are you sure you want to delete this instructor?"
            )
            if not conf:
                return
            values = self._get_selected_item_values()
            instructor_id = values[0]
            # deleting the selected instructor
            res = self.db.delete(
                (instructor_id,)(
                    "id",
                ),
                table_name=TABLENAME.INSTRUCTORS.value,
            )
            if res:
                self._refresh()
                messagebox.showerror("Success", "Instructor deleted successfully")
            else:
                messagebox.showerror("Error", "Error deleting instructor")

        except Exception as e:
            print(f"Error in deleting instructor: {e}")

    def _get_selected_item_values(self):
        try:
            item = self.tree.selection()[0]
            values = self.tree.item(item, "values")
            return values
        except Exception as e:
            print(f"Error in getting selected item values: {e}")
            return None
