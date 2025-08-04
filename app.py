from flask import Flask, render_template, jsonify
from court_scraper import fetch_case_table

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scrape")
def scrape():
    data = fetch_case_table()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
