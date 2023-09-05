import spacy
import pandas as pd
import numpy as np

# Load pre-trained word embeddings
nlp = spacy.load("en_core_web_md")

# Define the dataset
data_df = pd.read_excel('IBAS_data_en_bn_same_line.xlsx', sheet_name='Sheet1')

# Handle NaN values in the dataset
data_df['Answer'] = data_df['Answer'].fillna('')

# Convert the dataset to a list
dataset = data_df['Answer'].tolist()

# Get the sentence from the user
user_sentence = input("Enter a sentence: ")

# Calculate the similarity between the user sentence and dataset sentences
matches = [nlp(user_sentence).similarity(nlp(sentence)) for sentence in dataset]

# Set the threshold for similarity
threshold = 0.9

# Check if any sentence in the dataset matches the user sentence
if np.max(matches) > threshold:
    print("1")  # Match found
else:
    print("0")  # No match
