import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class AddMember(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.config(padx=10, pady=10)
        self.title("Add Member")
        self.geometry("500x500")
        self.resizable(False, False)
        self._config_row_col()
        self.create_ui()

    def _config_row_col(self):
        # Configure rows for padding
        self.grid_rowconfigure(0, pad=10)
        self.grid_rowconfigure(9, pad=10)

        # Configure columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def create_ui(self):
        # Labels and Entry Widgets with validation
        ttk.Label(self, text="Name:").grid(row=1, column=1, sticky="w")
        self.name_entry = tk.Entry(
            self,
            validate="focusout",
            validatecommand=(self.register(self.validate_name), "%P"),
        )
        self.name_entry.grid(row=2, column=1, sticky="ew")

        ttk.Label(self, text="Email:").grid(row=3, column=1, sticky="w")
        self.email_entry = tk.Entry(
            self,
            validate="focusout",
            validatecommand=(self.register(self.validate_email), "%P"),
        )
        self.email_entry.grid(row=4, column=1, sticky="ew")

        ttk.Label(self, text="Phone:").grid(row=5, column=1, sticky="w")
        self.phone_entry = tk.Entry(
            self,
            validate="focusout",
            validatecommand=(self.register(self.validate_phone), "%P"),
        )
        self.phone_entry.grid(row=6, column=1, sticky="ew")

        ttk.Label(self, text="Subscription:").grid(row=7, column=1, sticky="w")
        self.subscription_combobox = ttk.Combobox(self, values=["Annual", "Monthly"])
        self.subscription_combobox.grid(row=8, column=1, sticky="ew")

        # Create the Add button
        self.add_btn = ttk.Button(self, text="Add Member", command=self.add)
        self.add_btn.grid(row=10, column=1, pady=50, sticky="ew", columnspan=1)

    def validate_name(self, name):
        if len(name.strip()) == 0:
            messagebox.showerror("Invalid Input", "Name cannot be empty!")
            return False
        return True

    def validate_email(self, email):
        if "@" not in email or "." not in email.split("@")[-1]:
            messagebox.showerror("Invalid Input", "Please enter a valid email!")
            return False
        return True

    def validate_phone(self, phone):
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Invalid Input", "Phone number must be 10 digits!")
            return False
        return True

    def add(self):
        # Validate all fields before proceeding
        if (
            not self.validate_name(self.name_entry.get())
            or not self.validate_email(self.email_entry.get())
            or not self.validate_phone(self.phone_entry.get())
        ):
            return

        # Disable the button
        self.add_btn.config(state="disabled")

        # Schedule re-enabling the button after 2 seconds
        self.after(2000, self.enable_button)

    def enable_button(self):
        # Re-enable the button
        self.add_btn.config(state="normal")


# Usage example (if running standalone)
if __name__ == "__main__":
    root = tk.Tk()
    app = AddMember()
    root.mainloop()
