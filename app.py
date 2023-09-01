import recommender
from flask import Flask, flash, redirect, render_template, request, jsonify

app = Flask(__name__)
app.secret_key="12345"

@app.route('/complete', methods=['POST'])
def complete():
    search_term = request.form.get('search')
    autocomplete_results = recommender.complete(search_term)
    suggestions = autocomplete_results.index.str.contains(search_term, case=False)
    filtered_suggestions = autocomplete_results.index[suggestions]
    
    return jsonify(list(filtered_suggestions))

@app.route("/search", methods=["POST"])
def search():
    games = recommender.get_recommendations(request.form.get('title'))
    return render_template("search.html", title=request.form.get('title'), games = games)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", player_counts = ['1 Player', '2 Players', '3+ Players'], languages=recommender.get_all_languages())


# TODO
# Filter by year of release 'Release date'
# Filter by number of owners 'Estimated owners'
# Filter by number of users rates 'Positive' + 'Negative'
# Filter by minimum positive rate 'Positive' / 'Positive' + 'Negative'
# Filter by category/tags 'Categories' 'Tags'
# Filter by language 'Supported languages'
# Filter by game genre 'Genres'
# Filter by price 'Price'

app.run(debug=True)