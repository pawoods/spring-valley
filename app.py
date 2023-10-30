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
    if "user" in session:
        user = mongo.db.users.find_one({"user_id": session["user"]})
        return render_template("home.html", recipes=recipes, user=user)

    return render_template("home.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username is already in users collection
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get("email")})

        if existing_user and existing_email:
            flash("Username and email already exist")
            return redirect(url_for("register"))
        elif existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        elif existing_email:
            flash("Email already exists")
            return redirect(url_for("register"))
        elif request.form.get("password") != request.form.get("password_check"):
            flash("Passwords do not match")
            return redirect(url_for("register"))
        else:
            # adds unique id to new user
            user_id = 1
            existing_id = True
            while existing_id:
                if not mongo.db.users.find_one({"user_id": user_id}):
                    existing_id = False
                    break
                else:
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
            return redirect(url_for("profile"))

    return render_template("register.html")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        # checks if email exists on user in database
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email")})

        if existing_user:
            # checks password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                # puts signed in user id into session cookie
                session["user"] = existing_user["user_id"]
                flash("Welcome, {}".format(
                    existing_user["username"]))
                return redirect(url_for(
                    "profile"))
            else:
                # Incorrect password
                flash("Incorrect email and/or password")
                return redirect(url_for("sign_in"))
        else:
            # Incorrect email address
            flash("Incorrect email and/or password")
            return redirect(url_for("sign_in"))

    return render_template("sign_in.html")


def get_user(user_id):
    user = mongo.db.users.find_one({"user_id": user_id})
    return user


@app.route("/profile")
def profile():
    # if signed in, adds current user to template for use on front end
    if "user" in session:
        user = get_user(session["user"])
        return render_template("profile.html", user=user)


@app.route("/edit_details")
def edit_details():
    return render_template("edit_details.html")


@app.route("/recipe_details/<recipe_id>", methods=["GET", "POST"])
def recipe_details(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    # if signed in, adds current user to template for use on front end
    if "user" in session:
        user = get_user(session["user"])
        return render_template("recipe_details.html", recipe=recipe, user=user)

    return render_template("recipe_details.html", recipe=recipe)


@app.route("/recipes")
def recipes():
    recipes = mongo.db.recipes.find()
    # if signed in, adds current user to template for use on front end
    if "user" in session:
        user = get_user(session["user"])
        return render_template("recipes.html", recipes=recipes, user=user)

    return render_template("recipes.html", recipes=recipes)


@app.route("/add_recipe")
def add_recipe():
    return render_template("add_recipe.html")


@app.route("/edit_recipe")
def edit_recipe():
    return render_template("edit_recipe.html")


@app.route("/categories")
def categories():
    categories = mongo.db.categories.find()
    # if signed in, adds current user to template for use on front end
    if "user" in session:
        user = get_user(session["user"])
        return render_template(
            "categories.html", 
            categories=categories, 
            user=user)

    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name"),
            "category_description": request.form.get("category_description"),
            "category_color": request.form.get("category_color")
        }
        mongo.db.categories.insert_one(category)
        flash("New category added!")
        return redirect(url_for("categories"))
    # if signed in, adds current user to template for use on front end
    if "user" in session:
        user = get_user(session["user"])
        return render_template("add_category.html", user=user)

    return render_template


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
    # remove user_id from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect("home")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
