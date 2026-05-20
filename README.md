# Agriculture Chatbot

A simple chatbot I built using Python for agriculture related queries.
It works as both a CLI tool and a website.

## What it does

You can ask the chatbot about:
- crop status
- soil conditions
- fertilizer recommendations
- weather updates
- irrigation status
- farming tips
- current time
- command history

## How to run

### Website version

```
python web_app.py
```

Then open http://127.0.0.1:8000 in your browser.

### CLI version

```
python chatbot.py
```

## Commands you can type

```
help
crop
soil
fertilizer
weather
irrigation
tip
time
history
exit
```

## Files

- chatbot.py - main CLI file
- web_app.py - runs the website
- command_handler.py - handles user input and gives responses
- agriculture_data.py - loads and summarizes the crop recommendation dataset
- data/crop_recommendation_source.csv - source-backed crop recommendation dataset with soil nutrients, temperature, humidity, pH, rainfall, and crop labels
- utils.py - helper functions

## Dataset Source

The project uses the public Crop Recommendation dataset originally published on Kaggle and mirrored in a public GitHub repository for direct CSV access.

- Kaggle dataset page: https://www.kaggle.com/datasets/varshitanalluri/crop-recommendation-dataset/data
- CSV used in this project: https://github.com/nileshiq/Crop-Recommendation/blob/main/Crop_Recommendation.csv

Dataset fields:
- Nitrogen
- Phosphorus
- Potassium
- Temperature
- Humidity
- pH_Value
- Rainfall
- Crop

## Tech used

- Python
- HTML, CSS, JavaScript
- Python built-in HTTP server
