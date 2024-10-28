import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
from datetime import datetime, timedelta

from numpy import delete
from pyparsing import col

from utils.helper import focusIn, focusOut
from utils.widgets import createButton, createLabel
from resources.data import subscription_value


fees = {"Annual": 13000, "Monthly": 1200}


class AddMember(tk.Toplevel):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.last_clicked_time = time.time()
        self.config(padx=10, pady=10)
        self.title("Add Member")
        self.geometry("500x500")
        self.resizable(False, False)
        self._config_row_col()
        self.create_ui()

    def _config_row_col(self):
        # Configure rows for padding
        self.grid_rowconfigure(0, pad=20)  # Padding row
        self.grid_rowconfigure(9, pad=10)  # Padding row for button spacing

        # Configure columns
        self.grid_columnconfigure(0, weight=1)  # Padding column
        self.grid_columnconfigure(1, weight=1)  # Entry column
        self.grid_columnconfigure(2, weight=1)  # Padding column

    def create_ui(self):
        # Labels and Entry Widgets
        createLabel(self, "Name:").grid(
            row=1,
            column=1,
            sticky="w",
        )
        self.name_entry = tk.Entry(
            self,
            validate="focusout",
            validatecommand=(self.register(self._validate_text), "%P"),
        )
        self.name_entry.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=(0, 10),
        )

        createLabel(self, "Email:").grid(
            row=3,
            column=1,
            sticky="w",
        )
        self.email_entry = tk.Entry(
            self,
            validate="focusout",
            validatecommand=(self.register(self._validate_email), "%P"),
        )
        self.email_entry.grid(
            row=4,
            column=1,
            sticky="ew",
            pady=(0, 10),
        )

        createLabel(self, "Phone:").grid(
            row=5,
            column=1,
            sticky="w",
        )
        self.phone_entry = tk.Entry(
            self,
            validate="focusout",
            validatecommand=(self.register(self._validate_phone), "%P"),
        )
        self.phone_entry.grid(
            row=6,
            column=1,
            sticky="ew",
            pady=(0, 10),
        )

        createLabel(self, "Subscription:").grid(
            row=7,
            column=1,
            sticky="w",
        )
        self.subscription_combobox = ttk.Combobox(
            self,
            values=subscription_value,
        )
        # Bind the event to the combobox selection change
        self.subscription_combobox.bind("<<ComboboxSelected>>", self._change_fee)
        self.subscription_combobox.set("Select Subscription")

        self.subscription_combobox.grid(
            row=8,
            column=1,
            sticky="ew",
            pady=(0, 10),
        )
        createLabel(self, "Subscription charge:").grid(
            row=9,
            column=1,
            sticky="w",
        )

        self.subscription_charge_box = ttk.Combobox(self, state="readonly,")
        self.subscription_charge_box.set("...")
        self.subscription_charge_box.grid(
            row=10,
            column=1,
            sticky="ew",
            pady=(0, 10),
        )

        createLabel(self, "Amount Paid:").grid(
            row=11,
            column=1,
            sticky="w",
        )
        self.amount_paid_entry = tk.Entry(
            self,
            validate="focusout",
            validatecommand=(self.register(self._validate_amount), "%P"),
        )
        self.amount_paid_entry.insert(0, "0.0")

        self.amount_paid_entry.grid(
            row=12,
            column=1,
            sticky="ew",
            pady=(0, 10),
        )
        # registering event listeners
        self.amount_paid_entry.bind("<FocusIn>", lambda e: focusIn(e))
        # self.amount_paid_entry.bind("<FocusOut>", lambda e: focusOut(e, "0.0"))

        # Centering the Button
        self.add_btn = createButton(
            self,
            "Add Member",
            command=self.add,
            state="active",
        )
        self.add_btn.grid(
            row=13,
            column=1,
            pady=50,
            sticky="ew",
            columnspan=1,
        )

    def add(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        subscription = self.subscription_combobox.get()
        if (
            not self._validate_text(name)
            or not self._validate_email(email)
            or not self._validate_phone(phone)
            or not self._validate_subscription(subscription)
        ):
            return
        amount_paid = self.amount_paid_entry.get()
        total_amount = self.subscription_charge_box.get()
        self.add_btn.config(state="disabled")

        if subscription == subscription_value[1]:
            membership_expiry = datetime.now() + timedelta(days=30)
        else:
            membership_expiry = datetime.now() + timedelta(days=365)
        amount_paid_date = datetime.now()
        col = (
            "name" "email",
            "phone",
            "subscription_type",
            "membership_expiry",
            "subscription_price",
            "total_amount_paid",
            "last_payment_date",
        )
        customer = (
            name,
            email,
            phone,
            subscription,
            membership_expiry,
            total_amount,
            amount_paid,
            amount_paid_date,
        )
        row_id = self.db.insert(customer, col)
        if row_id is not None:
            self.name_entry.delete(0, "end")
            self.phone_entry.delete(0, "end")
            self.email_entry.delete(0, "end")
            self.subscription_combobox.set("Select Subscription")
            self.subscription_charge_box.set("...")
            self.amount_paid_entry.delete(0, "end")
            self.subscription_charge_box.set("...")

        self.after(2000, self._enable_button)

    def _enable_button(self):
        self.add_btn.config(state="active")

    def _validate_text(self, value):
        if len(value.strip()) == 0:
            messagebox.showerror("Validation Error", "This field is required")
            return False
        return True

    def _validate_email(self, email):

        if "@" not in email or "." not in email.split("@")[-1]:
            messagebox.showerror("Validation Error", "Invalid email format")
            return False
        return True

    def _validate_phone(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Validation Error", "Invalid phone number format")
            return False
        return True

    def _validate_subscription(self, subscription):
        if (
            subscription == "Select Subscription"
            or subscription not in subscription_value
        ):
            messagebox.showerror(
                "Validation Error", "Please select a valid subscription type"
            )
            return False

        return True

    def _change_fee(self, *args):
        subscription = self.subscription_combobox.get()

        if subscription == "Select Subscription" or subscription is None:
            return

        fee = fees[subscription]
        self.subscription_charge_box.set(str(fee))

    def _validate_amount(self, amount):
        try:
            float(amount)
            return True
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid amount format")
            return False
