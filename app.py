import recommender
from flask import Flask, flash, redirect, render_template, request

app = Flask(__name__)
app.secret_key="12345"


@app.route("/search", methods=["POST"])
def search():
    recommendations = recommender.get_recommendations(request.form.get('title'))
    return render_template("search.html")
    #return (str(recommender.get_recommendations(request.form.get('title'))))
    #return redirect('/')

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

app.run()