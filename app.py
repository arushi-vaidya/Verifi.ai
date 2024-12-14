from flask import Flask, redirect, render_template

# Initialize the Flask application
app = Flask(__name__)

# Define the root route (homepage)
@app.route('/')
def home():
    """
    Render the home page.
    This is the main landing page of the application.
    """
    return render_template('home.html')

# Define a route to redirect to the news checker application
@app.route('/news_checker')
def news_checker():
    """
    Redirect to the news checker application.
    The news checker is hosted on port 5001.
    """
    return redirect('http://127.0.0.1:5001')

# Define a route to redirect to the phishing detector application
@app.route('/phishing_detector')
def phishing_detector():
    """
    Redirect to the phishing detector application.
    The phishing detector is hosted on port 5002.
    """
    return redirect('http://127.0.0.1:5002')

# Define a route to render the "About Us" page
@app.route('/about_us')
def about_us():
    """
    Render the "About Us" page.
    This page provides information about the application or team.
    """
    return render_template('about_us.html')

# Run the application
if __name__ == '__main__':
    """
    Start the Flask application with debugging enabled on port 5000.
    Debug mode helps during development by providing detailed error messages.
    """
    app.run(debug=True, port=5000)
