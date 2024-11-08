import tkinter as tk
from tkinter.ttk import Frame

from files.add_update_class_details import AddOrUpdateDetailClass
from utils.constraints import TABLENAME
from utils.widgets import backButton, createButton, createLabel


class ClassScheduleView(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.schedules = []
        self.limit = 10
        self.offset = 0
        self._get_schedules()
        self.create_ui()

    def _get_schedules(self):
        # Fetching all schedules from the database
        res = self.db.get_schedule(self.limit, self.offset)
        self.schedules = res
        print(res)

    def create_ui(self):
        # Configure the main frame columns
        self.grid_columnconfigure(0, weight=1)  # Align contents to the left side
        self.grid_columnconfigure(1, weight=1)

        # Toolbar frame for the "Add Class" button
        toolrow = tk.Frame(self)
        toolrow.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=10)

        # Content frame for the class schedule
        content_frame = Frame(self)
        content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)

        # Set column configuration only for the necessary columns (0 and 1)
        self._config_grid(toolrow, columns=2)
        backButton(toolrow, self.controller).grid(row=0, column=0, sticky="w", pady=10)

        # print(res)
        createButton(
            toolrow,
            "Add Class",
            state="active",
            command=lambda: AddOrUpdateDetailClass(self.db),
        ).grid(row=1, column=0, sticky="w")

        self._config_grid(content_frame, columns=2)

        # Class Schedule label aligned to the left
        createLabel(content_frame, "Class Schedule").grid(row=0, column=0, sticky="w")

        # Treeview for the schedule
        columns = [
            "Date",
            "Duration",
            "Shift",
            "Status",
            "Available spot",
            "Instructor",
        ]
        self.schedule_tree = tk.ttk.Treeview(
            content_frame, columns=columns, show="headings"
        )
        for column in columns:
            self.schedule_tree.heading(column, text=column, anchor="center")
            self.schedule_tree.column(column, anchor="center")
        self.schedule_tree.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Add dummy data to the Treeview
        for schedule in self.schedules:
            self.schedule_tree.insert(
                "",
                "end",
                values=(
                    schedule[1],
                    schedule[2],
                    schedule[3],
                    schedule[4],
                    schedule[5],
                    schedule[6],
                ),
            )
        # binding event to treeview
        self.schedule_tree.bind("<Double-Button-1>", self._on_treeview_double_click)

    def _on_treeview_double_click(self, event):
        try:
            selected_item = self.schedule_tree.selection()[0]

            if selected_item is None:
                return
            selected_item_values = self.schedule_tree.item(selected_item, "values")
            print(selected_item_values)
            AddOrUpdateDetailClass(self.db, selected_item_values, selected_item)

        except Exception as e:
            print(f"Error occurred: {e}")

    def _config_grid(self, frame: Frame, columns: int):
        # Configuring only the used columns to keep elements aligned
        for i in range(columns):
            frame.grid_columnconfigure(i, weight=1)

    def _config_grid(self, frame: Frame, columns: int):
        # Configuring only the used columns to keep elements aligned
        for i in range(columns):
            frame.grid_columnconfigure(i, weight=1)
