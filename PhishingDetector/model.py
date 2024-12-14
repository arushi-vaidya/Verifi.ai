# File: model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the dataset from a CSV file
# 'phishing_dataset.csv' should contain columns 'URL' and 'Label' where 'Label' indicates good (0) or bad (1) URLs
data = pd.read_csv('phishing_dataset.csv')

# Map the labels 'good' to 0 and 'bad' to 1 for binary classification
data['Label'] = data['Label'].map({'good': 0, 'bad': 1})

# Feature Engineering
# Feature 1: Calculate the length of the URL
data['url_length'] = data['URL'].apply(len)

# Feature 2: Count the number of special characters in the URL (., -, _, /, @)
data['special_chars'] = data['URL'].apply(lambda x: sum(1 for c in x if c in ['.', '-', '_', '/', '@']))

# Feature 3: Count the number of digits in the URL
data['digit_count'] = data['URL'].apply(lambda x: sum(c.isdigit() for c in x))

# Define the features (X) and target (y) variables
# Features: url_length, special_chars, digit_count
X = data[['url_length', 'special_chars', 'digit_count']]

# Target: Label (0 for good, 1 for bad)
y = data['Label']

# Split the dataset into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Classifier model
# Random state is set for reproducibility
model = RandomForestClassifier(random_state=42)

# Train the model using the training data (X_train and y_train)
model.fit(X_train, y_train)

# Predict the target values using the test data (X_test)
y_pred = model.predict(X_test)

# Evaluate the model's performance using accuracy score and classification report
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the trained model to a file using joblib for later use
joblib.dump(model, 'phishing_model.pkl')
print("Model saved as 'phishing_model.pkl'")


























































