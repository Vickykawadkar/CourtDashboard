from flask import Flask, render_template, request
from court_scraper import fetch_case_data
from database import log_query

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    case_data = None
    error_message = None

    if request.method == "POST":
        case_type = request.form.get("case_type")
        case_number = request.form.get("case_number")
        filing_year = request.form.get("filing_year")

        try:
            case_data = fetch_case_data(case_type, case_number, filing_year)
            log_query(case_type, case_number, filing_year, case_data)
        except Exception as e:
            error_message = str(e)

    return render_template("index.html", case_data=case_data, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
