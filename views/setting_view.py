import tkinter as tk
from tkinter import Button, colorchooser
from tkinter.ttk import Combobox


from utils.constraints import LANGUAGES
from utils.environment_file import get_env, set_env
from utils.widgets import createButton, createLabel


class SettingView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Setting")
        self.geometry("550x600")
        self.config(padx=20, pady=20)
        self.bg = get_env("BACKGROUND_COLOR")
        self.configure(background=self.bg)

        # Configuring row layout
        # self.grid_rowconfigure(0, weight=1)  # Empty row for top padding
        # self.grid_rowconfigure(1, weight=1)  # Label row
        # self.grid_rowconfigure(2, weight=1)  # Combobox row
        # self.grid_rowconfigure(3, weight=1)  # Empty row for bottom padding

        # # Configuring column layout
        self.grid_columnconfigure(0, weight=1)  # Empty column at left
        self.grid_columnconfigure(1, weight=1)  # Column for label and combobox
        # self.grid_columnconfigure(2, weight=1)  # Empty column at right

        # Creating UI
        self.create_ui()

    def create_ui(self):
        # Language label
        label = createLabel(self, _("Language"), bg=self.bg)
        label.grid(row=1, column=1, sticky="nsew", pady=(10, 5), padx=10)

        # Language OptionMenu
        languages_list = list(LANGUAGES.keys())
        language_var = tk.StringVar()
        language_var.set(languages_list[0])  # Set default language

        self.languageBox = tk.OptionMenu(
            self, language_var, *languages_list, command=self.change_language
        )
        self.languageBox.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        ##background change button
        label = createLabel(self, _("Background"), bg=self.bg)
        label.grid(row=2, column=1, sticky="nsew", pady=(10, 5), padx=10)
        self.bg_change_button = Button(
            self,
            text=_("Change"),
            bg=self.bg,
            fg="#111",
            command=self.change_background,
        )
        self.bg_change_button.grid(row=2, column=2, sticky="nsew")
        label = createLabel(self, _("Notifications"), bg=self.bg)

        label.grid(row=3, column=1, sticky="nsew", pady=(10, 5), padx=10)

        self.notifications_var = tk.BooleanVar(value=True)  # Default enabled
        notification_check = tk.Checkbutton(
            self,
            text=_("Enable Notifications"),
            variable=self.notifications_var,
            command=self.toggle_notifications,
            bg=self.bg,
        )
        notification_check.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)
        label = createLabel(self, _("Theme"), bg=self.bg)
        label.grid(row=5, column=1, sticky="nsew", pady=(10, 5), padx=10)

        themes = [_("Light"), _("Dark")]
        theme_var = tk.StringVar(value=themes[0])  # Default to Light
        self.theme_box = tk.OptionMenu(
            self, theme_var, *themes, command=self.change_theme
        )
        self.theme_box.grid(row=5, column=2, sticky="nsew", padx=10, pady=10)

    def change_theme(self, theme):
        """Switch between light and dark themes."""
        print(f"Theme changed to: {theme}")
        theme_value = "forest-dark" if theme == "Dark" else "forest-light"

        set_env("THEME", theme_value)  # Update the environment variable
        self.parent.update_theme(theme_value)

    def change_language(self, language):
        """Handle language change action."""
        code = LANGUAGES.get(language)
        print(f"Language changed to: {language} ({code})")
        set_env("LANGUAGE", code)  # Update the environment variable

    def change_background(self):
        """Handle background change action."""
        color_code = colorchooser.askcolor(title="Choose Background Color")[1]
        if color_code:
            print(f"Background color changed to: {color_code}")
            self.configure(bg=color_code)
            self.bg_change_button.config(bg=color_code)
            # Update the environment variables
            set_env("BACKGROUND_COLOR", color_code)

    def toggle_notifications(self):
        """Enable/Disable notifications."""
        enabled = self.notifications_var.get()
        print(f"Notifications {'enabled' if enabled else 'disabled'}")
        set_env("NOTIFICATIONS", str(enabled))  # Update env settings
