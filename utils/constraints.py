from enum import Enum


class TABLENAME(Enum):
    CUSTOMERS = "customers"
    INSTRUCTORS = "instructors"
    CLASS_SCHEDULE = "class_schedule"
    CLASS_SCHEDULE_INSTRUCTORS = "class_schedule_instructors"
    ATTENDANCE = "attendance"
    INVOICE = "invoice"


SHIFTS = ("morning", "day", "evening", "night")
DURATIONS = ("1 hour", "2 hours", "3 hours", "1.5 hours")
STATUS = ("available", "full")
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Nepali": "ne",
}
