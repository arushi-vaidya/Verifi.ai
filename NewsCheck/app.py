from flask import Flask, render_template, request, session, redirect, url_for
import pickle
from datetime import timedelta

# Initialize the Flask application
app = Flask(__name__)

# Set a secret key for securely signing the session cookie
app.secret_key = 'your_secret_key'

# Define the duration for permanent sessions
app.permanent_session_lifetime = timedelta(minutes=30)

# Load the pre-trained model from a pickle file
# The model is assumed to classify news articles as 'True' or 'Fake'
with open('model.pkl', 'rb') as file:
    news_model = pickle.load(file)

# Define the root route (homepage) of the application
@app.route('/')
def index():
    """
    Render the index page. 
    Initializes the conversation in the session if it doesn't exist.
    """
    if 'conversation' not in session:
        session['conversation'] = []  # Initialize an empty conversation in session
    return render_template('index.html', conversation=session['conversation'])

# Define the route for handling predictions
@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict whether a news article is 'True' or 'Fake' using the loaded model.
    Store the user's input and the prediction result in the session conversation.
    """
    # Get the news article text from the submitted form
    news_article = request.form['news_article']
    
    # Use the model to predict the class of the news article
    prediction = news_model.predict([news_article])
    
    # Convert the prediction into a human-readable result
    result = "True" if prediction[0] == 0 else "Fake"
    
    # Append the user's input and the model's prediction to the conversation
    session['conversation'].append({
        'user_input': news_article,
        'prediction': result
    })
    session.modified = True  # Mark the session as modified to save changes
    
    # Redirect back to the index page to display the updated conversation
    return redirect(url_for('index'))

# Define the route for clearing the conversation
@app.route('/clear')
def clear_conversation():
    """
    Clear the conversation history stored in the session.
    """
    session.pop('conversation', None)  # Remove the conversation from the session
    return redirect(url_for('index'))  # Redirect to the index page

# Define a route to redirect to the home page of the application
@app.route('/home')
def home_page():
    """
    Redirect to the home page of the application.
    """
    return redirect('http://127.0.0.1:5000')

# Define a route to redirect to the phishing detector application
@app.route('/phishing_detector')
def phishing_detector():
    """
    Redirect to the phishing detector application.
    """
    return redirect('http://127.0.0.1:5002')

# Run the application
if __name__ == '__main__':
    """
    Start the Flask application on port 5001 with debugging enabled.
    """
    app.run(port=5001, debug=True)
