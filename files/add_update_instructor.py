import tkinter as tk
from tkinter import messagebox

from utils.constraints import TABLENAME
from utils.widgets import createButton


class AddUpdateInstructor(tk.Toplevel):
    def __init__(self, db, instructor=None):
        super().__init__()
        self.title(
            "Add/Update Instructor" if instructor is not None else "Add Instructor"
        )
        self.geometry("311x311")
        self.config(padx=11, pady=11)
        self.resizable(False, False)
        self.db = db
        self.instructor = instructor

        # Initialize the text fields and labels as None
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.rate_var = tk.StringVar()

        # assigning old value of instructor
        if instructor is not None:
            self.name_var.set(instructor[1])
            self.email_var.set(instructor[2])
            self.phone_var.set(instructor[3])
            self.rate_var.set(str(instructor[5]))

        # Create the grid layout

        self._config_grid(3)

        self.create_widgets()

    def _config_grid(self, col, row=6):
        for i in range(col):
            self.grid_columnconfigure(i, weight=1)
        for i in range(row):
            self.grid_rowconfigure(i, weight=1)

    def create_widgets(self):
        name_label = tk.Label(self, text="Name:")
        name_label.grid(row=1, column=1, sticky="w", pady=10)
        name_entry = tk.Entry(self, textvariable=self.name_var)
        name_entry.grid(row=1, column=2, pady=10)

        email_label = tk.Label(self, text="Email:")
        email_label.grid(row=2, column=1, sticky="w", pady=10)
        email_entry = tk.Entry(self, textvariable=self.email_var)
        email_entry.grid(row=2, column=2, pady=10)

        phone_label = tk.Label(self, text="Phone:")
        phone_label.grid(row=3, column=1, sticky="w", pady=10)
        phone_entry = tk.Entry(self, textvariable=self.phone_var)
        phone_entry.grid(row=3, column=2, pady=10)

        rate_label = tk.Label(self, text="Rate:")
        rate_label.grid(row=4, column=1, sticky="w", pady=10)
        rate_entry = tk.Entry(self, textvariable=self.rate_var)
        rate_entry.grid(row=4, column=2, pady=10)
        self.rate_var.set("4000")

        save_button = createButton(self, text="Save", command=self.save_instructor)
        save_button.grid(row=6, column=1, columnspan=2, pady=11)

    def save_instructor(self):
        name = self.name_var.get()
        if not name:
            messagebox.showerror("Validation failed", "Name must be provided")
            return
        email = self.email_var.get()
        phone = self.phone_var.get()
        if not phone:
            messagebox.showerror("Validation failed", "Phone must be provided")
            return
        rate = self.rate_var.get()
        if rate == "":
            rate = None
        if rate is not None:
            rate = float(rate)

        data = (name, email, phone, rate)
        cols = ["name", "email", "phone", "rate"]
        if rate is None:
            data = (name, email, phone)
            cols = ["name", "email", "phone"]

        if self.instructor is not None:
            instructor_id = self.instructor[0]

            res = self.db.update(
                cols,
                data,
                (instructor_id,),
                ("id",),
                table_name=TABLENAME.INSTRUCTORS.value,
            )
        else:
            res = self.db.insert(data, cols, table_name=TABLENAME.INSTRUCTORS.value)
        if res:
            messagebox.showinfo("Success", "Instructor saved successfully")
            self.name_var.set("")
            self.email_var.set("")
            self.phone_var.set("")
            self.rate_var.set("4000")
        else:
            messagebox.showerror("Error", "Failed to save instructor")
