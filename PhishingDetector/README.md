# Phishing Detector Web Application

This is a Flask-based web application designed to predict whether a given URL is phishing or legitimate. The application utilizes machine learning for URL classification and analyzes additional data such as WHOIS information and Google search results to provide further insights into the URL's credibility.

## Features
- **Phishing Prediction**: Predicts whether a URL is phishing or legitimate based on its features (e.g., URL length, special characters, digit count).
- **WHOIS Data Analysis**: Analyzes domain-related information such as domain age, expiration date, and WHOIS privacy.
- **Google Search Analysis**: Fetches Google search results for the URL to check for phishing-related warnings or indicators.

## Requirements

Before running the application, ensure that you have the following installed:

- Python 3.x
- pip (Python package installer)

The required Python packages are:

- `Flask`
- `joblib`
- `whois`
- `requests`
- `beautifulsoup4`

You can install them by running:

```bash
pip install Flask joblib whois requests beautifulsoup4
