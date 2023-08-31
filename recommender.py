import pickle
import pandas as pd

cosine_sim_filename = "cosine_similarity_matrix.pkl"
df_filename = "df.pkl"
indices_filename = "indices.pkl"

with open(cosine_sim_filename, 'rb') as pickle_file:
    cosine_sim = pickle.load(pickle_file)

with open(df_filename, 'rb') as pickle_file:
    df = pickle.load(pickle_file)

with open(indices_filename, 'rb') as pickle_file:
    indices = pickle.load(pickle_file)    

# drop reviews column

# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(name, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    if name not in indices:
      return "Game was not found"
    idx = indices[name]
    #if idx > 35500: return "not in index range"
    if type(idx) == pd.core.series.Series: idx = idx[0]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    game_indices = [i[0] for i in sim_scores]

    print(df.columns)
    # Return the top 10 most similar movies
    return df.iloc[game_indices]

#print(get_recommendations("Unturned"))