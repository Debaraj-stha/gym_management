import re
from tkinter import Entry, Frame

import smtplib
import os
import pandas as pd
import gettext

from utils.constraints import LANGUAGES
from utils.environment_file import get_env
from .logger import logger
from gettext import gettext as _


def focusIn(event):

    entry = event.widget
    if isinstance(entry, Entry):
        entry.delete(0, "end")


def focusOut(event, placeholder=None):
    """
    Placeholder for entry widget
    Args:
        event (Event): event object
        placeholder (string): placeholder text
    """
    entry = event.widget
    if isinstance(entry, Entry):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray")
            entry.bind("<FocusIn>", lambda event: focusIn(event))


def send_email(to, subject, message):
    """
    Send email using gmail account
    Args:
        to (string): recipient email address
        subject (string): email subject
        message (string): email content
    """
    gmail_user = get_env("EMAIL")
    gmail_password = get_env("PASSWORD")
    recipient = to
    msg = f"Subject: {subject}\n\n{message}"

    try:

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipient, msg)
        server.quit()
        logger.debug("emails sent successfully.")
        print("successfully sent emails")
        return True
    except Exception as e:
        logger.info(f"Error sending email:{e}")
        print("failed")
        return False


def config_grid_col(frame: Frame, col):
    """
    Configure grid columns
    Args:
        frame (Frame): grid container
        col (int): number of columns to configure
    """
    for i in range(col):
        frame.columnconfigure(i, weight=1)


def config_grid_row(frame: Frame, row):
    """
    Configure grid rows
    Args:
        frame (Frame): grid container
        row (int): number of rows to configure
    """

    for i in range(row):
        frame.rowconfigure(i, weight=1, pad=10)


def export_to_csv(data, filename: str, schema):
    try:
        # Fetch data to export

        print("Exporting to CSV")
        columns_name = get_table_column_name(schema)

        df = pd.DataFrame(data, columns=columns_name)

        # Define the target directory path within the current working directory
        directory = make_directory()
        # Define the complete file path
        file_path = os.path.join(directory, filename)

        # Save CSV file to the specified directory
        df.to_csv(file_path, index=False)

        print(f"CSV exported successfully to {file_path}")

    except Exception as e:
        print(f"An error occurred while exporting to CSV: {e}")


def make_directory(directory="data"):
    """ ""
    Define the target directory path within the current working directory
    """
    directory = os.path.join(os.getcwd(), directory)

    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def get_table_column_name(schema):
    """
    Extract table column names from the given schema
    """
    try:
        # Extract column names from the schema using regular expressions.
        columns = re.findall(r"(\w+)\s+\w+", schema)
        # Exclude system-defined columns such as PRIMARY, FOREIGN, DEFAULT, and REFERENCES from the list of column names.
        col = [
            col
            for col in columns
            if not col in ("PRIMARY", "FOREIGN", "DEFAULT", "REFERENCES")
        ]
        return col
    except Exception as e:
        print(f"An error occurred while fetching table column names: {e}")


def get_localization():
    try:
        language = get_env("LANGUAGE")
        print(language)
        code = LANGUAGES.get("Nepali")
        print(code)
        return code

    except Exception as e:
        print(f"An error occurred while fetching localization: {e}")
        return "en"


def collect_language_input():
    return _
