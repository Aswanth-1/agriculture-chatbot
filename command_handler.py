import re

from agriculture_data import crop_status, fertilizer, soil_info, tips, weather_updates
from utils import current_time, random_response

IRRIGATION_UPDATES = [
    "Irrigation system active.",
    "Water supply normal.",
    "Irrigation scheduled for evening.",
]

TOPIC_DISPLAY_NAMES = {
    "crop": "Crop status",
    "soil": "Soil status",
    "fertilizer": "Fertilizer",
    "weather": "Weather",
    "irrigation": "Irrigation",
    "tip": "Tip",
    "time": "Time",
    "history": "History",
}

QUICK_ACTION_ORDER = (
    "crop",
    "soil",
    "fertilizer",
    "weather",
    "irrigation",
    "tip",
    "time",
    "history",
)

TOPIC_KEYWORDS = (
    ("history", frozenset({"history"})),
    ("crop", frozenset({"crop", "crops"})),
    ("soil", frozenset({"soil", "soils"})),
    ("fertilizer", frozenset({"fertilizer", "fertilizers", "compost", "manure"})),
    ("weather", frozenset({"weather", "forecast", "rain", "temperature"})),
    ("tip", frozenset({"tip", "tips", "advice"})),
    ("irrigation", frozenset({"irrigation", "irrigate", "water", "watering"})),
    ("time", frozenset({"time", "clock"})),
)

def _format_section(title, data):
    lines = [title]

    for label, value in data.items():
        formatted_label = str(label).replace("_", " ")
        lines.append(f"- {formatted_label}: {value}")

    return "\n".join(lines)


def _format_history(command_history):
    if not command_history:
        return "Command History:\n- No commands yet."

    lines = ["Command History:"]

    for index, command in enumerate(command_history, start=1):
        lines.append(f"{index}. {command}")

    return "\n".join(lines)


def get_help_text():
    lines = ["Available Commands", "- Help"]
    lines.extend(f"- {TOPIC_DISPLAY_NAMES[topic]}" for topic in QUICK_ACTION_ORDER)
    lines.append("- Exit")
    return "\n".join(lines)


def get_quick_actions():
    return ["Help", *(TOPIC_DISPLAY_NAMES[topic] for topic in QUICK_ACTION_ORDER)]


def _contains_word(user_input, *words):
    return any(re.search(rf"\b{re.escape(word)}\b", user_input) for word in words)


def _extract_words(user_input):
    return set(re.findall(r"[a-z]+", user_input))


def should_exit(user_input):
    return _contains_word((user_input or "").lower(), "exit", "quit")


def get_welcome_message():
    return (
        "Welcome to the AgriFlow Assistant.\n"
        "Ask about crop status, soil, fertilizer, irrigation, weather, farming tips, time, or history. "
        "You can type your own question or use the suggested prompts to get started."
    )


def build_welcome_payload():
    return {
        "title": "AgriFlow Assistant",
        "message": get_welcome_message(),
        "quick_actions": get_quick_actions(),
    }


def _get_response_by_topic(topic, command_history):
    if topic == "history":
        return _format_history(command_history)

    if topic == "crop":
        return _format_section("Crop Status:", crop_status)

    if topic == "soil":
        return _format_section("Soil Information:", soil_info)

    if topic == "fertilizer":
        return _format_section("Fertilizer Recommendation:", fertilizer)

    if topic == "weather":
        return f"Weather Update: {random_response(weather_updates)}"

    if topic == "tip":
        return f"Agriculture Tip: {random_response(tips)}"

    if topic == "irrigation":
        return random_response(IRRIGATION_UPDATES)

    if topic == "time":
        return f"Current Time: {current_time()}"

    return None


def _detect_topic(user_input):
    words = _extract_words(user_input)

    for topic, keywords in TOPIC_KEYWORDS:
        if words.intersection(keywords):
            return topic

    return None


def _history_before_current_command(command_history, normalized_input, detected_topic):
    if detected_topic != "history" or not command_history:
        return command_history

    last_command = str(command_history[-1]).strip().lower()

    if last_command == normalized_input:
        return command_history[:-1]

    return command_history


def get_bot_response(user_input, command_history=None):
    normalized_input = (user_input or "").strip().lower()
    command_history = list(command_history or [])

    if not normalized_input:
        return "Please type a question so I can help with your farm update."

    if _contains_word(normalized_input, "help", "assist", "guide"):
        return get_help_text()

    if should_exit(normalized_input):
        return "Thank you for using the Agriculture Chatbot."

    detected_topic = _detect_topic(normalized_input)

    if detected_topic:
        history_for_response = _history_before_current_command(command_history, normalized_input, detected_topic)
        return _get_response_by_topic(detected_topic, history_for_response)

    return "Command not recognized. Try 'help' to see what you can ask."


def handle_command(user_input, command_history=None):
    return get_bot_response(user_input, command_history)
