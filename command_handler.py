import datetime
import random
import re

from agriculture_data import (
    crop_status,
    fertilizer,
    irrigation_updates,
    soil_info,
    tips,
    weather_updates,
)


STOP_WORDS = {
    "a",
    "about",
    "an",
    "and",
    "any",
    "are",
    "can",
    "do",
    "for",
    "give",
    "have",
    "how",
    "i",
    "in",
    "is",
    "me",
    "my",
    "of",
    "on",
    "please",
    "should",
    "tell",
    "the",
    "to",
    "what",
    "when",
    "with",
    "you",
}

AGRICULTURE_KEYWORDS = {
    "agriculture",
    "aphid",
    "aphids",
    "blight",
    "borer",
    "boron",
    "crop",
    "crops",
    "cultivation",
    "disease",
    "diseases",
    "drainage",
    "farm",
    "farmer",
    "farming",
    "fertility",
    "fertilization",
    "fertilizer",
    "fertilizers",
    "field",
    "flowering",
    "fruit",
    "germination",
    "harvest",
    "irrigate",
    "irrigation",
    "leaf",
    "manure",
    "moisture",
    "mulch",
    "mulching",
    "nutrient",
    "nutrients",
    "organic",
    "pest",
    "pests",
    "ph",
    "plant",
    "plants",
    "rain",
    "root",
    "seed",
    "seeds",
    "soil",
    "sowing",
    "spray",
    "temperature",
    "tillage",
    "water",
    "watering",
    "weed",
    "weeds",
    "yield",
}

MARKET_KEYWORDS = {"market", "price", "prices", "rate", "rates", "sell", "selling"}

KNOWN_CROP_WORDS = {
    "apple",
    "banana",
    "blackgram",
    "chickpea",
    "coconut",
    "coffee",
    "cotton",
    "grapes",
    "jute",
    "kidneybeans",
    "lentil",
    "maize",
    "mango",
    "mothbeans",
    "mungbean",
    "muskmelon",
    "orange",
    "papaya",
    "pigeonpeas",
    "pomegranate",
    "rice",
    "watermelon",
}


def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_random(data):
    return random.choice(data)


def get_quick_actions():
    return [
        "Help",
        "Crop status",
        "Soil status",
        "Fertilizer",
        "Weather",
        "Irrigation",
        "Tip",
        "Time",
        "History",
    ]


def get_help_text():
    return """Available Commands:
- Help
- Crop status
- Soil status
- Fertilizer
- Weather
- Irrigation
- Tip
- Time
- History
- Exit"""


def show_help():
    return get_help_text()


def get_words(text):
    return set(re.findall(r"[a-z]+", text.lower()))


def show_crop_status():
    result = "Crop Status:\n"
    for crop, status in crop_status.items():
        result += f"- {crop}: {status}\n"
    return result


def find_crop_status(user_input):
    words = get_words(user_input)
    for crop, status in crop_status.items():
        crop_words = get_words(crop)
        if crop_words and crop_words.issubset(words):
            return f"{crop} Status: {status}"
    return None


def find_crop_record(records, user_input, heading):
    words = get_words(user_input)
    for crop, message in records.items():
        crop_words = get_words(crop)
        if crop_words and crop_words.issubset(words):
            return f"{crop} {heading}: {message}"
    return None


def find_dataset_answer(user_input):
    words = get_words(user_input) - STOP_WORDS
    best_label = None
    best_message = None
    best_score = 0

    searchable_sections = [
        ("Crop", crop_status),
        ("Soil", soil_info),
        ("Fertilizer", fertilizer),
    ]

    for section, records in searchable_sections:
        for label, message in records.items():
            label_words = get_words(label) - STOP_WORDS
            haystack = get_words(f"{label} {message}") - STOP_WORDS
            score = len(words.intersection(haystack))
            label_score = len(words.intersection(label_words))
            if score > best_score and (label_score > 0 or score >= 3):
                best_label = f"{section} - {label}"
                best_message = message
                best_score = score

    if best_score >= 2:
        return f"{best_label}: {best_message}"

    return None


def is_agriculture_related(words):
    return bool(
        words.intersection(AGRICULTURE_KEYWORDS)
        or words.intersection(KNOWN_CROP_WORDS)
        or words.intersection(MARKET_KEYWORDS)
    )


def get_agriculture_fallback(words):
    if words.intersection(MARKET_KEYWORDS):
        return (
            "Market Price Advice: I do not have live crop prices in this project yet. "
            "Check your local mandi or agriculture market board, compare prices from nearby markets, "
            "and sell only after checking quality grade, transport cost, and demand."
        )

    return (
        "Agriculture Advice: I can help with crops, soil, fertilizer, irrigation, weather, pests, "
        "disease prevention, seeds, weeding, harvest, and general farm care. "
        "For a better answer, mention the crop name and the problem, for example: "
        "'rice fertilizer', 'tomato pest', or 'soil moisture'."
    )


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
    visible_history = [cmd for cmd in history if cmd.strip().lower() != "history"]

    if len(visible_history) == 0:
        return "No commands entered yet."
    result = "Command History:\n"
    for count, cmd in enumerate(visible_history, start=1):
        result += f"{count}. {cmd}\n"
    return result.rstrip()


def get_welcome_message():
    msg = "Welcome to AgriFlow Assistant.\n"
    msg += "Use the suggested prompts or type your own question about crops, soil, fertilizer, weather, irrigation, tips, time, or history.\n"
    msg += "Type help to see all commands."
    return msg


def build_welcome_payload():
    return {
        "title": "AgriFlow Assistant",
        "message": get_welcome_message(),
        "quick_actions": get_quick_actions()
    }


def detect_topic(user_input):
    # check what the user is asking about using simple keyword check
    words = get_words(user_input)

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
        return "Please type a question so I can help with your farm update."

    lower_input = user_input.lower()
    words = get_words(lower_input)

    # check for help
    if words.intersection({"help", "assist", "guide"}):
        return show_help()

    # check for exit
    if words.intersection({"exit", "quit"}):
        return "Thank you for using the Agriculture Chatbot. Goodbye!"

    if words.intersection(MARKET_KEYWORDS):
        return get_agriculture_fallback(words)

    topic = detect_topic(lower_input)

    if topic == "fertilizer":
        fertilizer_response = find_crop_record(fertilizer, lower_input, "Fertilizer")
        if fertilizer_response:
            return fertilizer_response

    crop_response = find_crop_status(lower_input)
    if crop_response and topic in {None, "crop"}:
        return crop_response

    # detect topic and return response
    if topic == "crop":
        return show_crop_status()

    elif topic == "soil":
        return show_soil_info()

    elif topic == "fertilizer":
        return show_fertilizer_info()

    elif topic == "weather":
        return "Weather Update: " + get_random(weather_updates)

    elif topic == "tip":
        return "Agriculture Tip: " + get_random(tips)

    elif topic == "irrigation":
        return get_random(irrigation_updates)

    elif topic == "time":
        return "Current Time: " + get_current_time()

    elif topic == "history":
        return show_history(command_history)

    dataset_response = find_dataset_answer(lower_input)
    if dataset_response:
        return dataset_response

    elif is_agriculture_related(words):
        return get_agriculture_fallback(words)

    else:
        return "Command not recognized. Try 'help' to see what you can ask."


def should_exit(user_input):
    words = get_words(user_input)
    return bool(words.intersection({"exit", "quit"}))


def handle_command(user_input, command_history=None):
    return get_bot_response(user_input, command_history)
