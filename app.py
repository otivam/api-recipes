from flask import Flask, render_template, request, redirect, url_for, session, make_response, Response
import requests, urllib.request

app = Flask(__name__, static_url_path="/static")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'







@app.route("/")
def home_page():
    return render_template("base.html")



@app.route("/search/", methods=["POST"])
def search():
    url = "https://tasty.p.rapidapi.com/recipes/list"
    headers = {
	"X-RapidAPI-Key": "2ad60a66c2msh449e56015dac732p1a7c37jsn1403adeafdd5",
	"X-RapidAPI-Host": "tasty.p.rapidapi.com"
    }
    data_ingridients = request.form["ingridients"]
    all_recipes_sorted = []
    querystring = {"from":"0","size":"100","q":data_ingridients}
    response = requests.request("GET", url, headers=headers, params=querystring)
    all_recipes = response.json()["results"]
    cc = 10
    cc_page = 1


    for recipe in all_recipes:
        with urllib.request.urlopen(recipe["original_video_url"]) as resp:
            info = resp.info()
            if info.get_content_type() == "binary/octet-stream":
                recipe["original_video_url"] = ""


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

    session['all_recipes_sorted'] = all_recipes_sorted

    return render_template("base.html",
                            recipes = all_recipes_sorted,
                            pagination = "True",
                            cc_page = cc_page
                            )




@app.route("/search/<recipe_id>")
def recipe_details(recipe_id):
    url = "https://tasty.p.rapidapi.com/recipes/get-more-info"
    headers = {
	"X-RapidAPI-Key": "2ad60a66c2msh449e56015dac732p1a7c37jsn1403adeafdd5",
	"X-RapidAPI-Host": "tasty.p.rapidapi.com"
    }
    querystring = {"id":str(recipe_id)}
    response = requests.get(url, headers=headers, params=querystring)
    json_response = response.json()

    with urllib.request.urlopen(json_response["original_video_url"]) as resp:
        info = resp.info()
        if info.get_content_type() == "binary/octet-stream":
            json_response["original_video_url"] = ""
            
    return render_template('recipe.html', recipe=json_response)

"""
@app.route('/get_recipe_video', methods=['POST'])
def get_recipe_video():
  if request.method == "POST":
    recipe_id = request.get_data(cache=False).decode('UTF-8')
    
    url = "https://tasty.p.rapidapi.com/recipes/get-more-info"
    headers = {
	"X-RapidAPI-Key": "2ad60a66c2msh449e56015dac732p1a7c37jsn1403adeafdd5",
	"X-RapidAPI-Host": "tasty.p.rapidapi.com"
    }
    querystring = {"id":str(recipe_id)}
    response = requests.get(url, headers=headers, params=querystring)
    video_url = response.json()["original_video_url"]

    resp = Response(video_url)
    resp.headers["Content-Type"] = "video/mp4"
    
    return resp
"""


@app.route("/search/<slug>")
def topics(slug):
    pass
    url = "https://tasty.p.rapidapi.com/recipes/get-more-info"
    headers = {
	"X-RapidAPI-Key": "2ad60a66c2msh449e56015dac732p1a7c37jsn1403adeafdd5",
	"X-RapidAPI-Host": "tasty.p.rapidapi.com"
    }
    querystring = {"id":str(recipe_id)}
    response = requests.get(url, headers=headers, params=querystring)
    json_response = response.json()

    with urllib.request.urlopen(json_response["original_video_url"]) as resp:
        info = resp.info()
        if info.get_content_type() == "binary/octet-stream":
            json_response["original_video_url"] = ""
            
    return render_template('recipe.html', recipe=json_response)

    

if __name__ == "__main__":
    app.run(debug=True)

