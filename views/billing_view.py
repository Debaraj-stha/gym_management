import tkinter as tk
from tkinter import messagebox


from files.add_update_invoice import AddUpdateInvoice
from files.database_schemas import INVOICE_SCHEMA
from utils.constraints import TABLENAME
from utils.helper import config_grid_col, export_to_csv, focusIn, focusOut
from utils.widgets import backButton, create_buttons, create_page_numbers, createButton


class BillingView(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self._controller = controller
        self._db = db
        self._total_records = self._db.total_records(table_name=TABLENAME.INVOICE.value)
        self._limit = 10
        self._offset = 0
        self._current_page = 1
        self._invoices = []
        self._serach_value = tk.StringVar()
        config_grid_col(self, 8)
        self._create_ui()
        self._get_invoices()

    def _create_ui(self):

        tool_row = tk.Frame(self)
        tool_row.grid(row=1, column=1, columnspan=7, sticky="ew", pady=(10, 10))
        config_grid_col(tool_row, 10)
        backButton(tool_row, self._controller).grid(
            row=1, column=0, sticky="ew", pady=10
        )

        placehoder = _("Search here...")

        self._serach_value.set(placehoder)
        serach_entry = tk.Entry(tool_row, textvariable=self._serach_value)
        serach_entry.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        serach_entry.bind("<FocusIn>", focusIn)
        serach_entry.bind("<FocusOut>", lambda event: focusOut(event, placehoder))

        # binding  keyup event

        serach_entry.bind("<KeyRelease>", self._search_customer)

        # createButton(
        #     tool_row,
        #     "Generate new Invoice",
        #     state="active",
        #     command=lambda: AddUpdateInvoice(self._db),
        # ).grid(row=2, column=3, sticky="ew")
        createButton(
            tool_row,
            _("Export to CSV"),
            command=lambda: export_to_csv(
                self._db.get_all(table_name=TABLENAME.INVOICE.value),
                "invoices.csv",
                INVOICE_SCHEMA,
            ),
        ).grid(row=2, column=4, sticky="ew")

        columns = [
            _("INVOICE ID"),
            _("NAME"),
            _("SUBSCRIPTION TYPE"),
            _("DATE"),
            _("AMOUNT TO PAY"),
            _("AMOUNT PAID"),
            _("REMAINING AMOUNT"),
            _("LAST PAID AMOUNT"),
            _("LAST PAID DATE"),
        ]
        self._tree = tk.ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            self._tree.heading(column, text=column, anchor="center")
            self._tree.column(column, anchor="center")

        # inserting  dummy data to treeview
        self._fill_tree()

        # binding events
        self._tree.bind("<Double-Button-1>", self._update_invoice)
        self._tree.bind("<Double-Button-3>", self._delete_invoice)

        self._tree.grid(
            row=3, column=1, columnspan=len(columns), pady=10, sticky="nsew"
        )
        # frame to hold pagination button
        self.row_frame = tk.Frame(self)
        self.row_frame.grid(
            row=6, column=1, columnspan=len(columns), sticky="ew", pady=(30, 10)
        )

        # pagination button
        self.sub_row, self.total_buttons, self.prev_button, self.next_button = (
            create_page_numbers(
                self._total_records,
                self.row_frame,
                self.change_page,
                limit=self._limit,
            )
        )

    def _fill_tree(self):
        if self._invoices:
            # deleting tree row and then updating the records
            self._tree.delete(*self._tree.get_children())

            for invoice in self._invoices:
                self._tree.insert("", "end", values=invoice)
        else:
            self._tree.insert("", "end", values=_("No invoices available"))

    def _refresh(self):
        # refresh the records
        self._offset = 0
        self._get_invoices()
        self._fill_tree()

    def _get_invoices(self, query=""):

        columns_name = (
            ["i", "invoice_id"],
            ["c", "name"],
            ["c", "subscription_type"],
            ["i", "date"],
            ["i", "amount_paid"],
            ["i", "amount_to_pay"],
            ["i", "remaining_amount"],
            # ["i", "last_paid_amount"],
            # ["i", "last_paid_date"],
        )
        self._invoices = self._db.search_invoices(
            columns_name=columns_name,
            limit=self._limit,
            offset=self._offset,
            is_searching=False,
        )
        self._fill_tree()

    def change_page(self, page):
        if page == self.current_page:
            return
        self.current_page = page
        self._offset = (page - 1) * self._limit

        # destoying previuos button pagination
        self.sub_row.destroy()
        self._update_page_button_state()
        create_buttons(
            self.row_frame, self.current_page, self.total_buttons, self.change_page
        )
        self._get_invoices()
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

    def _update_invoice(self, *args):
        try:
            values = self._get_selected_item_values()

            AddUpdateInvoice(self._db, values)
        except Exception as e:
            print(f"Error in updating invoice: {e}")

    def _delete_invoice(self, *args):
        try:
            conf = messagebox.askyesnocancel(
                "Conform", "Are you sure you want to delete this invoice?"
            )
            if not conf:
                return
            values = self._get_selected_item_values()
            instructor_id = values[0]
            # deleting the selected instructor
            res = self._db.delete(
                (instructor_id,),
                ("id",),
                table_name=TABLENAME.INSTRUCTORS.value,
            )
            if res:
                self._refresh()
                messagebox.showerror("Success", "Invoice deleted successfully")
            else:
                messagebox.showerror("Error", "Error deleting invoice")

        except Exception as e:
            print(f"Error in deleting instructor: {e}")

    def _get_selected_item_values(self):
        try:
            item = self._tree.selection()[0]
            values = self._tree.item(item, "values")
            return values
        except Exception as e:
            print(f"Error in getting selected item values: {e}")
            return None

    def _search_customer(self, event):
        query = self._serach_value.get()
        if query.strip():
            if event.keycode == 36:
                print("Searching...")
                self._get_invoices(search_query=query)
