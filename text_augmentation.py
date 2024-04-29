import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import random

import sys
sys.path.append("/home/zubair/workstation_2/")

nltk.download('punkt')
nltk.download('wordnet')

def synonym_replacement(words, n):
    new_words = words.copy()
    random_word_list = list(set([word for word in words if word.isalpha()]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = get_synonyms(random_word)
        if len(synonyms) > 0:
            synonym = random.choice(synonyms)
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n:
            break
    sentence = ' '.join(new_words)
    return sentence

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace("_", " ").replace("-", " ").lower()
            synonym = "".join([char for char in synonym if char.isalpha()])
            if synonym != word:
                synonyms.append(synonym)
    return list(set(synonyms))

def augment_sentence(sentence, n=10):
    augmented_sentences = [sentence]
    words = word_tokenize(sentence)
    for _ in range(n-1):
        augmented_sentences.append(synonym_replacement(words, 1))
    
    # Shuffle the entire set of augmented sentences
    random.shuffle(augmented_sentences)
    return augmented_sentences

def augment_data(input_file, output_file):
    df = pd.read_excel(input_file)

    augmented_data = {'bangla_ques': [], 'transliterated_ques': [], 'english_ques': []}

    for index, row in df.iterrows():
        bangla_question = row['bangla_ques']
        transliterated_question = row['transliterated_ques']
        english_question = row['english_ques']

        augmented_bangla = augment_sentence(bangla_question, 10)
        augmented_transliterated = augment_sentence(transliterated_question, 10)
        augmented_english = augment_sentence(english_question, 10)

        augmented_data['bangla_ques'].extend(augmented_bangla)
        augmented_data['transliterated_ques'].extend(augmented_transliterated)
        augmented_data['english_ques'].extend(augmented_english)

    augmented_df = pd.DataFrame(augmented_data)
    augmented_df.to_excel(output_file, index=False)

if __name__ == "__main__":
    input_file = "/home/zubair/workstation_2/source/Final-updated-dataset.xlsx"  # Change this to the path of your input file
    output_file = "/home/zubair/workstation_2/source/Final-updated-augmented-dataset.xlsx"  # Change this to the desired output file name
    augment_data(input_file, output_file)
