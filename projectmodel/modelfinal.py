import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import nltk
from nltk.corpus import cmudict
import joblib

# Download CMU Pronouncing Dictionary for syllable counting
nltk.download('cmudict')
d = cmudict.dict()

# Helper function to count syllables
def syllable_count(word):
    if isinstance(word, str):  # Check if the word is a string
        try:
            return max([len([y for y in x if y[-1].isdigit()]) for x in d[word.lower()]])
        except KeyError:
            return len([char for char in word if char in 'aeiou'])  # Estimate if not found
    else:
        return 0  # Return 0 for non-strings


# Load the dataset (assuming it has columns: word, difficulty, frequency)
train_data = pd.read_csv("modeltraining/train_data.csv")
test_data = pd.read_csv("modeltraining/test_data.csv")

# Ensure 'word' column is treated as strings and handle NaN values
train_data['word'] = train_data['Word'].astype(str)
test_data['word'] = test_data['Word'].astype(str)

# Feature extraction
def extract_features(df):
    df['word_length'] = df['Word'].str.len()  # len will work safely since 'word' is now a string
    df['syllable_count'] = df['Word'].apply(syllable_count)
    return df

train_data = extract_features(train_data)
test_data = extract_features(test_data)

# Train a RandomForest model (or another classifier)
clf = RandomForestClassifier(random_state=42)
X_train = train_data[['word_length', 'syllable_count', 'Frequency']]
y_train = train_data['diff_level'].fillna(0).astype(int)
clf.fit(X_train, y_train)

# Test the model
y_test = test_data['diff_level'].fillna(0).astype(int)
X_test = test_data[['word_length', 'syllable_count', 'Frequency']]

# Make predictions
y_pred = clf.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy on Test Data: {accuracy * 100:.2f}%")

# Save the trained model (optional)
joblib.dump(clf, 'word_difficulty_model.pkl')

print("Model training complete and saved!")