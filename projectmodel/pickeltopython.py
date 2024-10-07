import pandas as pd
import joblib
import nltk
from nltk.corpus import cmudict

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

# Load the trained model
model = joblib.load('word_difficulty_model.pkl')

# Function to predict the difficulty level of a word
def predict_difficulty(word):
    word_length = len(word)
    syllable_count_value = syllable_count(word)
    
    # Create a DataFrame to hold the features
    features = pd.DataFrame({
        'word_length': [word_length],
        'syllable_count': [syllable_count_value],
        'Frequency': [0]  # Placeholder for frequency if needed; adjust as necessary
    })
    
    # Make prediction
    difficulty_level = model.predict(features)
    
    return difficulty_level[0]  # Return the predicted difficulty level

# Example usage
if __name__ == "__main__":
    word_to_check = "confine"  # Replace with any word you want to check
    difficulty = predict_difficulty(word_to_check)
    print(f"The difficulty level of the word '{word_to_check}' is: {difficulty}")