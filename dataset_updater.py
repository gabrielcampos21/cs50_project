import pickle
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import kaggle
import os
import numpy as np
import pandas as pd

if (not os.path.isdir("pickle_files")):
    os.makedirs("pickle_files")

if (not os.path.isdir("data")):
    os.makedirs("data")

kaggle.api.authenticate()
kaggle.api.dataset_download_files(
    'fronkongames/steam-games-dataset', path='data', unzip=True)

# Removing unnecessary files
os.remove('data/games.json')

# Reading the dataset
df = pd.read_csv('data/games.csv')

# Adding a 'PositiveRate' column
df['PositiveRate'] = df['Positive'] / (df['Positive'] + df['Negative'])

# Dropping null values and games which don't support English language
df = df.drop(df[df['About the game'].isna()].index)
df = df.drop(df[df['Categories'].isna()].index)
df = df.drop(df[df['Genres'].isna()].index)
df = df.drop(df[df['Tags'].isna()].index)
df = df.drop(df[~df['Supported languages'].str.contains('English')].index)

# Limiting the 'About the game' text to 1800 characters (so it won't use too much ram)
# This is optional
# df['About the game'] = df['About the game'].apply(lambda x: x[:1800] if len(x) > 1800 else x)

# Keeping only the year in the 'Release date' label
df['Release date'] = df['Release date'].str[-4:]

# Dropping labels that won't be used
labels_to_drop = ['Reviews', 'Peak CCU',
                  'Required age', 'DLC count',
                  'Full audio languages',
                  'Header image', 'Website', 'Support url', 'Support email', 'Windows',
                  'Mac', 'Linux', 'Metacritic score', 'Metacritic url', 'User score',
                  'Score rank', 'Achievements', 'Recommendations',
                  'Notes', 'Average playtime forever', 'Average playtime two weeks',
                  'Median playtime forever', 'Median playtime two weeks', 'Developers',
                  'Publishers', 'Screenshots', 'Movies']

for label in labels_to_drop:
    df.drop(label, axis=1, inplace=True)

# Filtering non coop games
df = df[df['Categories'].str.contains('Co-op')]
df = df.reset_index(drop=True)


# TF-IDF(Term Frequency Inverse Document Frequency):
# It can be defined as the calculation of how relevant a word is to a text
# Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')

# Fits the TF-IDF vectorizer on the 'About the game' column of the df DataFrame,
# which means it learns the vocabulary of the corpus and calculates the term frequencies and inverse document frequencies for each term.
tfidf_matrix = tfidf.fit_transform(df['About the game'])

# Compute the cosine similarity matrix: a square matrix where each element represents the cosine similarity between two documents.
# It's a measure of how similar they are, with a higher cosine similarity indicating greater similarity.
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Construct map of indices and game titles
indices = pd.Series(df.index, index=df['Name']).drop_duplicates()


# Define the filename for the pickle file
PICKLE_FILENAME = 'pickle_files/cosine_similarity_matrix.pkl'

# Save the cosine_sim matrix to a pickle file
with open(PICKLE_FILENAME, 'wb') as pickle_file:
    pickle.dump(cosine_sim, pickle_file)

PICKLE_FILENAME = 'pickle_files/df.pkl'

with open(PICKLE_FILENAME, 'wb') as pickle_file:
    pickle.dump(df, pickle_file)

PICKLE_FILENAME = 'pickle_files/indices.pkl'

with open(PICKLE_FILENAME, 'wb') as pickle_file:
    pickle.dump(indices, pickle_file)


os.remove('data/games.csv')

print('Done!')
