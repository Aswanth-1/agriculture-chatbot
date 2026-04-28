from command_handler import get_bot_response, should_exit
from utils import print_console, console_input, greet_user, configure_console


def main():
    configure_console()

    print_console("====================================")
    print_console("  Agriculture Chatbot")
    print_console("====================================")

    name = console_input("Enter your name: ").strip()
    if name == "":
        name = "Farmer"

    greet_user(name)
    print_console("Type 'help' to see available commands.")

    # keep track of what the user typed
    command_history = []

    # main loop - keeps running until user types exit
    while True:
        user_input = console_input("\nYou: ").strip()

        if user_input == "":
            continue

        response = get_bot_response(user_input, command_history)
        print_console("\nBot: " + response)

        command_history.append(user_input)

        if should_exit(user_input):
            break


if __name__ == "__main__":
    main()
