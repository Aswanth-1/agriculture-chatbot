import datetime
import random

from agriculture_data import crop_status, soil_info, fertilizer, weather_updates, tips

# irrigation status messages
IRRIGATION_UPDATES = [
    "Irrigation system is running.",
    "Water supply is normal.",
    "Irrigation is scheduled for evening.",
]


def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_random(data):
    return random.choice(data)


def show_help():
    help_text = """Available Commands:
- help
- crop
- soil
- fertilizer
- weather
- irrigation
- tip
- time
- history
- exit"""
    return help_text


def show_crop_status():
    result = "Crop Status:\n"
    for crop, status in crop_status.items():
        result += f"- {crop}: {status}\n"
    return result


def show_soil_info():
    result = "Soil Information:\n"
    for key, info in soil_info.items():
        label = key.replace("_", " ")
        result += f"- {label}: {info}\n"
    return result


def show_fertilizer_info():
    result = "Fertilizer Recommendations:\n"
    for key, info in fertilizer.items():
        result += f"- {key}: {info}\n"
    return result


def show_history(history):
    if len(history) == 0:
        return "No commands entered yet."
    result = "Command History:\n"
    count = 1
    for cmd in history:
        result += f"{count}. {cmd}\n"
        count += 1
    return result


def get_welcome_message():
    msg = "Welcome to AgriFlow Assistant.\n"
    msg += "You can ask about crops, soil, fertilizer, weather, irrigation, tips, time or history.\n"
    msg += "Type help to see all commands."
    return msg


def build_welcome_payload():
    quick_actions = ["Help", "Crop status", "Soil status", "Fertilizer",
                     "Weather", "Irrigation", "Tip", "Time", "History"]
    return {
        "title": "AgriFlow Assistant",
        "message": get_welcome_message(),
        "quick_actions": quick_actions
    }


def detect_topic(user_input):
    # check what the user is asking about using simple keyword check
    words = user_input.lower().split()

    if "history" in words:
        return "history"

    if "crop" in words or "crops" in words:
        return "crop"

    if "soil" in words:
        return "soil"

    if "fertilizer" in words or "fertilizers" in words or "compost" in words or "manure" in words:
        return "fertilizer"

    if "weather" in words or "rain" in words or "temperature" in words or "forecast" in words:
        return "weather"

    if "tip" in words or "tips" in words or "advice" in words:
        return "tip"

    if "water" in words or "irrigation" in words or "irrigate" in words or "watering" in words:
        return "irrigation"

    if "time" in words or "clock" in words:
        return "time"

    return None


def get_bot_response(user_input, command_history=None):
    if command_history is None:
        command_history = []

    user_input = user_input.strip()

    if user_input == "":
        return "Please type something so I can help you."

    lower_input = user_input.lower()

    # check for help
    if "help" in lower_input or "assist" in lower_input or "guide" in lower_input:
        return show_help()

    # check for exit
    if "exit" in lower_input or "quit" in lower_input:
        return "Thank you for using the Agriculture Chatbot. Goodbye!"

    # detect topic and return response
    topic = detect_topic(lower_input)

    if topic == "crop":
        return show_crop_status()

    elif topic == "soil":
        return show_soil_info()

    elif topic == "fertilizer":
        return show_fertilizer_info()

    elif topic == "weather":
        return "Weather Update: " + get_random(weather_updates)

    elif topic == "tip":
        return "Farming Tip: " + get_random(tips)

    elif topic == "irrigation":
        return get_random(IRRIGATION_UPDATES)

    elif topic == "time":
        return "Current Time: " + get_current_time()

    elif topic == "history":
        return show_history(command_history)

    else:
        return "I did not understand that. Type 'help' to see what you can ask."


def should_exit(user_input):
    lower = user_input.lower()
    if "exit" in lower or "quit" in lower:
        return True
    return False


def handle_command(user_input, command_history=None):
    return get_bot_response(user_input, command_history)
