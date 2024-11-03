from flask import Flask, render_template, request, session, redirect, url_for
import pickle
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
app.permanent_session_lifetime = timedelta(minutes=30)

# Load the news classification model
with open('model.pkl', 'rb') as file:
    news_model = pickle.load(file)

# Route for the home page (RV Fact Checker)
@app.route('/')
def index():
    # Initialize session history if it doesn't exist
    if 'conversation' not in session:
        session['conversation'] = []
    return render_template('index.html', conversation=session['conversation'])

# Route for news classification
@app.route('/predict', methods=['POST'])
def predict():
    news_article = request.form['news_article']
    prediction = news_model.predict([news_article])
    result = "True" if prediction[0] == 0 else "Fake"

    # Store user input and prediction in session
    session['conversation'].append({
        'user_input': news_article,
        'prediction': result
    })
    session.modified = True  # Indicate session has changed

    return redirect(url_for('index'))

# Route to clear conversation history
@app.route('/clear')
def clear_conversation():
    session.pop('conversation', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
