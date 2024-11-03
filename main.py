import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report
import pickle

def load_data():
    # Load true news dataset
    true_df = pd.read_csv('True.csv')
    true_df['label'] = 0  # Add a label column for true news
    # Load fake news dataset
    fake_df = pd.read_csv('Fake.csv')
    fake_df['label'] = 1  # Add a label column for fake news

    # Combine the datasets
    return pd.concat([true_df, fake_df], ignore_index=True)

def train_model(df):
    # Splitting into train-test set
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

    # Train the model
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    classification_report_result = classification_report(y_test, predictions)

    # Display model evaluation results
    print("Model Accuracy: {:.2f}%".format(accuracy * 100))
    print("\nClassification Report:\n", classification_report_result)

    return model

def save_model(model):
    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)

if __name__ == "__main__":
    df = load_data()
    model = train_model(df)
    save_model(model)

    # Taking user input for testing
    user_input = input("Enter a news article: ")

    # Error handling for user input
    if user_input.strip():  # Check if the input is not just whitespace
        # Make a prediction
        prediction = model.predict([user_input])

        # Display the result
        if prediction[0] == 0:
            print("The news is likely to be true.")
        else:
            print("The news is likely to be fake.")
    else:
        print("No input provided. Please enter a valid news article.")
