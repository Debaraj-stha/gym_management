import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox, Frame

from utils.widgets import createButton, createLabel

instructors = [
    "Manish BAsnet",
    "Deepa Dhakal",
    "Sandeep Bohora",
    "Rahjesh Tamang",
    "Sanjeeta Shrestha",
    "A",
    "B",
    "Jhon",
    "Michel",
    "Jhon Doe",
    "Alex",
]


class AddOrUpdateDetailClass(tk.Toplevel):
    def __init__(self, db, old_value: tuple = None, record_id: int = None, *args):

        super().__init__()
        self._is_update = record_id is not None
        self.title("Update Class Details" if self._is_update else "Add Class Details")
        self.geometry("500x600")
        self.config(padx=10, pady=10)
        self.resizable(False, False)
        self.d_b = db
        self._old_value = old_value if self._is_update else [" "] * 6
        self._record_id = record_id
        self.combobox = None
        self.entry = None
        self.label_text = None
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.create_widgets()

    def create_widgets(self):
        createLabel(self, "Date:").grid(row=1, column=1, sticky="w")
        self.date_box = Combobox(self, values=[1, 2, 3])
        self.date_box.grid(row=1, column=2, sticky="nsew")

        self.date_box.set(self._old_value[0] if self._is_update else 1)

        createLabel(self, "Duration:").grid(row=2, column=1, sticky="w", pady=10)
        self.duration_box = Combobox(self, values=["1 hour", "2 hours", "3 hours"])
        self.duration_box.grid(row=2, column=2, sticky="nsew", pady=10)
        self.duration_box.set(self._old_value[1] if self._is_update else "1 hour")

        createLabel(self, "Shift:").grid(row=3, column=1, sticky="w", pady=10)
        self.shift_box = Combobox(self, values=["Morning", "Day", "Evening", "Night"])
        self.shift_box.grid(row=3, column=2, sticky="nsew", pady=10)
        self.shift_box.set(self._old_value[2] if self._is_update else "Morning")

        createLabel(self, "Instructor:").grid(row=4, column=1, sticky="w", pady=10)

        # Create a Frame to hold the Listbox and Scrollbar
        listbox_frame = Frame(self)
        listbox_frame.grid(row=4, column=2, sticky="nsew", pady=10)

        self.instructor = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE)
        scrollbar = tk.Scrollbar(
            listbox_frame, orient="vertical", command=self.instructor.yview
        )
        self.instructor.config(yscrollcommand=scrollbar.set)

        for instructor in instructors:
            self.instructor.insert("end", instructor)

        # Pack the Listbox and Scrollbar in the Frame
        self.instructor.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        createLabel(self, "Status:").grid(row=5, column=1, sticky="w", pady=10)
        self.status = Combobox(self, values=["Available", "Full", "Not Available"])
        self.status.grid(row=5, column=2, sticky="nsew", pady=10)
        self.status.set(self._old_value[4] if self._is_update else "Available")

        createLabel(self, "Available spot:").grid(row=6, column=1, sticky="w", pady=10)
        self.entry = tk.Entry(self)
        self.entry.grid(row=6, column=2, sticky="nsew", pady=10)
        self.entry.insert(0, self._old_value[5])

        createButton(
            self,
            "Update" if self._record_id is not None else "Add",
            command=self._process,
        ).grid(row=8, column=2, sticky="nsew", pady=20)

    def _process(self):
        try:
            date, duration, shift, status, available_spot, instructors = (
                self._get_values()
            )
            if self._is_update:
                self.d_b.update_class_details(
                    self._record_id,
                    date,
                    duration,
                    shift,
                    status,
                    available_spot,
                    instructors,
                )
                messagebox.showinfo("Success", "Class details updated successfully")
            else:
                self.d_b.add_class_details(
                    date, duration, shift, status, available_spot, instructors
                )
                messagebox.showinfo("Success", "Class details added successfully")
        except Exception as e:
            print(f"An error occurred while processing the form: {e}")
            messagebox.showerror("Error", "An error occurred while processing the form")

    def _get_values(self):
        """
        Get the values from the widgets and validate them.

        Returns:
            tuple: Date, Duration, Shift, Status, Available spot, Selected instructors
        """
        try:
            selected_instructors_id = self.instructor.curselection()
            date = self.date_box.get()
            if date == " ":
                messagebox.showerror("Validation Error", "Date must be filled out")
                return None
            duration = self.duration_box.get()
            if duration == " ":
                messagebox.showerror("Validation Error", "Duration must be filled out")
                return None
            shift = self.shift_box.get()
            if shift == " ":
                messagebox.showerror("Validation Error", "Shift must be filled out")
                return None
            status = self.status.get()
            if status == " ":
                messagebox.showerror("Validation Error", "Status must be filled out")
                return None
            available_spot = self.entry.get()
            if not available_spot.isdigit() or int(available_spot) < 0:
                messagebox.showerror(
                    "Validation Error", "Available spot must be a positive integer"
                )
                return None
            selected_instructors = [instructors[id] for id in selected_instructors_id]
            return (date, duration, shift, status, available_spot, selected_instructors)
        except Exception as e:
            print(f"An error occurred while getting values: {e}")
            return None
