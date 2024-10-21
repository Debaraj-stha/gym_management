from tkinter import Button, Label
from typing import Literal


def createButton(
    frame,
    text,
    height=0,
    width=0,
    command=lambda x: print("clicked"),
    relief: Literal["flat", "groove", "raised", "ridge", "solid", "sunken"] = "groove",
    borderwidth=1,
    highlightthickness=1,
    fontfamily="Arial",
    fontsize=12,
):
    button = Button(
        frame,
        text=text,
        height=height,
        width=width,
        command=command,
        cursor="hand2",
        font=(fontfamily, fontsize),
        # bg=bg,
        relief=relief,
        borderwidth=borderwidth,
        highlightthickness=highlightthickness,
    )
    return button


def createLabel(
    frame,
    text,
    bg,
    fontfamily="Arial",
    fontsize=12,
    fg="#111",
):
    label = Label(frame, text=text, font=(fontfamily, fontsize), fg=fg, bg=bg)
    return label
