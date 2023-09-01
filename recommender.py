import pickle
import pandas as pd

cosine_sim_filename = "cosine_similarity_matrix.pkl"
df_filename = "df.pkl"
indices_filename = "indices.pkl"

all_languages = []

with open(cosine_sim_filename, 'rb') as pickle_file:
    cosine_sim = pickle.load(pickle_file)

with open(df_filename, 'rb') as pickle_file:
    df = pickle.load(pickle_file)

with open(indices_filename, 'rb') as pickle_file:
    indices = pickle.load(pickle_file)    

def complete(text):
    return indices[indices.index.str.find(text) != -1]

def get_all_languages():
    global all_languages
    if (len(all_languages) > 0):
        return all_languages
    
    # Mapping for combining languages
    language_mapping = {
        'Portuguese - Brazil': 'Portuguese',
        'Portuguese - Portugal': 'Portuguese',
        'Spanish - Latin America': 'Spanish',
        'Spanish - Spain': 'Spanish',
    }

    # Iterate through each row in the Series and extend the all_languages list
    for languages in df['Supported languages']:
        languages = languages.replace('[', '').replace(']', '').replace("'", '').split(',')
        languages = [language.strip() for language in languages]
        
        # Apply language mapping
        languages = [language_mapping.get(language, language) for language in languages]
        
        all_languages.extend(languages)

    # Use set to get unique language names
    all_languages = list(set(all_languages))
    all_languages.sort()
    return all_languages

# Function that takes in game title as input and outputs top 10 most similar games
def get_recommendations(name, cosine_sim=cosine_sim):
    # Get the index of the game that matches the title
    if name not in indices:
      return None
    idx = indices[name]
    #if idx > 35500: return "not in index range"
    if type(idx) == pd.core.series.Series: idx = idx[0]

    # Get the pairwsie similarity scores of all games with that game
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the games based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 10 similarity scores
    sim_scores = sim_scores[1:11]

    # Get the games indices
    game_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar games
    return df.iloc[game_indices].iloc()

