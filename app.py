from flask import Flask, request, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pickle

# Load the model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    user_input = request.form['news_article']
    if user_input.strip():
        prediction = model.predict([user_input])
        result = "The news is likely to be true." if prediction[0] == 0 else "The news is likely to be fake."
    else:
        result = "No input provided. Please enter a valid news article."
    
    return render_template('index.html', prediction=result)

if __name__ == "__main__":
    app.run(debug=True)
