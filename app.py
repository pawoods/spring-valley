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


def get_user(user_id):
    user = mongo.db.users.find_one({"user_id": user_id})
    return user


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
        # check if username and email are already in users collection
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
        elif request.form.get("password") != request.form.get(
                "password_check"):
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
                "password": generate_password_hash(
                    request.form.get("password")),
                "photo_url": request.form.get("photo_url"),
                "is_super": False,
                "is_admin": False}
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
                    existing_user["password"],
                    request.form.get("password")):
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
        return render_template(
            "recipe_details.html",
            recipe=recipe,
            user=user)

    return render_template("recipe_details.html", recipe=recipe)


@app.route("/recipes")
def recipes():
    recipes = mongo.db.recipes.find()
    # if signed in, adds current user to template for use on front end
    if "user" in session:
        user = get_user(session["user"])
        return render_template("recipes.html", recipes=recipes, user=user)

    return render_template("recipes.html", recipes=recipes)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    user = get_user(session["user"])

    if request.method == "POST":
        selected_categories = request.form.getlist("category_name")
        recipe_categories = []
        for category in selected_categories:
            category_object = mongo.db.categories.find_one(
                {"category_name": category})
            recipe_categories.append(category_object)
        # gets ingredients and instructions lists and removed blank entries
        ingredients = request.form.getlist("ingredient")
        filtered_ingredients = [x for x in ingredients if x]

        instructions = request.form.getlist("instruction")
        filtered_instructions = [x for x in instructions if x]

        recipe = {
            "categories": recipe_categories,
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": filtered_ingredients,
            "instructions": filtered_instructions,
            "recipe_description": request.form.get("recipe_description"),
            "created_by": {
                "username": user["username"],
                "user_id": user["user_id"]},
            "serves": request.form.get("serves"),
            "prep_time": request.form.get("prep_time"),
            "cook_time": request.form.get("cook_time"),
            "likes": []}
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe successfully added")
        return redirect(url_for("recipes"))

    categories = mongo.db.categories.find()
    return render_template("add_recipe.html", categories=categories)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    user = get_user(session["user"])

    if request.method == "POST":
        selected_categories = request.form.getlist("category_name")
        recipe_categories = []
        for category in selected_categories:
            category_object = mongo.db.categories.find_one(
                {"category_name": category})
            recipe_categories.append(category_object)
        # gets ingredients and instructions lists and removed blank entries
        ingredients = request.form.getlist("ingredient")
        filtered_ingredients = [x for x in ingredients if x]

        instructions = request.form.getlist("instruction")
        filtered_instructions = [x for x in instructions if x]

        edit = {
            "categories": recipe_categories,
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": filtered_ingredients,
            "instructions": filtered_instructions,
            "recipe_description": request.form.get("recipe_description"),
            "created_by": {
                "username": user["username"],
                "user_id": user["user_id"]},
            "serves": request.form.get("serves"),
            "prep_time": request.form.get("prep_time"),
            "cook_time": request.form.get("cook_time"),
            "likes": []}

        mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {
            "$set": edit})
        flash("Recipe successfully updated")
        return redirect(url_for("recipes"))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find()
    return render_template(
        "edit_recipe.html",
        categories=categories,
        recipe=recipe,
        user=user)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})

    flash("Recipe successfully deleted")
    return redirect(url_for("recipes"))


@app.route("/recipe_like/<recipe_id>/<page>")
def recipe_like(recipe_id, page):
    likes = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})["likes"]
    if session["user"] in likes:
        mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {
            "$pull": {"likes": session["user"]}})
        return redirect(url_for(page))

    mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {
        "$push": {"likes": session["user"]}})
    return redirect(url_for(page))


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
        # Adds new category to the database
        category = {
            "category_name": request.form.get("category_name"),
            "category_description": request.form.get("category_description"),
            "category_color": request.form.get("category_color")}
        mongo.db.categories.insert_one(category)

        flash("New category added!")
        return redirect(url_for("categories"))
    # if signed in, adds current user to template for use on front end
    if "user" in session:
        user = get_user(session["user"])
        return render_template("add_category.html", user=user)

    return render_template


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        # Updates the category in the database
        edit = {
            "category_name": request.form.get("category_name"),
            "category_description": request.form.get("category_description"),
            "category_color": request.form.get("category_color")}
        mongo.db.categories.update_one({"_id": ObjectId(category_id)}, {
            "$set": edit})
        # Updates the category on all applicable recipes in recipe database
        query = {
            "categories._id": ObjectId(category_id)}
        update = {"$set": {
            "categories.$.category_name":
            request.form.get("category_name"),
                "categories.$.category_color":
                    request.form.get("category_color")}}
        mongo.db.tasks.update_many(query, update)

        flash("Category successfully updated")
        return redirect(url_for("categories"))
    # if signed in, adds current user to template for use on front end
    if "user" in session:
        user = get_user(session["user"])
        category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
        return render_template(
            "edit_category.html",
            category=category,
            user=user)
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.recipes.update_many(
        {"categories._id": ObjectId(category_id)},
        {"$pull": {"categories": {"_id": ObjectId(category_id)}}})
    mongo.db.categories.delete_one({"_id": ObjectId(category_id)})

    flash("Category successfully deleted")
    return redirect(url_for("categories"))


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/users")
def users():
    if "user" in session:
        user = get_user(session["user"])
        if user["is_admin"]:
            users = mongo.db.users.find()
            return render_template("users.html", users=users, user=user)
    flash("Access denied to users page")
    return redirect(url_for("home"))


@app.route("/super_user/<user_id>")
def super_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user["is_super"]:
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {
            "$set": {"is_super": False}})
    else:
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {
            "$set": {"is_super": True}})
    return redirect(url_for("users"))


@app.route("/admin_user/<user_id>")
def admin_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user["is_admin"]:
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {
            "$set": {"is_admin": False}})
    else:
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {
            "$set": {"is_admin": True}})
    return redirect(url_for("users"))


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
