# Steam Co-Op games recommender
#### Name: Gabriel Campos
#### City & Country: Belo Horizonte, Brazil
#### Video Demo:  <URL HERE>
## Description: 
#### My final project is a website that allows users to input a coop game from Steam they like and get a list of similar games which they might like to play. There are also filter options to make the recommendation more relevant to the user, ex.: filtering by the price of the game or year of release. This project uses a [Kaggle Steam games dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/) for the games data.

Tecnologies used: 
- Python:
    - Recommendation system: Pandas, Numpy, Pickle, sklearn 
    - Website: Flask
- HTML
- JavaScript
- JQuery
- CSS
- Bootstrap

## Motivation
I decided to do this project because sometimes I find it hard to search and discover new games. With that problem and a desire to learn more about how recommendation systems work, I had the idea of creating a game recommender system based on coop Steam games.

## Project Files
-  steam-co-op-game-recommender.ipynb -> this is the downloaded Kaggle notebook, which:
    - reads the dataset into memory, drops unnecessary columns and modifies the ones needed and filters non coop games out of the dataframe.
    -  Then it does the calculation of how relevant a word is to a text in the games 'About the game' column and generates a matrix with a measure of how similar two elements are, indicating how similar one game is to another.
    -  After that, these variables are saved into pickle files to be read by other python files.
-  app.py -> Simple python and flask routes controller with 3 routes:
    - '/' (GET) which renders the index page.
    - '/search' (POST) which runs the recommendation function and renders the game recommendations list.
    - '/complete' (POST) which provides the list of autocompletions (game titles) based on what the user is writting.
-  recommender.py -> loads the pickle files into memory (for recommendations) and contains the following functions:
    - complete(provides the list of game titles based on what the user is writting).
    - get_recommendations(returns similar games based on the game name and filter options).

The point of having these pickle files is that I find it more convenient to download the dataset and generate the similarity matrixes on Kaggle, and then downloading them as files to be read by the website recommender python file. This way, I can choose when I want to update the games data and can use Kaggle's computer resources to do that faster.

The Kaggle python notebook also contains a few examples of how the recommendation can be implemented and also how the search function works.
