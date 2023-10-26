import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
    return render_template("home.html", recipes=recipes)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/sign_in")
def sign_in():
    return render_template("sign_in.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


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
