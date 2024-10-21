# Gym Management Software

This is a Gym Management System developed using Python and Tkinter. The application is designed to manage members, track attendance, handle membership billing, schedule gym classes, and generate reports.

## Features

- **Member Management**: Add, update, and remove gym members.
- **Attendance Tracking**: Record daily attendance of members.
- **Membership Plans**: Manage different membership plans (monthly, yearly, etc.).
- **Billing and Payments**: Generate invoices and track payments.
- **Class Scheduling**: Manage fitness class schedules and attendance.
- **Reports**: Generate reports related to memberships, attendance, and payments.
- **Localization**: Multilingual support (English, Spanish).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/gym-management.git
   cd gym-management

    Set up a virtual environment:

        On Windows:

        bash
   ```

python -m venv venv
venv\Scripts\activate

On macOS/Linux:

bash

    python3 -m venv venv
    source venv/bin/activate

Install dependencies:

bash

pip install -r requirements.txt

Run the application:

bash

python app.py

When finished, deactivate the virtual environment:

bash

    deactivate

Folder Structure

    app.py: Main entry point of the application.
    views/: Contains views for different sections of the gym management system (e.g., member management, attendance).
    files/: Functional modules like member management, billing, and attendance.
    utils/: Utility functions like database connections and data validation.
    config/: Configuration files (e.g., for database settings).
    database/: Contains the SQLite database file.
    locales/: Localization files for multilingual support.
    assets/: Static assets (e.g., images, icons).
    resources/: Resource files like styles and fonts.

Dependencies

    Tkinter: For GUI components.
    SQLite3: For database management.
    Babel: For localization.
    Pillow: For image handling.

Install these dependencies using pip install:

bash

pip install tkinter pillow babel

Usage

    Member Management: Use the "Members" section to add, update, or remove members. This includes basic details like name, contact information, and membership plan.

    Attendance: Use the "Attendance" section to mark members’ attendance for the day.

    Billing: Go to the "Billing" section to generate invoices, record payments, and manage outstanding balances.

    Class Scheduling: The "Class Schedule" section allows you to add, update, and remove fitness classes, and track members attending these classes.

    Reports: Generate reports on active memberships, attendance, payments, and more.

License

This project is licensed under the MIT License. See the LICENSE file for details.

yaml

---

By using a virtual environment, you ensure that your project's dependencies are isolated
