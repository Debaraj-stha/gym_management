from operator import sub
from tkinter import Button, Label, Frame
from PIL import Image, ImageTk
from typing import Literal
import os

max_display_buttons = 7


def createButton(
    frame,
    text,
    height=0,
    width=0,
    command=lambda: print("clicked"),
    relief: Literal["flat", "groove", "raised", "ridge", "solid", "sunken"] = "groove",
    borderwidth=1,
    highlightthickness=1,
    fontfamily="Arial",
    fontsize=12,
    image=None,
    state="normal",
):
    button = Button(
        frame,
        text=text,
        image=image,
        height=height,
        width=width,
        command=command,
        cursor="hand2",
        font=(fontfamily, fontsize),
        # bg=bg,
        relief=relief,
        borderwidth=borderwidth,
        highlightthickness=highlightthickness,
        compound="left",
        state=state,
    )
    return button


def createLabel(
    frame,
    text,
    fontfamily="Arial",
    fontsize=12,
    fg="#000",
):
    label = Label(frame, text=text, font=(fontfamily, fontsize), fg=fg)
    return label


def backButton(frame, controller):
    print("clicked")
    image_path = os.path.join(os.getcwd(), "asset/arrow.png")
    image = Image.open(image_path)
    image = image.resize((20, 20))

    # Create a persistent reference for the image
    frame.arrow_photo = ImageTk.PhotoImage(image)

    createButton(
        frame,
        text="Back",
        image=frame.arrow_photo,
        command=lambda: controller.show_frame("Dashboard"),
    ).grid(row=0, column=0, sticky="ew")


def create_page_numbers(
    total_records, row_frame, change_page, limit=10, current_page=1, row_index=6
):
    """
    generate  and display pages
    Args:
        total_records (int): numbers of record
        row_frame (Frame): a frame window
        change_page (function): A functin to handle page change functionality
        limit (int, optional): how many item to fetch per page. Defaults to 10.
        current_page (int, optional): the current active page. Defaults to 1.

    Returns:
    tuple: (sub_row, total_buttons, prev_button, next_button)
    """
    total_buttons = total_records // limit
    if total_records % limit != 0:
        total_buttons += 1
    row_frame.grid(row=row_index, column=0, sticky="ew")

    createLabel(row_frame, text="Page:").grid(row=0, column=0, sticky="ew")

    # Previous button
    prev_button = Button(
        row_frame,
        text="Prev",
        # command=prev_page,
    )
    prev_button.grid(row=0, column=1, padx=(5, 0))

    # Determine which buttons to display
    button_to_display = get_display_buttons(current_page, total_buttons)
    sub_row = create_buttons(row_frame, current_page, total_buttons, change_page)

    # Next button
    next_button = Button(
        row_frame,
        text="Next",
        # command=next_page,
    )
    next_button.grid(row=0, column=len(button_to_display) + 2, padx=(5, 0))
    # _update_page_button_state()
    return sub_row, total_buttons, prev_button, next_button


def create_buttons(row_frame, current_page, total_button, change_page):
    print(f"current page:{current_page}")
    button_to_display = get_display_buttons(current_page, total_button)
    sub_row = Frame(row_frame)
    sub_row.grid(row=0, column=2, sticky="w")
    # Display page buttons
    for i, page in enumerate(button_to_display):
        if page == "...":
            createLabel(sub_row, text="...").grid(row=0, column=i + 2, padx=(5, 0))
        else:
            button = createButton(
                sub_row,
                text=f"{page}",
                state="active" if page == current_page else "normal",
            )
            button.grid(row=0, column=i + 2, padx=(5, 0))
            button.bind(
                "<Button-1>",
                lambda event, page=page: change_page(page),
            )
    return sub_row


def get_display_buttons(current_page, total_buttons):
    """Returns a list of page numbers (with ellipses) to display."""
    pages = []

    # Always show the first and last page
    if total_buttons <= max_display_buttons:
        pages = list(range(1, total_buttons + 1))
    else:
        pages = [1]

        if current_page > 4:
            pages.append("...")

        # Show up to two pages before and after the current page
        start_page = max(2, current_page - 2)
        end_page = min(total_buttons - 1, current_page + 2)

        pages.extend(range(start_page, end_page + 1))

        if current_page < total_buttons - 3:
            pages.append("...")

        pages.append(total_buttons)

    return pages
