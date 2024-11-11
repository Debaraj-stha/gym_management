from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from gettext import gettext as _

from utils.widgets import createButton, createLabel
from resources.data import subscription_value


class UpdateMember(tk.Tk):
    def __init__(self, db, member_id, field_index, old_value=None):
        super().__init__()
        self.db = db
        self.member_id = member_id
        self.old_value = old_value
        self.field_index = field_index

        # Initialize the combobox and entry fields as None
        self.subscription_combobox = None
        self.total_amount_paid = None

        print("self old value: ", self.old_value)

        # Configure column 0 to control left alignment
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Title and window settings
        self.title(_("Update Member"))
        self.geometry("300x200")
        self.resizable(False, False)

        # Create the UI
        self.create_ui()

    def create_ui(self):
        if self.field_index == 5:
            createLabel(self, _("Subscription type")).grid(
                row=1, column=0, padx=20, pady=10, sticky="w"
            )
            self.subscription_combobox = ttk.Combobox(self, values=subscription_value)

            # Ensure old_value is set if provided for the combobox
            if self.old_value:
                self.subscription_combobox.set(self.old_value)
            else:
                self.subscription_combobox.set(_("Select Subscription"))

            self.subscription_combobox.grid(
                row=2, column=0, padx=20, pady=10, sticky="w"
            )

        elif self.field_index == 9:
            createLabel(self, _("Total Amount paid:")).grid(
                row=1, column=0, padx=20, pady=10, sticky="w"
            )

            self.total_amount_paid = tk.Entry(self)
            if self.old_value:
                self.total_amount_paid.insert(0, str(self.old_value))
            self.total_amount_paid.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        createButton(
            self, _("Update"), state="active", command=self._update_record
        ).grid(row=3, column=0, padx=20, pady=10, sticky="w")

    def _update_record(self):
        # Retrieve values based on the initialized widgets
        subscription_type = (
            self.subscription_combobox.get() if self.subscription_combobox else None
        )
        amount = self.total_amount_paid.get() if self.total_amount_paid else None

        # Update the record based on available values
        if subscription_type:
            res = self.db.update_subscription_type(self.member_id, subscription_type)
            if res:
                messagebox.showinfo("Success", "Subscription type updated successfully")
            self.destroy()
        elif amount:
            update_date = datetime.now()
            # Assuming a function `update_amount_paid` exists for updating the amount
            res = self.db.update_total_amount_paid(self.member_id, amount, update_date)
            if res:
                messagebox.showinfo("Success", "Amount paid updated successfully")
            self.destroy()
