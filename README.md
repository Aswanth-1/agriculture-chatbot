# Natural Language Agriculture Chatbot

## Overview

This project is a Python agriculture assistant that now supports both:

- a command-line interface
- a browser-based website

The chatbot answers agriculture-related questions about crop status, soil condition, irrigation, weather updates, fertilizer recommendations, farming tips, time, and command history.

## Features

- Website chat interface
- Command Line Interface (CLI)
- Natural language style commands
- Free typing for custom questions
- Clickable prompts for instant answers
- Keyword matching
- Agriculture knowledge base
- Randomized weather and tip responses
- Reusable chatbot logic for the website

## Technologies Used

- Python
- HTML
- CSS
- JavaScript
- Built-in Python HTTP server
- Built-in `unittest` test framework

## Example Commands

```text
help
crop status
soil status
weather
fertilizer
irrigation
tip
time
history
exit
```

## How to Run

### Run the Website

```bash
python web_app.py
```

Then open `http://127.0.0.1:8000` in your browser.

### Run the CLI

```bash
python chatbot.py
```

## Run Tests

```bash
python -m unittest discover -s tests -v
```
