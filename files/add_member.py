import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
from datetime import datetime, timedelta

from utils.widgets import createButton, createLabel

subscription_value = ["Annual", "Monthly"]


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
        createLabel(self, "Name:").grid(row=1, column=1, sticky="w")
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

        createLabel(self, "Email:").grid(row=3, column=1, sticky="w")
        self.email_entry = tk.Entry(
            self,
            validate="focusout",
            validatecommand=(self.register(self._validate_email), "%P"),
        )
        self.email_entry.grid(row=4, column=1, sticky="ew", pady=(0, 10))

        createLabel(self, "Phone:").grid(row=5, column=1, sticky="w")
        self.phone_entry = tk.Entry(
            self,
            validate="focusout",
            validatecommand=(self.register(self._validate_phone), "%P"),
        )
        self.phone_entry.grid(row=6, column=1, sticky="ew", pady=(0, 10))

        createLabel(self, "Subscription:").grid(row=7, column=1, sticky="w")
        self.subscription_combobox = ttk.Combobox(
            self,
            values=subscription_value,
        )
        self.subscription_combobox.set("Select Subscription")

        self.subscription_combobox.grid(row=8, column=1, sticky="ew", pady=(0, 10))

        # Centering the Button
        self.add_btn = createButton(
            self, "Add Member", command=self.add, state="active"
        )
        self.add_btn.grid(row=10, column=1, pady=50, sticky="ew", columnspan=1)

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
        self.add_btn.config(state="disabled")

        if subscription == subscription_value[1]:
            membership_expiry = datetime.now() + timedelta(days=30)
        else:
            membership_expiry = datetime.now() + timedelta(days=365)
        subscription_price = 9999
        amount_paid = 6000
        customer = (
            name,
            email,
            phone,
            subscription,
            membership_expiry,
            subscription_price,
            amount_paid,
        )
        self.db.insert(customer)

        self.after(2000, self._enable_button)

    def _enable_button(self):
        self.add_btn.config(state="active")

    def _validate_text(self, value):
        if len(value.strip()) == 0:
            messagebox.showerror("Validation Error", "This field is required")
            return False
        return True

    def _validate_email(self, email):
        print(email.split("@")[-1])
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
