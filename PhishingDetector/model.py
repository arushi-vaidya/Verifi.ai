# File: model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the dataset
data = pd.read_csv('phishing_dataset.csv')

# Map labels to binary values
data['Label'] = data['Label'].map({'good': 0, 'bad': 1})

# Feature Engineering
# Feature 1: Length of URL
data['url_length'] = data['URL'].apply(len)

# Feature 2: Count of special characters in URL
data['special_chars'] = data['URL'].apply(lambda x: sum(1 for c in x if c in ['.', '-', '_', '/', '@']))

# Feature 3: Count of digits in URL
data['digit_count'] = data['URL'].apply(lambda x: sum(c.isdigit() for c in x))

# Features and Target
X = data[['url_length', 'special_chars', 'digit_count']]
y = data['Label']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the trained model
joblib.dump(model, 'phishing_model.pkl')
print("Model saved as 'phishing_model.pkl'")
