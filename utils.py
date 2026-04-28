import datetime
import random


def random_response(data):
    # just picks a random item from the list
    index = random.randint(0, len(data) - 1)
    return data[index]


def current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def print_console(text=""):
    # print to terminal
    try:
        print(text)
    except UnicodeEncodeError:
        # some terminals don't support special characters
        cleaned = text.encode("ascii", "ignore").decode("ascii")
        print(cleaned)


def console_input(prompt=""):
    # get input from user
    try:
        return input(prompt)
    except UnicodeEncodeError:
        cleaned = prompt.encode("ascii", "ignore").decode("ascii")
        return input(cleaned)


def configure_console():
    # nothing special needed for most systems
    pass


def greet_user(name):
    print_console(f"\nHello {name}! Welcome to the Agriculture Chatbot.")
