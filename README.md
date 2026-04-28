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
- agriculture_data.py - stores all the agriculture information
- utils.py - helper functions

## Tech used

- Python
- HTML, CSS, JavaScript
- Python built-in HTTP server
