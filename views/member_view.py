from random import randint

import tkinter as tk
import os
from tkinter.ttk import Style, Treeview
from PIL import Image, ImageTk
from utils.widgets import createButton, createLabel
from files.add_member import AddMember

members = [
    (
        2,
        "Jane Smith",
        "jane.smith@example.com",
        "234-567-8901",
        "Annual",
        "Inactive",
        "2022-06-15",
    ),
    (
        3,
        "Mike Johnson",
        "mike.johnson@example.com",
        "345-678-9012",
        "Monthly",
        "Active",
        "2023-03-22",
    ),
    (
        4,
        "Emily Davis",
        "emily.davis@example.com",
        "456-789-0123",
        "Annual",
        "Active",
        "2021-11-05",
    ),
    (
        5,
        "Chris Brown",
        "chris.brown@example.com",
        "567-890-1234",
        "Monthly",
        "Inactive",
        "2022-12-10",
    ),
    (
        6,
        "Katie Wilson",
        "katie.wilson@example.com",
        "678-901-2345",
        "Annual",
        "Active",
        "2020-09-12",
    ),
    (
        7,
        "David Miller",
        "david.miller@example.com",
        "789-012-3456",
        "Monthly",
        "Inactive",
        "2023-08-01",
    ),
    (
        8,
        "Sarah Lee",
        "sarah.lee@example.com",
        "890-123-4567",
        "Monthly",
        "Active",
        "2023-05-18",
    ),
    (
        9,
        "Daniel Moore",
        "daniel.moore@example.com",
        "901-234-5678",
        "Annual",
        "Active",
        "2022-02-20",
    ),
    (
        10,
        "Laura White",
        "laura.white@example.com",
        "012-345-6789",
        "Monthly",
        "Inactive",
        "2023-07-30",
    ),
    (
        11,
        "James Black",
        "james.black@example.com",
        "123-456-7890",
        "Annual",
        "Active",
        "2023-04-10",
    ),
    (
        12,
        "Sophia Green",
        "sophia.green@example.com",
        "234-567-8901",
        "Monthly",
        "Inactive",
        "2021-10-25",
    ),
    (
        13,
        "Andrew King",
        "andrew.king@example.com",
        "345-678-9012",
        "Monthly",
        "Active",
        "2023-09-17",
    ),
    (
        2,
        "Jane Smith",
        "jane.smith@example.com",
        "234-567-8901",
        "Annual",
        "Inactive",
        "2022-06-15",
    ),
    (
        3,
        "Mike Johnson",
        "mike.johnson@example.com",
        "345-678-9012",
        "Monthly",
        "Active",
        "2023-03-22",
    ),
    (
        4,
        "Emily Davis",
        "emily.davis@example.com",
        "456-789-0123",
        "Annual",
        "Active",
        "2021-11-05",
    ),
    (
        14,
        "Olivia Hall",
        "olivia.hall@example.com",
        "456-789-0123",
        "Annual",
        "Active",
        "2022-01-08",
    ),
    (
        15,
        "Matthew Scott",
        "matthew.scott@example.com",
        "567-890-1234",
        "Monthly",
        "Inactive",
        "2020-12-14",
    ),
    (
        16,
        "Ava Young",
        "ava.young@example.com",
        "678-901-2345",
        "Annual",
        "Active",
        "2023-06-02",
    ),
    (
        17,
        "Michael Adams",
        "michael.adams@example.com",
        "789-012-3456",
        "Monthly",
        "Active",
        "2021-03-29",
    ),
    (
        18,
        "Ella Collins",
        "ella.collins@example.com",
        "890-123-4567",
        "Annual",
        "Inactive",
        "2023-09-12",
    ),
    (
        19,
        "Liam Turner",
        "liam.turner@example.com",
        "901-234-5678",
        "Monthly",
        "Active",
        "2023-11-03",
    ),
    (
        20,
        "Charlotte Lewis",
        "charlotte.lewis@example.com",
        "012-345-6789",
        "Annual",
        "Active",
        "2020-05-20",
    ),
]


