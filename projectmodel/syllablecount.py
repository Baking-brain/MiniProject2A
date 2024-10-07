#testing the syllable count

import pandas as pd
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

# Load the dataset (assuming it has a 'word' column)
data = pd.read_csv("modeltraining/train_data.csv")  # Use the correct path to your CSV file

# Ensure 'word' column is treated as strings
data['word'] = data['Word'].astype(str)  # Adjust if necessary based on your column name

# Print only the syllable count for each word
for word in data['word']:
    print(syllable_count(word))