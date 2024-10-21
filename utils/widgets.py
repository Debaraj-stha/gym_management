from tkinter import Button, Label
from typing import Literal


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
