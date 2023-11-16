# Steam Co-Op games recommender
#### Name: Gabriel Campos
#### City & Country: Belo Horizonte, Brazil
#### Video Demo:  [YouTube](https://youtu.be/OgmhahIGl4Q)
## Description: 
My final project is a website that allows users to input a coop game from Steam they like and get a list of similar games they might enjoy playing. There are also filter options to make the recommendations more relevant to the user, such as filtering by the price of the game or year of release. This project utilizes a [Kaggle Steam games dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/) for the games data.

## Tecnologies used: 
- Python:
    - Recommendation System: Pandas, Numpy, Pickle, sklearn 
    - Website: Flask
- HTML, JavaScript, CSS
- Bootstrap

## Motivation
I decided to do this project because I often find it challenging to search and discover new games. With that problem 
in mind and a desire to learn more about how recommendation systems work, I came up with the idea of creating a game recommender system based on cooperative Steam games.
## Learning Resources
- [Kaggle Learn courses](https://www.kaggle.com/learn)
- [Kaggle Competitions](https://www.kaggle.com/competitions)
- [Kaggle notebooks on recommendation systems](https://www.kaggle.com/search?q=recommendation)


## Project Files
-  **dataset_updater.ipynb:**
    - Uses Kaggle's API to download and extract the dataset.
    - Reads the dataset into memory, drops unnecessary columns, modifies the needed ones, and filters out non-coop games from the dataframe.
    - Calculates the relevance of words in the games' 'About the game' column and generates a matrix indicating the similarity between two elements, showing how similar one game is to another.
    - Saves these variables into pickle files to be read by other Python files.
- **dataset_updater.py**:
   - Performs the same tasks as the Jupyter notebook (dataset_updater.ipynb) but without demonstrations. Another option to update the dataset.
-  **app.py:**
    - Simple Python and Flask routes controller with 3 routes:
        - `/` (GET) renders the index page.
        - `/search` (POST) runs the recommendation function and renders the game recommendations list.
        - `/complete` (POST) provides the list of autocompletions (game titles) based on what the user is writing.
-  **recommender.py:**
    - Loads the pickle files into memory (for recommendations) and contains the following functions:
        - `complete`: provides the list of game titles based on what the user is writing.
        - `get_title_id`: returns the Steam AppId from the title.
        - `get_recommendations`: returns similar games based on the game name and filter options.

The use of pickle files allows me to download the dataset and generate similarity matrices on demand, providing flexibility in updating the games data.


## Usage
1. Configure Kaggle API credentials:
    - Kaggle API Documentation: To use the Kaggle API, sign up for a Kaggle account at [https://www.kaggle.com](https://www.kaggle.com). Then go to the 'Account' tab of your user profile ([https://www.kaggle.com/account](https://www.kaggle.com/account)) and select 'Create API Token'. This will trigger the download of kaggle.json, a file containing your API credentials. Place this file in the location ~/.kaggle/kaggle.json (on Windows in the location C:\Users\<Windows-username>\.kaggle\kaggle.json - you can check the exact location, sans drive, with `echo %HOMEPATH%`).

2. Clone the repository:
    ```bash
    git clone https://github.com/gabrielcampos21/cs50_project
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the dataset updater:
    ```bash
    python3 dataset_updater.py
    ```

5. Run the Flask application:
    ```bash
    python3 app.py
    ```

6. Open a browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