class MembersView(tk.Frame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        # initialization
        self.controller = controller
        self.db = db
        self.limit = 2
        self.offset = 1
        self.current_page = 1
        self.paginated_members = []
        self.show_dots = False
        self.has_prev = False
        self.has_next = False
        self.total_buttons = 1
        self._config_row_column()
        self._paginate()

        self.create_ui()

    def create_ui(self):
        # Add members table and search bar here
        image_path = os.path.join(os.getcwd(), "asset/arrow.png")
        image = Image.open(image_path)

        image = image.resize((20, 20))
        self.arrow_photo = ImageTk.PhotoImage(image)

        createButton(
            self,
            text="Back",
            image=self.arrow_photo,
            command=lambda: self.controller.show_frame("Dashboard"),
        ).grid(row=1, column=0, sticky="ew")

        self.search_entry = tk.Entry(
            self,
            cursor="hand2",
            font=("Arial", 12),
            relief="groove",
            bg="#ffffff",
            fg="#000000",
        )

        self.search_entry.grid(row=2, column=1, sticky="ew", padx=(10, 0))
        self.search_entry.insert(0, "Search Members...")
        self.search_entry.bind(
            "<FocusIn>", lambda event: self.search_entry.delete(0, "end")
        )

        self.search_entry.bind("<FocusOut>", lambda event: self.insert_placeholder())

        self.search_entry.bind("<KeyRelease>", self.search)

        createLabel(self, "From:").grid(row=2, column=3, sticky="ew")
        self.from_date_entry = tk.Entry(self)
        self.from_date_entry.insert(0, "2020-09-01")
        self.from_date_entry.grid(row=2, column=4, sticky="ew", padx=(10, 0))

        createLabel(self, "To:").grid(row=2, column=5, sticky="ew")
        self.to_date_entry = tk.Entry(self)
        self.to_date_entry.insert(0, "2020-09-01")
        self.to_date_entry.grid(row=2, column=6, sticky="ew", padx=(10, 0))

        # adding members
        createButton(self, "Add member", command=lambda: AddMember(self.db)).grid(
            row=3, column=1, sticky="w"
        )

        tree_scroll = tk.Scrollbar(
            self,
            orient="vertical",
        )
        tree_scroll.grid(row=4, column=8, sticky="ns")
        columns = [
            "Id",
            "Name",
            "Email",
            "Phone",
            "Subscription",
            "Status",
            "Activation Date",
        ]
        # Add members table here
        self.treeview = Treeview(
            self,
            selectmode="browse",
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll.set,
        )
        self.treeview.heading("Id", text="Id", anchor="center")
        self.treeview.heading("Name", text="Name", anchor="center")
        self.treeview.heading("Email", text="Email", anchor="center")
        self.treeview.heading("Phone", text="Phone", anchor="center")

        self.treeview.heading("Subscription", text="Subscription", anchor="center")

        self.treeview.heading("Status", text="Status", anchor="center")
        self.treeview.heading(
            "Activation Date", text="Activation date", anchor="center"
        )
        for col in columns:
            self.treeview.column(col, anchor="center")  # Center the content

        for member in self.paginated_members:
            self.treeview.insert("", "end", values=member)
            tree_scroll.config(command=self.treeview.yview)
            style = Style()
            style.map(
                "Treeview",
                background=[("selected", "green")],
                foreground=[("selected", "white")],
            )

            self.treeview.grid(row=4, column=1, columnspan=7, sticky="nsew")

            # pagination button
            self.create_page_numbers()

    def create_page_numbers(self):
        total_records = len(members)
        self.total_buttons = total_records // self.limit
        if total_records % self.limit != 0:
            self.total_buttons += 1

        self.max_display_buttons = 7  # Show up to 7 buttons with dots
        self.row_frame = tk.Frame(self)
        self.row_frame.grid(row=5, column=1, sticky="ew")

        createLabel(self.row_frame, text="Page:").grid(row=0, column=0, sticky="ew")

        # Previous button
        self.prev_button = tk.Button(
            self.row_frame,
            text="Prev",
            command=self.prev_page,
        )
        self.prev_button.grid(row=0, column=1, padx=(5, 0))

        # Determine which buttons to display
        button_to_display = self.get_display_buttons(self.max_display_buttons)
        self._create_buttons()

        # Next button
        self.next_button = tk.Button(
            self.row_frame,
            text="Next",
            command=self.next_page,
        )
        self.next_button.grid(row=0, column=len(button_to_display) + 2, padx=(5, 0))
        self._update_page_button_state()

    def _create_buttons(
        self,
    ):
        button_to_display = self.get_display_buttons(self.max_display_buttons)
        self.sub_row = tk.Frame(self.row_frame)
        self.sub_row.grid(row=0, column=2, sticky="ew")
        # Display page buttons
        for i, page in enumerate(button_to_display):
            if page == "...":
                createLabel(self.sub_row, text="...").grid(
                    row=0, column=i + 2, padx=(5, 0)
                )
            else:
                button = createButton(
                    self.sub_row,
                    text=f"{page}",
                    state="active" if page == self.current_page else "normal",
                )
                button.grid(row=0, column=i + 2, padx=(5, 0))
                button.bind(
                    "<Button-1>",
                    lambda event, page=page: self.change_page(page),
                )

    def get_display_buttons(self, max_display_buttons):
        """Returns a list of page numbers (with ellipses) to display."""
        pages = []
        total_buttons = self.total_buttons

        # Always show the first and last page
        if total_buttons <= max_display_buttons:
            pages = list(range(1, total_buttons + 1))
        else:
            pages = [1]

            if self.current_page > 4:
                pages.append("...")

            # Show up to two pages before and after the current page
            start_page = max(2, self.current_page - 2)
            end_page = min(total_buttons - 1, self.current_page + 2)

            pages.extend(range(start_page, end_page + 1))

            if self.current_page < total_buttons - 3:
                pages.append("...")

            pages.append(total_buttons)

        return pages

    def prev_page(self):
        if self.current_page > 1:
            self.change_page(self.current_page - 1)

    def next_page(self):
        if self.current_page < self.total_buttons:
            self.change_page(self.current_page + 1)

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

    def _paginate(self):
        end = self.current_page * self.limit
        start = self.offset

        self.paginated_members = members[start:end]

    def change_page(self, page):
        self.current_page = page
        self.offset = (page - 1) * self.limit

        # destoying previuos button pagination
        self.sub_row.destroy()
        self._update_page_button_state()
        self._create_buttons()
        self._paginate()
        self._update_table()

    def _update_table(self):
        self.treeview.delete(*self.treeview.get_children())
        for member in self.paginated_members:
            self.treeview.insert("", "end", values=member)

    def insert_placeholder(self):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, "Search Members...")

    def search(self, event):
        pass  # Implement search functionality here

    def _config_row_column(self):
        for i in range(2, 10):
            self.grid_rowconfigure(i, weight=1)
        for i in range(1, 14):
            self.grid_columnconfigure(i, weight=1)
