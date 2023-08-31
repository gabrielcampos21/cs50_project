import recommender
from flask import Flask, flash, redirect, render_template, request

app = Flask(__name__)
app.secret_key="12345"

@app.route("/search", methods=["POST"])
def search():
    games = recommender.get_recommendations(request.form.get('title'))
    return render_template("search.html", title=request.form.get('title'), games = games)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

app.run(debug=True)