import datetime
import random
import sys

CONSOLE_REPLACEMENTS = str.maketrans(
    {
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00a0": " ",
    }
)

def random_response(data):
    return random.choice(data)

def current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _get_stream_encoding(stream):
    return (getattr(stream, "encoding", None) or "").lower()


def supports_unicode_output(stream=None):
    encoding = _get_stream_encoding(stream or sys.stdout)
    return encoding.startswith("utf") or encoding == "cp65001"


def configure_console():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(errors="replace")
            except ValueError:
                continue


def to_console_text(text, stream=None):
    normalized = str(text).translate(CONSOLE_REPLACEMENTS)

    if supports_unicode_output(stream):
        return normalized

    return normalized.encode("ascii", "ignore").decode("ascii")


def print_console(text="", end="\n"):
    print(to_console_text(text), end=end)


def console_input(prompt=""):
    return input(to_console_text(prompt))


def greet_user(name):
    print_console(f"\nHello {name}! Welcome to the Agriculture Chatbot 🌾")
