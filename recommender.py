import pickle
import pandas as pd

COSINE_SIM_FILENAME = "pickle_files/cosine_similarity_matrix.pkl"
DF_FILENAME = "pickle_files/df.pkl"
INDICES_FILENAME = "pickle_files/indices.pkl"

# Loading the files into memory
with open(COSINE_SIM_FILENAME, 'rb') as pickle_file:
    cosine_sim = pickle.load(pickle_file)

with open(DF_FILENAME, 'rb') as pickle_file:
    df = pickle.load(pickle_file)

with open(INDICES_FILENAME, 'rb') as pickle_file:
    indices = pickle.load(pickle_file)


# Autocomplete function
def complete(text):
    return indices[indices.index.str.find(text) != -1]


# Function that takes in game title as input and outputs top x most similar games
def get_recommendations(name, min_rating=0, min_reviews=0, max_price=None, min_release_year=None, max_release_year=None, recommendations_count=10, cosine_sim=cosine_sim):
    # Get the index of the game that matches the title
    if name not in indices:
        return None
    idx = indices[name]

    if type(idx) == pd.core.series.Series:
        idx = idx[0]

    # Get the pairwise similarity scores of all games with that game
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the games based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    game_indices = [i[0] for i in sim_scores]
    games = df.iloc[game_indices]

    filtered_games = games[(games.apply(lambda row: (
        (max_price == 'free' and float(row['Price']) == 0) or
        (max_price == 'paid' and float(row['Price']) > 0) or
        (max_price == 'any')
    ), axis=1))]
    filtered_games = filtered_games[(filtered_games['PositiveRate'] >= float(min_rating)/10) &
                                    ((filtered_games['Negative'] + filtered_games['Positive']) >= int(min_reviews)) &
                                    (filtered_games['Release date'] >= min_release_year) &
                                    (filtered_games['Release date'] < max_release_year)]

    filtered_games = filtered_games[1:recommendations_count+1]

    # Return the top similar games
    return filtered_games.iloc()
