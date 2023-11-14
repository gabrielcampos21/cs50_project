import recommender
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/complete', methods=['POST'])
def complete():
    search_term = request.get_json().get('search')
    autocomplete_results = recommender.complete(search_term)
    suggestions = autocomplete_results.index.str.contains(
        search_term, case=False)
    filtered_suggestions = autocomplete_results.index[suggestions]

    return jsonify(list(filtered_suggestions))


@app.route("/search", methods=["POST"])
def search():
    games = recommender.get_recommendations(name=request.form.get('title'),
                                            min_rating=request.form.get(
                                                'min-score-rate'),
                                            min_reviews=request.form.get(
                                                'min-reviews'),
                                            max_price=request.form.get(
                                                'max_price'),
                                            min_release_year=request.form.get(
                                                'release-date-start'),
                                            max_release_year=request.form.get(
                                                'release-date-end'),
                                            recommendations_count=int(request.form.get('recommendations_count')))

    return render_template("search.html", title=request.form.get('title'), games=games)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


app.run(debug=True)
