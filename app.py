from flask import Flask, render_template, request, redirect, url_for, session, make_response, Response, jsonify
import requests, urllib.request, sqlite3, json

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user


app = Flask(__name__, static_url_path="/static")
app.secret_key = b'##########'

login_manager = LoginManager()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):   
    def __init__(self, name, id, active):
        self.name = name
        self.id = str(id)
        self.active = active                

    def is_authenticated(self):
        return True

    def is_active(self):   
        return self.active           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)





@login_manager.user_loader
def load_user(user_id):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `users` WHERE `id` = ?", (user_id))
    results = cursor.fetchall()
    connection.close()

    UserObject = User(results[0][1], user_id, True)
    if UserObject.get_id() == user_id:
        return UserObject
    else:
        return None



@app.route('/login', methods=['POST'])
def login():
  if request.method == "POST":
    data = request.get_json()

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `users` WHERE `username` = ? AND `password` = ?", (data["username"], data["pass"]))
    results = cursor.fetchall()
    connection.close()

    if results != []:
        result_id = str(results[0][0])
        UserObject = User(results[0][1], result_id, active=True)
        login_user(UserObject)

        if not results:
            return jsonify(status="0")
        else:
            return jsonify(status="1", username=UserObject.name, id=UserObject.id)
    else:
        return jsonify(status="0")

    
    
@app.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(status="1")






@app.route('/register-user', methods=['POST'])
def register_user():
  if request.method == "POST":
    data = request.get_json()

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (data["username"], data["email"], data["pass"]))
    connection.commit()
    connection.close()
    
    return jsonify(status="1")
  

@app.route('/check-username', methods=['POST'])
def check_username():
  if request.method == "POST":
    data = (request.get_json())

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT EXISTS (SELECT 1 FROM users WHERE username = ?)", (data["username"],))
    
    if cursor.fetchone()[0]:
        connection.close()
        return jsonify(status="1")
    else:
        connection.close()
        return jsonify(status="0")
    
    
    



@app.route("/")
def home_page():
    return render_template("base.html")



@app.route("/search/", methods=["POST"])
def search():
    url = "https://tasty.p.rapidapi.com/recipes/list"
    headers = {
	"X-RapidAPI-Key": "",
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
	"X-RapidAPI-Key": "",
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




@app.route("/search/<slug>")
def topics(slug):
    pass
    url = "https://tasty.p.rapidapi.com/recipes/get-more-info"
    headers = {
	"X-RapidAPI-Key": "",
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

