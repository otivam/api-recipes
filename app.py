from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__, static_url_path="/static")
url = "https://tasty.p.rapidapi.com/recipes/list"
headers = {
	"X-RapidAPI-Key": "2ad60a66c2msh449e56015dac732p1a7c37jsn1403adeafdd5",
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
    cc = 10
    cc_page = 1
    pagination = ""
    all_recipes_sorted = []

    if response.json()["count"] > 0:
        all_recipes = response.json()["results"]
        pagination = "True"

        for recipe in all_recipes:
            if recipe["description"] == "" or recipe["description"] == None:
                all_recipes_sorted.append(recipe)
            else:
                all_recipes_sorted.insert(0,recipe)

        for i, recipe in enumerate(all_recipes_sorted):
            recipe["page"] = cc_page
            cc -= 1

            if i != len(all_recipes_sorted)-1:
                if cc == 0:
                    cc = 10
                    cc_page += 1

    return render_template(
        "base.html",
        recipes = all_recipes_sorted,
        pagination = pagination,
        cc_page = cc_page
    )

if __name__ == "__main__":
    app.run(debug=True)

