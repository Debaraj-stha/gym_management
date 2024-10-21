
# Gym Management Software

Gym Management Software is a desktop application developed using Python's Tkinter framework. It allows gym administrators to manage their gym's operations such as tracking members, managing attendance, handling billing, and scheduling classes. The software also includes a theme-switching feature, enabling users to switch between light and dark modes.

## Features

- **Member Management**: Add, update, and remove gym members.
- **Attendance Tracking**: Track member attendance and generate reports.
- **Billing System**: Manage membership fees, payments, and generate bills.
- **Report**: Reporting of member subscription expiration.
- **Class Scheduling**: Schedule gym classes and manage bookings.
- **Theme Support**: Switch between light and dark themes (Forest Light and Forest Dark themes).
- **Customization**: Settings page to update background color, language, and other preferences.
- **Localization**: Support for localization in Nepali, Spanish, French, English, and Hindi.

## Screenshots

### Dashboard

![Dashboard Screenshot](screenshots/dashboard.png)

### Member Management

![Members Screenshot](screenshots/members.png)

### Attendance Tracking

![Attendance Screenshot](screenshots/attendance.png)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Debaraj-stha/gym_management.git
   cd gym-management
   ```

2. **Set up the virtual environment**:

   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```

   - Activate the virtual environment:
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

   - Install the required dependencies using pip:
     ```bash
     pip install -r requirements.txt
     ```

3. **Set up environment variables**:

   - Create a `.env` file in the root directory with the following contents:
     ```
     THEME=forest-dark
     BACKGROUND_COLOR=#d4d4d4
     LANGUAGE=en
     ```

4. **Run the application**:
   ```bash
   python app.py
   ```

## Usage

- Use the **Dashboard** to get an overview of the gym’s performance.
- **Manage members** by adding, editing, and deleting member records.
- Track **attendance** of members and generate reports for review.
- Handle **billing** and membership payments through the billing section.
- **Schedule classes** for different workouts and manage bookings.
- Switch between **light** and **dark** themes using the theme switch buttons at the top of the application.

## Customization

### Themes

- You can customize the themes by modifying or adding `.tcl` files in the `theme` directory.
- The default themes are **forest-dark** and **forest-light**.

### Environment Variables

- **THEME**: Sets the initial theme of the application.
- **BACKGROUND_COLOR**: Sets the background color of the application.
- **LANGUAGE**: Set the language for localization.

## License

This project is licensed under the MIT License.
