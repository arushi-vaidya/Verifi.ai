# FactChecker
# RV Fact Checker

RV Fact Checker is a web-based application that uses a machine learning model to classify news articles as either **true** or **fake**. The project leverages a Naive Bayes classifier with TF-IDF vectorization to analyze the text and predict the article's authenticity. The web app is designed with a chatbot-style interface that maintains conversation history, allowing users to classify multiple articles and view previous classifications.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Model Training](#model-training)
- [License](#license)

---

## Features

- **News Classification**: Predicts whether a given news article is likely true or fake.
- **Chat Interface**: Chatbot-style UI that maintains conversation history, allowing users to see past classifications.
- **Dark Theme**: Modern dark-themed UI with a compact, responsive design.
- **Simple Interface**: Easy-to-use form with real-time results displayed in a chat-like window.

## Installation

To run this project locally, follow these steps:

### Prerequisites

- Python 3.6+
- Flask
- Required Python libraries listed in `requirements.txt`

### Clone the Repository

```bash
git clone https://github.com/arushi-vaidya/rv-fact-checker.git
cd rv-fact-checker
