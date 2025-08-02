from flask import Flask, render_template, request, jsonify
from court_scraper import fetch_case_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scrape", methods=["POST"])
def scrape():
    case_type = request.form.get("case_type")
    case_number = request.form.get("case_number")
    case_year = request.form.get("case_year")

    data = fetch_case_data(case_type, case_number, case_year)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
