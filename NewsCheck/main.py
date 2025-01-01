import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

def load_data():
    # Load true news dataset
    try:
        true_df = pd.read_csv('True.csv', encoding='utf-8')
        print("Columns in True.csv:", true_df.columns)
        true_df['label'] = 1  # Add a label column for true news
        true_df['text'] = true_df['text'].fillna('')  # Fill missing text with empty string
        print(f"Loaded True.csv, shape: {true_df.shape}")
    except Exception as e:
        print("Error loading True.csv:", e)
        return None
    
    # Load fake news dataset
    try:
        fake_df = pd.read_csv('Fake.csv', encoding='utf-8')
        print("Columns in Fake.csv:", fake_df.columns)
        fake_df['label'] = 0  # Add a label column for fake news
        fake_df['text'] = fake_df['text'].fillna('')  # Fill missing text with empty string
        print(f"Loaded Fake.csv, shape: {fake_df.shape}")
    except Exception as e:
        print("Error loading Fake.csv:", e)
        return None
    
    # Load the additional news dataset (news_dataset.csv)
    try:
        news_df = pd.read_csv('news_dataset.csv', encoding='ISO-8859-1')  # Use a different encoding
        print("Columns in news_dataset.csv:", news_df.columns)
        # Drop the 'Date' column (making sure the column name is correct)
        if 'Date' in news_df.columns:
            news_df = news_df.drop(columns=['Date'])
            print("Dropped 'Date' column.")
        else:
            print("'Date' column not found in news_dataset.csv.")
            
        news_df = news_df[['Statement', 'Label']]  # Extract relevant columns
        news_df.rename(columns={'Statement': 'text', 'Label': 'label'}, inplace=True)  # Rename for consistency
        news_df['text'] = news_df['text'].fillna('')  # Fill missing text with empty string
        # Clean the text data by removing non-alphanumeric characters and converting to lowercase
        news_df['text'] = news_df['text'].str.replace(r'[^a-zA-Z\s]', '', regex=True).str.lower()
        print(f"Loaded news_dataset.csv, shape: {news_df.shape}")
    except Exception as e:
        print("Error loading news_dataset.csv:", e)
        return None

    # Handle missing values in the 'text' and 'label' columns (drop rows with NaN)
    true_df = true_df.dropna(subset=['text', 'label'])
    fake_df = fake_df.dropna(subset=['text', 'label'])
    news_df = news_df.dropna(subset=['text', 'label'])

    # Remove any rows with empty strings in the text columns
    true_df = true_df[true_df['text'].str.strip() != '']
    fake_df = fake_df[fake_df['text'].str.strip() != '']
    news_df = news_df[news_df['text'].str.strip() != '']

    print(f"After cleaning, shapes: True.csv: {true_df.shape}, Fake.csv: {fake_df.shape}, news_dataset.csv: {news_df.shape}")

    # Combine the datasets into one
    combined_df = pd.concat([true_df[['text', 'label']], 
                             fake_df[['text', 'label']], 
                             news_df[['text', 'label']]], ignore_index=True)
    print(f"Combined dataset shape: {combined_df.shape}")
    
    # Ensure that no NaN values are present in the final combined dataset
    combined_df = combined_df.dropna(subset=['text', 'label'])
    print(f"Shape after dropping NaN rows: {combined_df.shape}")

    # Convert label column to int type explicitly
    combined_df['label'] = combined_df['label'].replace({'TRUE': 1, 'FALSE': 0, 'true': 1, 'false': 0, 'True': 1, 'False': 0, 'Fake':0})
    
    # Handle any remaining non-numeric values in the label column by forcing them to NaN and then dropping them
    combined_df['label'] = pd.to_numeric(combined_df['label'], errors='coerce')
    combined_df = combined_df.dropna(subset=['label'])

    print(f"Shape after cleaning label column: {combined_df.shape}")

    # Convert label column to int
    combined_df['label'] = combined_df['label'].astype(int)

    return combined_df


def train_model(df):
    # Split data into training and test sets
    X = df['text']
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create a pipeline with TfidfVectorizer and Naive Bayes classifier
    model = make_pipeline(TfidfVectorizer(max_features=5000), MultinomialNB())
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy * 100:.2f}%")
    
    # Generate classification report
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"Confusion Matrix:\n{cm}")
    
    return model

def save_model(model):
    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)

if __name__ == "__main__":
    df = load_data()
    if df is not None:
        model = train_model(df)
        save_model(model)

        # Taking user input for testing
        user_input = input("Enter a news article: ")

        # Error handling for user input
        if len(user_input.strip()) == 0:
            print("Input cannot be empty. Please try again.")
        else:
            # Predict the news category
            prediction = model.predict([user_input])
            if prediction[0] == 1:
                print("This news is classified as TRUE.")
            else:
                print("This news is classified as FAKE.")
