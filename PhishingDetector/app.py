from flask import Flask, request, render_template
import joblib
import whois
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

# Load the trained model
model = joblib.load('phishing_model.pkl')

# Analyze WHOIS data
def analyze_whois(whois_data):
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

    # WHOIS Privacy
    analysis['whois_privacy'] = 'Yes' if whois_data.get('privacy') else 'No'

    return analysis


# Analyze Google search results
def analyze_google_results(google_results):
    analysis = {}

    # Analyze number of Google search results
    analysis['google_results_count'] = len(google_results)

    # Look for phishing-related warnings or trusted sources in the search results
    phishing_indicators = ['phishing', 'malware', 'scam', 'warning']
    analysis['google_phishing_warning'] = any(indicator in result.lower() for result in google_results for indicator in phishing_indicators)
    
    return analysis


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']

    # Feature extraction
    url_length = len(url)
    special_chars = sum(1 for c in url if c in ['.', '-', '_', '/', '@'])
    digit_count = sum(c.isdigit() for c in url)
    features = [[url_length, special_chars, digit_count]]
    
    # Prediction
    prediction = model.predict(features)[0]
    result = 'Phishing' if prediction == 1 else 'Legitimate'

    # WHOIS lookup
    whois_data = {}
    whois_analysis = {}
    try:
        domain = url.split('/')[2] if '//' in url else url.split('/')[0]
        domain_info = whois.whois(domain)
        whois_data = {
            'domain_name': domain_info.domain_name,
            'creation_date': domain_info.creation_date,
            'expiration_date': domain_info.expiration_date,
            'privacy': domain_info.get('privacy'),
        }
        whois_analysis = analyze_whois(domain_info)
    except Exception as e:
        whois_data = {'error': str(e)}
        whois_analysis = {'error': str(e)}

    # Google search results
    google_results = []
    google_analysis = {}
    try:
        search_url = f"https://www.google.com/search?q={url}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        google_results = [a.text for a in soup.select('h3')][:5]
        google_analysis = analyze_google_results(google_results)
    except Exception as e:
        google_results = [f"Error fetching search results: {e}"]
        google_analysis = {'error': str(e)}

    # Combine all the analysis and return to the template
    return render_template('result.html', 
                           url=url, 
                           result=result, 
                           whois_data=whois_data, 
                           whois_analysis=whois_analysis,
                           google_results=google_results,
                           google_analysis=google_analysis)


if __name__ == '__main__':
    app.run(debug=True)
