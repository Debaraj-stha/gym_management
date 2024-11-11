from curses.ascii import isdigit
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

from utils.constraints import TABLENAME
from utils.helper import config_grid_col, config_grid_row
from utils.widgets import createButton


class AddUpdateInvoice(tk.Toplevel):
    def __init__(self, db, invoice=None, invoice_id=None):
        print(f"invoice id:{invoice_id}")
        super().__init__()
        print(invoice)
        self._invoice_id = invoice_id
        self.title("Update Invoice")
        self.geometry("400x300")
        self.config(padx=10, pady=10)
        self.resizable(False, False)
        self._db = db
        self._invoice = invoice
        # initializing the field
        self._amount = tk.DoubleVar(value=0.0)
        self._remaining_amount = tk.DoubleVar()
        self._amount_to_pay = tk.DoubleVar(value=4000)
        config_grid_col(self, 3)
        config_grid_row(self, 5)
        self._create_ui()

    def _create_ui(self):
        label_amount = tk.Label(self, text="Amount")
        label_amount.grid(row=1, column=1, sticky="w")
        entry_amount = tk.Entry(
            self,
            textvariable=self._amount,
        )
        # binding keyup event to entry
        entry_amount.bind("<KeyRelease>", self._validate_amount)
        entry_amount.grid(row=1, column=2)

        label_to_pay = tk.Label(self, text="Amount to Pay")
        label_to_pay.grid(row=2, column=1, sticky="w")
        amount_to_pay_entry = tk.Entry(
            self, textvariable=self._amount_to_pay, state="readonly"
        )

        amount_to_pay_entry.grid(row=2, column=2)

        label_remaining_amount = tk.Label(self, text="Remaining Amount")
        label_remaining_amount.grid(row=3, column=1, sticky="w")
        remaining_amount_entry = tk.Entry(
            self, textvariable=self._remaining_amount, state="readonly"
        )
        remaining_amount_entry.grid(row=3, column=2)

        createButton(
            self,
            "Save",
            command=self._save,
            state="active",
        ).grid(row=5, column=1, columnspan=2)

    def _save(self):
        try:
            amount = self._amount.get()
            invoice_id = self._invoice[0]
            remaining_amount = self._remaining_amount.get()
            amount_to_pay = self._amount_to_pay.get()
            table_name = TABLENAME.INVOICE.value
            columns = [
                "amount_paid",
                "remaining_amount",
                "amount_to_pay",
                "last_paid_amount",
                "last_paid_date",
            ]
            today = datetime.now().date().strftime("%Y-%m-%d")
            data = (amount, remaining_amount, amount_to_pay, today, amount)

            res = self._db.update(
                columns,
                data,
                (invoice_id,)(
                    "invoice_id",
                ),
                table_name=table_name,
            )
            if res:
                messagebox.showinfo("Success", "Invoice saved successfully")
                self.destroy()
            else:
                messagebox.showerror("Error", "Failed to save invoice")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _validate_amount(self, event):
        try:

            amount = self._amount.get()

            # Handle Backspace or Delete key separately by recalculating based on the text
            if event.keycode in (22, 119):  # Backspace and Delete
                # Default to 0.0 if the field is empty after deletion
                amount = amount if amount else 0.0
                self._amount.set(amount)
            else:
                amount = self._amount.get()
            if amount < 0:
                messagebox.showerror("Error", "Amount cannot be negative")
                self._amount.set(0.0)
                self._amount_to_pay.set(4000)
                self._remaining_amount.set(4000)
            elif amount > 4000:
                messagebox.showerror("Error", "Amount cannot exceed 4000")
                self._amount.set(4000)
                self._amount_to_pay.set(0)
                self._remaining_amount.set(0)
            else:
                self._amount_to_pay.set(4000 - amount)
                self._remaining_amount.set(4000 - amount)
            return True

        except ValueError as e:

            messagebox.showerror("Error", f"{e}")
            self._amount.set(0.0)
            self._amount_to_pay.set(4000)
            self._remaining_amount.set(4000)
