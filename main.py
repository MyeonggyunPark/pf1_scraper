from flask import Flask,request, render_template
from scrapers.extractors import extract_bsj_jobs, extract_wwr_jobs, extract_ssd_jobs


# Initialize the Flask app
app = Flask(__name__)


# Helper function that returns the number of job postings from each source
def length_result(keyword):
    bsj = extract_bsj_jobs(keyword)
    wwr = extract_wwr_jobs(keyword)
    ssd = extract_ssd_jobs(keyword)

    result = {
        "bsj": len(bsj),
        "wwr": len(wwr),
        "ssd": len(ssd)
    }
    return result


# Route for the homepage
@app.route("/")
def home():
    return render_template("index.html", results={})


# Route for search results
@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    results = length_result(keyword)
    return render_template("index.html", results=results)


# Run the Flask app 
if __name__ == "__main__":
    app.run(debug=True)
