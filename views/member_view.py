import tkinter as tk
from tkinter import Frame, IntVar, ttk
from tkinter.ttk import Style, Treeview, Combobox
import os
from tkinter import messagebox

import pandas as pd

from files.update_member import UpdateMember
from utils.widgets import (
    backButton,
    create_buttons,
    create_page_numbers,
    createButton,
    createLabel,
)
from files.add_member import AddMember
from utils.helper import focusIn, focusOut

days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]


class MembersView(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        # initialization
        self.controller = controller
        self.db = db
        self.limit = 2
        self.offset = 0
        self.current_page = 1
        self.total_records = self.db.total_records()
        self.paginated_members = []
        self.show_dots = False
        self.has_prev = False
        self.has_next = False
        self.total_buttons = 1
        self.sort_by_columns = None
        self.db.send_membership_expiring_message(26)
        self._config_row_column()
        self._paginate()

        self.create_ui()

    def create_ui(self):
        # Add members table and search bar here
        toolrow = tk.Frame(self)
        toolrow.grid(row=1, column=1, sticky="ew", pady=(10, 0))
        toolrow.grid_rowconfigure(0, weight=1)
        toolrow.grid_rowconfigure(1, weight=1)
        toolrow.grid_columnconfigure(2, weight=1)
        toolrow.grid_columnconfigure(0, weight=1)
        toolrow.grid_columnconfigure(1, weight=3)
        toolrow.grid_columnconfigure(2, weight=1)

        backButton(self, self.controller)  ##back button

        # toolbar rows

        self.search_entry = tk.Entry(
            toolrow,
            cursor="hand2",
            font=("Arial", 12),
            relief="groove",
            bg="#ffffff",
            fg="#000000",
        )

        self.search_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0))
        self.search_entry.insert(0, "Search Members...")

        # registering events
        self.search_entry.bind("<FocusIn>", lambda event: focusIn(event))

        self.search_entry.bind(
            "<FocusOut>", lambda event: focusOut(event, "Search Members...")
        )

        self.search_entry.bind("<KeyRelease>", self.search)

        createLabel(toolrow, "From:").grid(row=1, column=3, sticky="ew")
        self.from_date_entry = tk.Entry(toolrow)
        self.from_date_entry.insert(0, "2020-09-01")
        self.from_date_entry.grid(row=1, column=4, sticky="ew", padx=(10, 0))

        createLabel(toolrow, "To:").grid(row=1, column=5, sticky="ew")
        self.to_date_entry = tk.Entry(toolrow)
        self.to_date_entry.insert(0, "2020-09-01")
        self.to_date_entry.grid(row=1, column=6, sticky="ew", padx=(10, 0))

        # adding  events to date entry
        self.to_date_entry.bind("<FocusIn>", lambda event: focusIn(event))
        self.from_date_entry.bind("<FocusIn>", lambda event: focusIn(event))
        self.to_date_entry.bind(
            "<FocusOut>", lambda event: focusOut(event, "2020-09-01")
        )
        self.from_date_entry.bind(
            "<FocusOut>", lambda event: focusOut(event, "2020-09-01")
        )

        self.to_date_entry.bind(
            "<KeyRelease>", lambda event: self._get_customer_between(event)
        )
        self.from_date_entry.bind(
            "<KeyRelease>", lambda event: self._get_customer_between(event)
        )

        createLabel(toolrow, "Membership is expiring on days:").grid(
            row=1,
            column=7,
            sticky="ew",
        )
        self.days_before_expiry_entry = Combobox(toolrow, values=days)
        self.days_before_expiry_entry.current(0)
        self.days_before_expiry_entry.grid(row=1, column=8, sticky="ew")
        createLabel(toolrow, "Get pending payment customers:").grid(
            row=2, column=1, sticky="w"
        )
        self.get_pending_customer_var = IntVar()
        ttk.Checkbutton(
            toolrow,
            command=self._get_pending_customer,
            variable=self.get_pending_customer_var,
        ).grid(row=2, column=2, sticky="w")
        sort_by_columns = [
            "name",
            "email",
            "phone",
            "subscription_date",
            "last_payment_date",
            "membership_expiry",
        ]
        sort_order = ["asc", "desc"]
        self.sort_by_columns_combobox = Combobox(toolrow, values=sort_by_columns)
        self.sort_by_columns_combobox.grid(row=2, column=3, sticky="nsew")
        self.sort_by_columns_combobox.set(
            "Sort by",
        )
        self.sort_order_combobox = Combobox(toolrow, values=sort_order)
        self.sort_order_combobox.current(0)
        self.sort_order_combobox.grid(row=2, column=4, sticky="nsew", padx=(10))
        self.sort_by_columns_combobox.bind("<<ComboboxSelected>>", self._sort)
        self.sort_order_combobox.bind("<<ComboboxSelected>>", self._sort)

        # frame to hold button row
        button_row = Frame(toolrow)
        button_row.grid(row=3, column=1, columnspan=5, sticky="ew", pady=(10, 0))
        createButton(
            button_row, "Export as CSV", command=lambda: self._export_to_csv()
        ).grid(row=3, column=1, sticky="nsew", padx=10)

        createButton(
            button_row, "Export as json", command=lambda: self._export_to_json()
        ).grid(row=3, column=2, sticky="nsew", padx=(10))
        createButton(
            button_row, "Export as excel", command=lambda: self._export_to_excel()
        ).grid(row=3, column=3, sticky="nsew", padx=(10))
        createButton(button_row, "Print", command=lambda: self._print()).grid(
            row=3, column=4, sticky="w", padx=(10)
        )

        # adding members
        createButton(
            self, "Add member", command=lambda: AddMember(self.db), state="active"
        ).grid(row=2, column=1, sticky="w")

        tree_scroll = tk.Scrollbar(
            self,
            orient="vertical",
        )
        tree_scroll_horizontal = tk.Scrollbar(self, orient="horizontal")

        tree_scroll.grid(row=3, column=8, sticky="ns")

        columns = [
            "Id",
            "Name",
            "Email",
            "Phone",
            "Subscription",
            "Subscription Date",
            "membership_expiry",
            "subscription_price",
            "total_amount_paid",
            "last_payment_date",
            "Status",
            "Action",
        ]

        # Add members table here
        self.treeview = Treeview(
            self,
            selectmode="browse",
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll.set,
            xscrollcommand=tree_scroll_horizontal.set,
        )

        for col in columns:
            self.treeview.heading(f"{col}", text=f"{col}", anchor="center")
            self.treeview.column(col, anchor="center", width=150)  # Center the content

        for member in self.paginated_members:
            self.treeview.insert("", "end", values=member)

        tree_scroll.config(command=self.treeview.yview)
        tree_scroll_horizontal.config(command=self.treeview.xview)

        style = Style()
        style.map(
            "Treeview",
            background=[("selected", "green")],
            foreground=[("selected", "white")],
        )

        self.treeview.grid(row=3, column=1, columnspan=7, sticky="nsew")
        tree_scroll_horizontal.grid(row=4, column=1, columnspan=7, sticky="ew")
        self.treeview.bind("<Double-Button-1>", self._delete_record)
        self.treeview.bind("<Button-1>", self._edit_record)
        self.row_frame = tk.Frame(self)
        self.row_frame.grid(row=6, column=1, sticky="ew")
        # pagination button
        self.sub_row, self.total_buttons, self.prev_button, self.next_button = (
            create_page_numbers(
                self.total_records, self.row_frame, self.change_page, limit=self.limit
            )
        )

    def _sort(self, event):
        self.sort_order = self.sort_order_combobox.get()
        self.sort_by_columns = self.sort_by_columns_combobox.get()
        self._paginate(order_by=self.sort_by_columns, sort_order=self.sort_order)
        self.change_page(1)

    def _edit_record(self, event):

        item = self.treeview.selection()

        if item:

            record = self.treeview.item(item[0], "values")
            clicked_column = self.treeview.identify_column(event.x)
            id = record[0]
            column_index = int(clicked_column.split("#")[1])

            if id is None:

                return
            old_value = record[column_index - 1]
            if column_index == 5:

                UpdateMember(self.db, id, column_index, old_value)

            elif column_index == 9:
                # old_value = record[8]
                UpdateMember(self.db, id, column_index, old_value)

    def _delete_record(self, event):
        conf = messagebox.askyesno("Conform", "Are you sure you want to delete?")
        if conf:
            item = self.treeview.selection()[0]
            self.db.delete_customer(self.treeview.item(item, "values")[0])
            self._paginate()

    def prev_page(self):
        if self.current_page > 1:
            self.change_page(self.current_page - 1)

    def next_page(self):
        if self.current_page < self.total_buttons:
            self.change_page(self.current_page + 1)

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

    def _paginate(self, **kwargs):
        end = self.current_page * self.limit
        start = self.offset
        if "order_by" in kwargs and "sort_order" in kwargs:
            order_by = kwargs["order_by"]
            sort_order = kwargs["sort_order"]
            self.paginated_members = self.db.get_customers(
                limit=self.limit,
                offset=self.offset,
                order_by=order_by,
                sort_order=sort_order,
            )
            return
        self.paginated_members = self.db.get_customers(
            limit=self.limit, offset=self.offset
        )

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
        if self.sort_by_columns is not None:
            self._paginate(order_by=self.sort_by_columns, sort_order=self.sort_order)
        else:
            self._paginate()

        self._update_table()

    def _update_table(self):
        self.treeview.delete(*self.treeview.get_children())
        if self.paginated_members:
            for member in self.paginated_members:
                self.treeview.insert("", "end", values=member)
        else:
            pass
        # Force UI redraw if necessary
        self.treeview.update_idletasks()

    def insert_placeholder(self):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, "Search Members...")

    def search(self, event):
        query = self.search_entry.get()

        # Define is_get_result as an instance variable if it doesn't exist
        if not hasattr(self, "is_get_result"):
            self.is_get_result = False

        if event.keycode == 36 and query.strip() != "":
            self.old_value = self.paginated_members
            self.is_get_result = True
            self.current_page = 1
            self.offset = 0

            res = self.db.search(
                query,
                column_names=[
                    ["t1", "id"],
                    ["t1", "name"],
                    ["t2", "check_in"],
                    ["t2", "checkout"],
                ],
                search_column=["name", "phone", "email", "t1.id"],
                table_name="customers",
                join_with="attendance",
                join_column=["id", "customer_id"],
            )
            self.customers = res
            self._update_table()
            self._update_page_button_state()

            self.total_records = len(res)

            # Check if self.sub_row exists before forgetting and destroying
            if hasattr(self, "sub_row") and self.sub_row:
                self.sub_row.grid_forget()
                self.sub_row.destroy()

            # Recreate row_frame if necessary
            if hasattr(self, "row_frame"):
                self.row_frame.grid_forget()
                self.row_frame.destroy()

            self.row_frame = tk.Frame(self)
            self.row_frame.grid(row=4, column=3, sticky="nsew", pady=20)

            # Create pagination buttons based on search results
            self.sub_row, self.total_buttons, self.prev_button, self.next_button = (
                create_page_numbers(
                    self.total_records,
                    self.row_frame,
                    self.change_page,
                    limit=self.limit,
                    current_page=self.current_page,
                )
            )

            return

        # Reset search results if escape key (22) is pressed
        if self.is_get_result and event.keycode == 22:
            self.search_entry.delete(0, tk.END)
            self.paginated_members = self.old_value
            self.total_records = self.db.total_records()

            if hasattr(self, "sub_row") and self.sub_row:
                self.sub_row.grid_forget()
                self.sub_row.destroy()
            # Recreate row_frame if necessary
            if hasattr(self, "row_frame"):
                self.row_frame.grid_forget()
                self.row_frame.destroy()

            self.row_frame = tk.Frame(self)
            self.row_frame.grid(row=4, column=3, sticky="nsew", pady=20)

            # Create pagination buttons based on search results
            self.sub_row, self.total_buttons, self.prev_button, self.next_button = (
                create_page_numbers(
                    self.total_records,
                    self.row_frame,
                    self.change_page,
                    limit=self.limit,
                    current_page=self.current_page,
                )
            )
            self._update_table()
            self._update_page_button_state()

    def _config_row_column(self):
        for i in range(2, 10):
            self.grid_rowconfigure(i, weight=1)
        for i in range(1, 14):
            self.grid_columnconfigure(i, weight=1)

    def _get_customer_between(self, event):
        if event.keycode == 36:
            self.current_page = 1
            self.offset = 1
            to_date = self.to_date_entry.get()
            from_date = self.from_date_entry.get()
            between = ("subscription_date", from_date, to_date)

            self.paginated_members = self.db.get_customers(between=between)
            self._update_table()

    def _get_pending_customer(self):
        state = self.get_pending_customer_var.get()

        if state:
            self.total_records = self.db.count_pending_payment_customers()

            self.create_page_numbers()
            res = self.db.get_customer_by_pending_payment(self.limit, self.offset)

            self.paginated_members = res

            self._update_table()

    def _export_to_csv(self):
        try:
            # Fetch data to export
            customers = self.db.get_all()
            print("Exporting to CSV")

            df = pd.DataFrame(customers)

            # Define the target directory path within the current working directory
            directory = self._make_directory()
            # Define the complete file path
            file_path = os.path.join(directory, "customers.csv")

            # Save CSV file to the specified directory
            df.to_csv(file_path, index=False)

            print(f"CSV exported successfully to {file_path}")

        except Exception as e:
            print(f"An error occurred while exporting to CSV: {e}")

    def _export_to_json(self, *args):
        try:
            # Fetch data to export
            customers = self.db.get_all()
            print("Exporting to JSON")

            df = pd.DataFrame(customers)

            # Define the target directory path within the current working directory
            directory = self._make_directory()
            # Define the complete file path
            file_path = os.path.join(directory, "customers.json")

            # Save JSON file to the specified directory
            df.to_json(file_path, orient="records")

            print(f"JSON exported successfully to {file_path}")
            pass
        except Exception as e:
            print(f"An error occurred while exporting to JSON: {e}")

    def _export_to_excel(self, *args):
        try:
            # Fetch data to export
            customers = self.db.get_all()
            print("Exporting to Excel")

            df = pd.DataFrame(customers)

            # Define the target directory path within the current working directory
            directory = self._make_directory()
            # Define the complete file path
            file_path = os.path.join(directory, "customers.xlsx")

            # Save Excel file to the specified directory
            df.to_excel(file_path, index=False)

            print(f"Excel exported successfully to {file_path}")
        except Exception as e:
            print(f"An error occurred while exporting to Excel: {e}")

    def _print(self, *args):
        try:
            # Fetch data to export
            customers = self.db.get_all()
            print("Printing")

        except Exception as e:
            print(f"An error occurred while printing: {e}")

    def _make_directory(self, directory="data"):
        """ ""
        Define the target directory path within the current working directory
        """
        directory = os.path.join(os.getcwd(), directory)

        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory
