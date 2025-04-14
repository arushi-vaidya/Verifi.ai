# VERIFI.AI

This repository contains two separate Flask-based web applications:

1. **NewsCheck** - A news fact-checking app that classifies news articles as true or fake using a machine learning model.
2. **Phishing Detector** - A URL phishing detection app that predicts whether a given URL is legitimate or phishing.

Both applications need to be run simultaneously for full functionality. Make sure to run each app's `app.py` in a separate terminal and the main `app.py` for the combined functionality.

## Table of Contents
- [NewsCheck](#newscheck)
- [Phishing Detector](#phishing-detector)
- [How to Run the Applications](#how-to-run-the-applications)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)

---

## NewsCheck

**News Checker** is a web-based application that uses a machine learning model to classify news articles as either **true** or **fake**. The project leverages a Naive Bayes classifier with TF-IDF vectorization to analyze the text and predict the article's authenticity. The web app is designed with a chatbot-style interface that maintains conversation history, allowing users to classify multiple articles and view previous classifications.

### Features
- **News Classification**: Predicts whether a given news article is likely true or fake.
- **Chat Interface**: Chatbot-style UI that maintains conversation history, allowing users to see past classifications.
- **Dark Theme**: Modern dark-themed UI with a compact, responsive design.
- **Simple Interface**: Easy-to-use form with real-time results displayed in a chat-like window.

### Installation
#### Prerequisites:
- Python 3.6+
- Flask
- Required Python libraries listed in `requirements.txt`

#### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rv-fact-checker.git](https://github.com/arushi-vaidya/Verifi.ai.git
   cd Verifi.ai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Train the model:
   Place the `True.csv` and `Fake.csv` datasets in the root directory.
   Run the training script to create the `model.pkl` file:
   ```bash
   python main.py
   ```

4. Start the app:
   ```bash
   python app.py
   ```
   The app will be available at: [http://127.0.0.1:5001](http://127.0.0.1:5001)

---

## Phishing Detector Web Application

This is a Flask-based web application designed to predict whether a given URL is phishing or legitimate. The application utilizes machine learning for URL classification and analyzes additional data such as WHOIS information and Google search results to provide further insights into the URL's credibility.

### Features
- **Phishing Prediction**: Predicts whether a URL is phishing or legitimate based on features like URL length, special characters, and digit count.
- **WHOIS Data Analysis**: Analyzes domain-related information such as domain age, expiration date, and WHOIS privacy.
- **Google Search Analysis**: Fetches Google search results for the URL to check for phishing-related warnings or indicators.

### Installation
#### Prerequisites:
- Python 3.x
- pip (Python package installer)

#### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/phishing-detector.git
   cd phishing-detector
   ```

2. Install dependencies:
   ```bash
   pip install Flask joblib whois requests beautifulsoup4
   python3 model.py
   ```

3. Start the app:
   ```bash
   python app.py
   ```
   The app will be available at: [http://127.0.0.1:5002](http://127.0.0.1:5002)

---

## How to Run the Applications

Since both applications are independent Flask apps, you'll need to run them in separate terminals to have both running simultaneously. Additionally, if you want the main app to integrate both services, you will need to start its `app.py` after running both apps.

### Steps to run the apps:
1. Open three terminals.
2. In the first terminal, navigate to the **NewsCheck** folder and run:
   ```bash
   cd NewsCheck
   python app.py
   ```
3. In the second terminal, navigate to the **Phishing Detector** folder and run:
   ```bash
   cd "Phishing Detector"
   python app.py
   ```
4. In the third terminal, run the main app (if applicable) that combines both apps' functionality. Ensure you have set it up to make requests to both services:
   ```bash
   cd ..
   python app.py
   ```

---

## Project Structure

### NewsCheck
```
NewsCheck/
├── app.py               # Main Flask app for NewsCheck
├── train_model.py       # Model training script
├── requirements.txt     # List of dependencies
├── model.pkl            # Saved trained model
├── True.csv             # Dataset of true news articles
├── Fake.csv             # Dataset of fake news articles
└── templates/           # HTML templates for the app
    └── index.html       # Main page template
```

### Phishing Detector
```
PhishingDetector/
├── app.py               # Main Flask app for Phishing Detector
├── requirements.txt     # List of dependencies
├── phishing_model.pkl   # Trained phishing detection model
├── whois_data.py        # WHOIS data analysis script
└── templates/           # HTML templates for the app
    └── index.html       # Main page template
```

---

## Notes

- **Ports**: By default, main runs on[http://127.0.0.1:5000](http://127.0.0.1:5000), the NewsCheck app runs on [http://127.0.0.1:5001](http://127.0.0.1:5001) and the Phishing Detector app runs on [http://127.0.0.1:5002](http://127.0.0.1:5002).
- **Dependencies**: Make sure you have installed the required dependencies for each app by following the instructions above.
- **Model Training**: For NewsCheck, make sure you train the model first before running the app, or use a pre-trained model if available.

---

## Usage

- **NewsCheck**: Users can input news article text into the chat interface to classify it as either true or fake.
- **Phishing Detector**: Users can input a URL to classify it as legitimate or phishing and view additional insights like WHOIS data and Google search results.
```
