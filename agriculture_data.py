import csv
from collections import defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).parent
CROP_RECOMMENDATION_DATASET = BASE_DIR / "data" / "crop_recommendation_source.csv"


def _average(values):
    return sum(values) / len(values)


def _range_text(values, unit=""):
    suffix = f" {unit}" if unit else ""
    return f"{min(values):.1f}-{max(values):.1f}{suffix}"


def load_crop_recommendation_rows(path=CROP_RECOMMENDATION_DATASET):
    rows = []
    with path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            rows.append(
                {
                    "crop": row["Crop"].strip().title(),
                    "nitrogen": float(row["Nitrogen"]),
                    "phosphorus": float(row["Phosphorus"]),
                    "potassium": float(row["Potassium"]),
                    "temperature": float(row["Temperature"]),
                    "humidity": float(row["Humidity"]),
                    "ph": float(row["pH_Value"]),
                    "rainfall": float(row["Rainfall"]),
                }
            )
    return rows


def build_crop_profiles(rows):
    grouped_rows = defaultdict(list)
    for row in rows:
        grouped_rows[row["crop"]].append(row)

    profiles = {}
    for crop, crop_rows in sorted(grouped_rows.items()):
        profiles[crop] = {
            "records": len(crop_rows),
            "nitrogen_avg": _average([row["nitrogen"] for row in crop_rows]),
            "phosphorus_avg": _average([row["phosphorus"] for row in crop_rows]),
            "potassium_avg": _average([row["potassium"] for row in crop_rows]),
            "temperature_range": _range_text([row["temperature"] for row in crop_rows], "C"),
            "humidity_range": _range_text([row["humidity"] for row in crop_rows], "%"),
            "ph_range": _range_text([row["ph"] for row in crop_rows]),
            "rainfall_range": _range_text([row["rainfall"] for row in crop_rows], "mm"),
        }

    return profiles


def build_crop_status(profiles):
    crop_messages = {}
    for crop, profile in profiles.items():
        crop_messages[crop] = (
            f"Based on {profile['records']} dataset records, suitable conditions are "
            f"temperature {profile['temperature_range']}, humidity {profile['humidity_range']}, "
            f"soil pH {profile['ph_range']}, and rainfall {profile['rainfall_range']}. "
            f"Average soil nutrients are N {profile['nitrogen_avg']:.1f}, "
            f"P {profile['phosphorus_avg']:.1f}, K {profile['potassium_avg']:.1f}."
        )
    return crop_messages


def build_fertilizer_profiles(profiles):
    fertilizer_messages = {}
    for crop, profile in profiles.items():
        fertilizer_messages[crop] = (
            f"The dataset average nutrient profile for {crop} is "
            f"N {profile['nitrogen_avg']:.1f}, P {profile['phosphorus_avg']:.1f}, "
            f"K {profile['potassium_avg']:.1f}. Use this as a reference and confirm exact "
            f"fertilizer dose with a local soil test."
        )

    fertilizer_messages["Organic"] = (
        "Use compost, vermicompost, green manure, or well-decomposed farmyard manure "
        "to improve soil structure and slow-release nutrients."
    )
    fertilizer_messages["Balanced"] = (
        "Balanced fertilization means supplying N, P, K, and needed micronutrients "
        "according to crop requirement and soil-test results."
    )

    return fertilizer_messages


crop_recommendation_rows = load_crop_recommendation_rows()
crop_profiles = build_crop_profiles(crop_recommendation_rows)

crop_status = build_crop_status(crop_profiles)
fertilizer = build_fertilizer_profiles(crop_profiles)

soil_info = {
    "Moisture Low": "Irrigate soon and use mulch where possible. Check that water reaches the crop root zone.",
    "Moisture High": "Pause irrigation, improve drainage, and watch for root rot or fungal disease.",
    "pH Low": "Soil is acidic. Add agricultural lime only after checking soil-test recommendations.",
    "pH High": "Soil is alkaline. Add organic matter and follow local soil-test guidance before correction.",
    "Nutrient Deficiency": "Test soil for N, P, K, sulphur, zinc, and boron before corrective application.",
    "Soil Health": "Improve soil health with crop rotation, cover crops, compost, residue retention, and careful tillage.",
}

weather_updates = [
    "Sunny and dry conditions are suitable for field work. Irrigate sensitive crops if soil moisture is falling.",
    "Light rain is possible. Delay irrigation and avoid spraying pesticides just before rainfall.",
    "Heavy rainfall risk. Clean drainage channels and avoid fertilizer application until the field is workable.",
    "High temperature expected. Irrigate early morning or evening and protect seedlings from heat stress.",
    "Humid weather increases fungal disease risk. Improve airflow and scout leaves for early symptoms.",
]

tips = [
    "Rotate cereals, pulses, and vegetables to break pest cycles and protect soil fertility.",
    "Inspect fields weekly so pests and nutrient problems are caught before they spread.",
    "Use certified, healthy seed and choose varieties suited to local climate and soil.",
    "Remove weeds early because young crops lose yield quickly when competing for water and nutrients.",
    "Test soil before each major season to plan fertilizer and pH correction accurately.",
]

irrigation_updates = [
    "Irrigation system is running. Check field edges to confirm water distribution is even.",
    "Water supply is normal. Continue the planned irrigation schedule.",
    "Irrigation is scheduled for evening to reduce evaporation losses.",
    "Inspect filters, valves, and channels before the next irrigation cycle.",
]
