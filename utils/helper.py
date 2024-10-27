from tkinter import Entry

import smtplib

from utils.environment_file import get_env
from .logger import logger


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
