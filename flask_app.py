from flask import Flask, request, redirect, render_template
import json

app = Flask(__name__)

def load_jobs():
    try:
        with open("jobs.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_jobs(jobs):
    with open("jobs.json", "w") as file:
        json.dump(jobs, file, indent=4)

@app.route("/", methods=["GET", "POST"])
def home():
    jobs = load_jobs()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            company = request.form.get("company")
            role = request.form.get("role")
            jobs.append({
                "company": company,
                "role": role,
                "status": "Applied"
            })
            save_jobs(jobs)

        elif action == "update":
            company = request.form.get("company")
            status = request.form.get("status")
            for job in jobs:
                if job["company"] == company:
                    job["status"] = status
                    break
            save_jobs(jobs)

        return redirect("/")

    return render_template("index.html", jobs=jobs)

if __name__ == "__main__":
    app.run(debug=True)

