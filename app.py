import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    recipes = mongo.db.recipes.find()
    # adds current user if signed in
    if session:
        user = mongo.db.users.find_one({"user_id": session["user"]})
        return render_template("home.html", recipes=recipes, user=user)

    return render_template("home.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username is already in users collection
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # adds unique id to new user
        user_id = 1
        existing_id = True
        while existing_id:
            if not mongo.db.user.find_one({"user_id": user_id}):
                existing_id = False
                break
            user_id += 1

        # builds new user dict with default superuser and admin permissions
        new_user = {
            "user_id": user_id,
            "f_name": request.form.get("f_name"),
            "l_name": request.form.get("l_name"),
            "email": request.form.get("email"),
            "username": request.form.get("username"),
            "password": generate_password_hash(request.form.get("password")),
            "photo_url": request.form.get("photo_url"),
            "is_super": False,
            "is_admin": False
        }
        mongo.db.users.insert_one(new_user)

        # puts new user id into session cookie
        session["user"] = user_id
        flash("Successfully Registered!")
        return redirect(url_for("profile", user=session["user"]))

    return render_template("register.html")


@app.route("/sign_in")
def sign_in():
    return render_template("sign_in.html")


@app.route("/profile")
def profile():
    # pulls current user from datatbase using id from session cookie
    user = mongo.db.users.find_one({"user_id": session["user"]})
    return render_template("profile.html", user=user)


@app.route("/edit_details")
def edit_details():
    return render_template("edit_details.html")


@app.route("/recipe_details")
def recipe_details():
    return render_template("recipe_details.html")


@app.route("/recipes")
def recipes():
    return render_template("recipes.html")


@app.route("/add_recipe")
def add_recipe():
    return render_template("add_recipe.html")


@app.route("/edit_recipe")
def edit_recipe():
    return render_template("edit_recipe.html")


@app.route("/categories")
def categories():
    return render_template("categories.html")


@app.route("/add_category")
def add_category():
    return render_template("add_category.html")


@app.route("/edit_category")
def edit_category():
    return render_template("edit_category.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/users")
def users():
    return render_template("users.html")


@app.route("/sign_out")
def sign_out():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
