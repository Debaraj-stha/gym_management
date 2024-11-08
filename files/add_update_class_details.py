from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox, Frame

from utils.constraints import DURATIONS, SHIFTS, STATUS, TABLENAME
from utils.widgets import createButton, createLabel


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
        self.duration_box = Combobox(self, values=DURATIONS)
        self.duration_box.grid(row=2, column=2, sticky="nsew", pady=10)
        self.duration_box.set(self._old_value[1] if self._is_update else DURATIONS[0])

        createLabel(self, "Shift:").grid(row=3, column=1, sticky="w", pady=10)
        self.shift_box = Combobox(self, values=SHIFTS)
        self.shift_box.grid(row=3, column=2, sticky="nsew", pady=10)
        self.shift_box.set(self._old_value[2] if self._is_update else SHIFTS[0])

        createLabel(self, "Instructor:").grid(row=4, column=1, sticky="w", pady=10)

        # Create a Frame to hold the Listbox and Scrollbar
        listbox_frame = Frame(self)
        listbox_frame.grid(row=4, column=2, sticky="nsew", pady=10)

        self.instructor = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE)
        scrollbar = tk.Scrollbar(
            listbox_frame, orient="vertical", command=self.instructor.yview
        )
        self.instructor.config(yscrollcommand=scrollbar.set)
        self.instructors = self.d_b.get_all(
            columns_name=("id", "name"), table_name=TABLENAME.INSTRUCTORS.value
        )

        for id, instructor in self.instructors:
            self.instructor.insert("end", instructor)

        # Pack the Listbox and Scrollbar in the Frame
        self.instructor.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        createLabel(self, "Status:").grid(row=5, column=1, sticky="w", pady=10)
        self.status = Combobox(self, values=STATUS)
        self.status.grid(row=5, column=2, sticky="nsew", pady=10)
        self.status.set(self._old_value[4] if self._is_update else STATUS[0])

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
            columns_name = [
                "date",
                "duration",
                "shift",
                "status",
                "available_spots",
            ]
            data = (date, duration, shift, status, available_spot)

            if self._is_update:
                res = self.d_b.update(
                    columns_name,
                    data,
                    (self._record_id,),
                    table_name=TABLENAME.CLASS_SCHEDULE.value,
                    where_col=("id",),
                )
                if res is None:
                    messagebox.showerror("Error", f"Something went wrong:{res}")
                    return

                messagebox.showinfo("Success", "Class details updated successfully")
            else:

                res = self.d_b.insert(
                    data,
                    columns_name,
                    table_name=TABLENAME.CLASS_SCHEDULE.value,
                    instructors_id=instructors,
                )
                if res is None:
                    messagebox.showerror("Error", f"Something went wrong:{res}")
                    return
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
            selected_instructors_index = self.instructor.curselection()

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
            if available_spot == " ":
                available_spot = None
            else:
                if int(available_spot) < 0:
                    messagebox.showerror(
                        "Validation Error", "Available spot must be a positive integer"
                    )
                    return None
            selected_instructors_id = [
                self.instructors[id][0] for id in selected_instructors_index
            ]
            today = datetime.now().date().strftime("%Y-%m-%d")
            return (
                today,
                duration,
                shift,
                status,
                available_spot,
                selected_instructors_id,
            )
        except Exception as e:
            print(f"An error occurred while getting values: {e}")
            return None
