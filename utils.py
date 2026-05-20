import datetime
import random


def random_response(data):
    # just picks a random item from the list
    index = random.randint(0, len(data) - 1)
    return data[index]


def current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def supports_unicode_output(stream):
    encoding = getattr(stream, "encoding", "") or ""
    return "utf" in encoding.lower()


def to_console_text(text, stream):
    if supports_unicode_output(stream):
        return text

    cleaned = text.replace("â€“", "-").replace("–", "-").replace("—", "-")
    return cleaned.encode("ascii", "ignore").decode("ascii")


def print_console(text=""):
    # print to terminal
    import sys

    print(to_console_text(text, sys.stdout))


def console_input(prompt=""):
    # get input from user
    import sys

    return input(to_console_text(prompt, sys.stdout))


def configure_console():
    # nothing special needed for most systems
    pass


def greet_user(name):
    print_console(f"\nHello {name}! Welcome to the Agriculture Chatbot.")
