from flask import Flask,request, render_template, redirect
from scrapers.extractors import extract_bsj_jobs, extract_wwr_jobs, extract_ssd_jobs


# Initialize the Flask app
app = Flask(__name__)

# In-memory database to store job data temporarily
db = {}

# Function to get job data and store both raw data and its length in db
def length_result(keyword):
    bsj = extract_bsj_jobs(keyword)
    wwr = extract_wwr_jobs(keyword)
    ssd = extract_ssd_jobs(keyword)

    # Save the raw job data per site under the keyword
    db[keyword] = {
        "bsj": bsj,
        "wwr": wwr,
        "ssd": ssd
    }

    # Save the number of job results for each source
    result = {
        "bsj": len(bsj),
        "wwr": len(wwr),
        "ssd": len(ssd)
    }
    db[f"{keyword}_length"] = result

    return result


# Route for the homepage
@app.route("/")
def home():
    return render_template("index.html", results={})


# Route for search results
@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword is None:
        return redirect("/")

    # Use cached result if available
    if f"{keyword}_length" in db:
        results = db[f"{keyword}_length"]
    else:
        results = length_result(keyword)

    return render_template("index.html", results=results)


# Route to show detailed job listings per site
@app.route("/result")
def result():
    site = request.args.get("site")
    keyword = request.args.get("keyword")

    # Retrieve jobs for the selected site and keyword
    if site in ["bsj", "wwr", "ssd"]:
        jobs = db.get(keyword, {}).get(site, [])
    else:
        jobs = []

    return render_template("result.html", jobs=jobs, site=site, keyword=keyword)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
