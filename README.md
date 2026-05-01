# SpamGuard

A simple SMS spam classifier built with FastAPI, scikit-learn, and NLP preprocessing.

## Project structure

- `main.py` - FastAPI backend that loads a trained spam classifier and exposes a `/predict` endpoint.
- `index.html` - Web UI for entering messages and viewing classification results.
- `script.js` - Frontend script that sends user input to the prediction API.
- `style.css` - Styling for the web interface.
- `model.pkl` - Trained classification model.
- `vectorizer.pkl` - TF-IDF vectorizer used to transform input text.
- `requirements.txt` - Python dependencies.
- `Procfile` - Startup command for deployment platforms.
- `Spam_classifier.ipynb` - Notebook for training and exploring the classifier.

## Features

- Predicts whether a message is `Spam` or `Not Spam`
- Uses NLTK preprocessing including tokenization, stopword removal, and stemming
- Supports real-time inference via a web interface

## Requirements

- Python 3.8+
- `pip` package manager

## Install

```bash
python -m pip install -r requirements.txt
```

## Run locally

1. Start the FastAPI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

2. Open `index.html` in a browser.

> Note: `script.js` currently sends requests to a deployed API endpoint. If you want to use the local server instead, update the `fetch` URL in `script.js` from `https://sms-spam-2-jsrh.onrender.com/predict` to `/predict`.

## Usage

- Paste or type an SMS message in the input box.
- Click `Analyze`.
- See the predicted label displayed on the page.

## Deployment

The app can be deployed to platforms that support FastAPI and `Procfile`-style web processes.

Example command:

```bash
heroku local web
```

or using any compatible cloud provider that supports Python web apps.

## Notes

- The backend downloads NLTK resources at startup if needed.
- The classifier pipeline relies on `vectorizer.pkl` and `model.pkl` present in the project root.
