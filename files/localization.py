import gettext
import os


def setup_translation(language_code="en"):
    global _
    locales_dir = os.path.join(os.getcwd(), "locales")
    print(locales_dir)
    lang = gettext.translation(
        "messages", localedir=locales_dir, languages=[language_code], fallback=True
    )
    lang.install()
    _ = lang.gettext
    return _
