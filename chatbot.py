from command_handler import get_bot_response, should_exit
from utils import configure_console, console_input, greet_user, print_console

BANNER = """====================================
  🌾 Natural Language Agriculture Bot 🌾
===================================="""


def main():
    configure_console()
    print_console(BANNER)

    name = console_input("👤 Enter your name: ").strip() or "Farmer"
    greet_user(name)

    command_history = []

    while True:
        user_input = console_input("\n💬 You: ").strip().lower()

        response = get_bot_response(user_input, command_history)
        print_console(f"\n{response}")

        if user_input:
            command_history.append(user_input)

        if should_exit(user_input):
            break


if __name__ == "__main__":
    main()
