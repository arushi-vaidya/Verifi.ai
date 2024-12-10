from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/news_checker')
def news_checker():
    return redirect('http://127.0.0.1:5001')  

@app.route('/phishing_detector')
def phishing_detector():
    return redirect('http://127.0.0.1:5002') 

@app.route('/about_us')
def about_us():
    return render_template('about_us.html') 

if __name__ == '__main__':
    app.run(debug=True, port=5000)  
