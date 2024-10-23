from tkinter import Entry


def focusIn(event):
    entry = event.widget
    if isinstance(entry, Entry):
        entry.delete(0, "end")


def focusOut(event, placeholder=None):
    entry = event.widget
    if isinstance(entry, Entry):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray")
            entry.bind("<FocusIn>", lambda event: focusIn(event))
