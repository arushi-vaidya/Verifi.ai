from flask import Flask, request, render_template, redirect
import joblib
import whois
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Load the trained phishing detection model using joblib
model = joblib.load('phishing_model.pkl')

# Function to analyze WHOIS data
def analyze_whois(whois_data):
    """
    Analyze the WHOIS data to extract domain age, expiration date, and privacy status.
    Returns a dictionary with analysis results.
    """
    analysis = {}
    
    # Analyze domain age
    if 'creation_date' in whois_data and isinstance(whois_data.creation_date, list):
        domain_age = (datetime.now() - whois_data.creation_date[0]).days
        analysis['domain_age'] = domain_age
        analysis['domain_age_status'] = 'Suspicious' if domain_age < 180 else 'Legitimate'
    else:
        analysis['domain_age'] = None
        analysis['domain_age_status'] = 'Unknown'
    
    # Analyze expiration date
    if 'expiration_date' in whois_data and isinstance(whois_data.expiration_date, list):
        expiration_date = whois_data.expiration_date[0]
        analysis['expiration_date'] = expiration_date
        analysis['expiration_status'] = 'Suspicious' if expiration_date < datetime.now() else 'Legitimate'
    else:
        analysis['expiration_date'] = None
        analysis['expiration_status'] = 'Unknown'
    
    # Check if the WHOIS data is private
    analysis['whois_privacy'] = 'Yes' if whois_data.get('privacy') else 'No'

    return analysis

# Function to analyze Google search results
def analyze_google_results(google_results):
    """
    Analyze the first 5 Google search results to look for phishing indicators like 'phishing', 'scam', etc.
    Returns a dictionary with the count of results and whether phishing-related warnings were found.
    """
    analysis = {}
    analysis['google_results_count'] = len(google_results)
    
    # Define phishing indicators
    phishing_indicators = ['phishing', 'malware', 'scam', 'warning']
    
    # Check if any of the search results contain phishing-related keywords
    analysis['google_phishing_warning'] = any(indicator in result.lower() for result in google_results for indicator in phishing_indicators)
    
    return analysis

# Route for the home page
@app.route('/')
def home():
    """
    Render the home page of the phishing detector application.
    """
    return render_template('index.html')

# Route to predict if the given URL is phishing or legitimate
@app.route('/predict', methods=['POST'])
def predict():
    """
    Analyze the provided URL to predict whether it is phishing or legitimate.
    Extract features, perform a WHOIS lookup, and analyze Google search results.
    """
    # Get the URL input from the user
    url = request.form['url']

    # Feature extraction from the URL (e.g., URL length, special characters, and digit count)
    url_length = len(url)
    special_chars = sum(1 for c in url if c in ['.', '-', '_', '/', '@'])
    digit_count = sum(c.isdigit() for c in url)
    features = [[url_length, special_chars, digit_count]]
    
    # Use the pre-trained model to predict if the URL is phishing or legitimate
    prediction = model.predict(features)[0]
    result = 'Phishing' if prediction == 1 else 'Legitimate'

    # WHOIS lookup to extract domain information
    whois_data = {}
    whois_analysis = {}
    try:
        # Extract domain from the URL
        domain = url.split('/')[2] if '//' in url else url.split('/')[0]
        
        # Perform WHOIS lookup
        domain_info = whois.whois(domain)
        
        # Store WHOIS data
        whois_data = {
            'domain_name': domain_info.domain_name,
            'creation_date': domain_info.creation_date,
            'expiration_date': domain_info.expiration_date,
            'privacy': domain_info.get('privacy'),
        }
        
        # Analyze WHOIS data
        whois_analysis = analyze_whois(domain_info)
    except Exception as e:
        # Handle exceptions in case of invalid domain or failed WHOIS lookup
        whois_data = {'error': str(e)}
        whois_analysis = {'error': str(e)}

    # Google search results analysis
    google_results = []
    google_analysis = {}
    try:
        # Perform Google search to gather results related to the URL
        search_url = f"https://www.google.com/search?q={url}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        
        # Parse the search results with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        google_results = [a.text for a in soup.select('h3')][:5]
        
        # Analyze Google search results
        google_analysis = analyze_google_results(google_results)
    except Exception as e:
        # Handle exceptions during the Google search process
        google_results = [f"Error fetching search results: {e}"]
        google_analysis = {'error': str(e)}

    # Render the result page with the analysis data
    return render_template('result.html', 
                           url=url, 
                           result=result, 
                           whois_data=whois_data, 
                           whois_analysis=whois_analysis,
                           google_results=google_results,
                           google_analysis=google_analysis)

# Route to redirect to the news checker application
@app.route('/news_checker')
def news_checker():
    """
    Redirect to the news checker application.
    """
    return redirect('http://127.0.0.1:5001')

# Route to redirect to the home page of the phishing detector application
@app.route('/home')
def home_page():
    """
    Redirect to the home page of the phishing detector application.
    """
    return redirect('http://127.0.0.1:5000')

# Run the application
if __name__ == '__main__':
    """
    Start the Flask application on port 5002 with debugging enabled.
    """
    app.run(port=5002, debug=True)
