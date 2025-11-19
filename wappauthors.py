from flask import Flask, render_template, request, redirect, url_for
import requests

API_URL = "http://127.0.0.1:5000/authors"

app = Flask(__name__)

"""
 response = requests.get(API_URL)
authors = response.json()
return render_template("index.html", authors=authors)
"""

# List authors
@app.route("/")
def index():
    response = requests.get(API_URL)
    authors = response.json().get("authors", [])
    return render_template("index.html", authors=authors)


# Add author
@app.route("/add", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "specialisation": request.form["specialisation"]
        }
        requests.post(API_URL, json=data)
        return redirect(url_for("index"))
    return render_template("add.html")

# Edit author
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_author(id):
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "specialisation": request.form["specialisation"]
        }
        requests.put(f"{API_URL}/{id}", json=data)
        return redirect(url_for("index"))

    author = requests.get(f"{API_URL}/{id}").json()
    return render_template("edit.html", author=author)

# Delete author
@app.route("/delete/<int:id>")
def delete_author(id):
    requests.delete(f"{API_URL}/{id}")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000, debug=True)
