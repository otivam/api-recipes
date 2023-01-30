from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__, static_url_path="/static")

url = "https://tasty.p.rapidapi.com/recipes/list"

headers = {
	"X-RapidAPI-Key": "",
	"X-RapidAPI-Host": "tasty.p.rapidapi.com"
}

@app.route("/")
def home_page():
    return render_template("base.html")

@app.route("/search/", methods=["POST"])
def search():
    data_ingridients = request.form["ingridients"]

    querystring = {"from":"0","size":"100","q":data_ingridients}
    response = requests.request("GET", url, headers=headers, params=querystring)
    all_recipes = response.json()["results"]
    all_recipes_sorted = []
    cc = 10
    cc_page = 1

    for recipe in all_recipes:
        if recipe["description"] == "" or recipe["description"] == None:
            all_recipes_sorted.append(recipe)
        else:
            all_recipes_sorted.insert(0,recipe)

    for recipe in all_recipes_sorted:
        recipe["page"] = cc_page
        cc -= 1

        if cc == 0:
            cc = 10
            cc_page += 1


    return render_template(
        "base.html",
        recipes = all_recipes_sorted,
        pagination = "True"
    )

if __name__ == "__main__":
    app.run(debug=True)

