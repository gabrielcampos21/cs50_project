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
    return render_template("index.html")

app.run(debug=True)