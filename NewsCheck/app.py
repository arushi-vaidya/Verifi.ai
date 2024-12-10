from flask import Flask, render_template, request, session, redirect, url_for
import pickle
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
app.permanent_session_lifetime = timedelta(minutes=30)

with open('model.pkl', 'rb') as file:
    news_model = pickle.load(file)

@app.route('/')
def index():
    if 'conversation' not in session:
        session['conversation'] = []
    return render_template('index.html', conversation=session['conversation'])

@app.route('/predict', methods=['POST'])
def predict():
    news_article = request.form['news_article']
    prediction = news_model.predict([news_article])
    result = "True" if prediction[0] == 0 else "Fake"
    session['conversation'].append({
        'user_input': news_article,
        'prediction': result
    })
    session.modified = True  

    return redirect(url_for('index'))

@app.route('/clear')
def clear_conversation():
    session.pop('conversation', None)
    return redirect(url_for('index'))

@app.route('/home')
def home_page():
    return redirect('http://127.0.0.1:5000') 

@app.route('/phishing_detector')
def phishing_detector():
    return redirect('http://127.0.0.1:5002') 

if __name__ == '__main__':
      app.run(port=5001, debug=True)