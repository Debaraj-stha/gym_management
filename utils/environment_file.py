from dotenv import set_key
import os

env_path = ".env"


def set_env(key, value):
    """
    set environment variable value
    Args:
        key (string): key of the environment variable
        value (string): value of the environment variable
    """

    set_key(env_path, key, value)


def get_env(key):
    """
    get environment variable value
    Args:
        key (string): key of the environment variable
    Returns:
        string: value of the environment variable
    """
    try:
        return os.getenv(key)
    except Exception as e:
        print(f"Error in getting environment variable: {e}")
        return None
