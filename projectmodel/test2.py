import pandas as pd

# Load the dataset (assuming it has columns: word, difficulty, frequency)
data = pd.read_csv(r'modeltraining/wholewordset.csv')

# Group by difficulty and sample 80 words from each level for testing data
test_data = data.groupby('diff_level').apply(lambda x: x.sample(n=80, random_state=42))

# Remove the sampled words from the original data to create the training data
train_data = data.loc[~data.index.isin(test_data.index)]

# Check the shapes of train and test data
print(f"Training Data: {train_data.shape}")
print(f"Testing Data: {test_data.shape}")

# Optionally, shuffle the data (if needed)
train_data = train_data.sample(frac=1, random_state=42).reset_index(drop=True)
test_data = test_data.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the datasets if needed
train_data.to_csv('train_data.csv', index=False)
test_data.to_csv('test_data.csv', index=False)

print("Data split into training and testing sets complete!")