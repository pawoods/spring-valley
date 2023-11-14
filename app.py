import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from datetime import datetime
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
    session["url"] = request.url
    new_recipes = mongo.db.recipes.find().sort("created_date", -1).limit(3)
    popular_recipes = mongo.db.recipes.find().sort("likes.count", -1).limit(3)
    # adds current user if signed in
    if "user" in session:
        user = mongo.db.users.find_one({"user_id": session["user"]})
        return render_template(
            "home.html",
            new_recipes=new_recipes,
            popular_recipes=popular_recipes,
            user=user)

    return render_template(
        "home.html",
        new_recipes=new_recipes,
        popular_recipes=popular_recipes)


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
                "f_name": request.form.get("f_name").capitalize(),
                "l_name": request.form.get("l_name").capitalize(),
                "email": request.form.get("email"),
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(
                    request.form.get("password")),
                "user_since": datetime.now(),
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
    session["url"] = request.url
    # if signed in, adds current user to template for use on front end
    if "user" in session:
        user = get_user(session["user"])
        owned_recipes = mongo.db.recipes.find({
            "created_by.user_id": user["user_id"]})
        liked_recipes = mongo.db.recipes.find({
            "likes.id": user["user_id"]})

        return render_template(
            "profile.html",
            owned_recipes=owned_recipes,
            liked_recipes=liked_recipes,
            user=user)


@app.route("/edit_details/<user_id>", methods=["GET", "POST"])
def edit_details(user_id):
    editing = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if "user" in session:
        user = get_user(session["user"])
    if request.method == "POST":
        # check if username and email are already in users collection
        # excluding current user
        existing_user = mongo.db.users.find_one({
            "$and": [{"_id": {"$ne": ObjectId(user_id)}}, {
                "username": request.form.get("username")}]})
        existing_email = mongo.db.users.find_one({
            "$and": [{"_id": {"$ne": ObjectId(user_id)}}, {
                "email": request.form.get("email")}]})

        if existing_user and existing_email:
            flash("Username and email already exist")
            return redirect(url_for(
                "edit_details",
                user_id=user_id))
        elif existing_user:
            flash("Username already exists")
            return redirect(url_for(
                "edit_details",
                user_id=user_id))
        elif existing_email:
            flash("Email already exists")
            return redirect(url_for(
                "edit_details",
                user_id=user_id))

        edit = {
            "f_name": request.form.get("f_name").capitalize(),
            "l_name": request.form.get("l_name").capitalize(),
            "email": request.form.get("email"),
            "username": request.form.get("username").lower(),
            "photo_url": request.form.get("photo_url")
        }
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {
            "$set": edit})

        query = {"created_by.user_id": editing["user_id"]}
        update = {"$set": {
            "created_by.username": request.form.get("username").lower()}}
        mongo.db.recipes.update_many(query, update)
        flash("User details updated successfuly")
        return redirect(session["url"])

    return render_template(
        "edit_details.html",
        editing=editing,
        user=user)


@app.route("/delete_user/<user_id>")
def delete_user(user_id):
    deleted = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    # Remove user from session and recirect to home if they delete themself
    if deleted["user_id"] == session["user"]:
        session.pop("user")
        mongo.db.users.delete_one({"_id": ObjectId(user_id)})
        flash("Account successfully removed")
        return redirect(url_for("home"))

    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    flash("Account successfully removed")
    return redirect(session["url"])


@app.route("/recipe_details/<recipe_id>")
def recipe_details(recipe_id):
    session["url"] = request.url
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
    session["url"] = request.url
    recipes = mongo.db.recipes.find().sort("recipe_name", 1)
    # if signed in, adds current user to template for use on front end
    if "user" in session:
        user = get_user(session["user"])
        return render_template("recipes.html", recipes=recipes, user=user)

    return render_template("recipes.html", recipes=recipes)


@app.route("/filter_recipes/<category_name>")
def filter_recipes(category_name):
    session["url"] = request.url
    recipes = mongo.db.recipes.find({
        "categories.category_name": category_name})
    if "user" in session:
        user = get_user(session["user"])
        return render_template(
            "filter_recipes.html",
            recipes=recipes,
            category_name=category_name,
            user=user)

    return render_template(
        "filter_recipes.html",
        recipes=recipes,
        category_name=category_name)


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
            "serves": int(request.form.get("serves")),
            "prep_time": int(request.form.get("prep_time")),
            "cook_time": int(request.form.get("cook_time")),
            "photo_url": request.form.get("photo_url"),
            "likes": {
                "count": 0,
                "id": []},
            "created_date": datetime.now()}
        mongo.db.recipes.insert_one(recipe)
        # returns the _id of the newly created recipe to use in the redirect
        new_recipe_id = mongo.db.recipes.find_one(recipe)["_id"]
        flash("Recipe successfully added")
        return redirect(url_for("recipe_details", recipe_id=new_recipe_id))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "add_recipe.html",
        categories=categories,
        user=user)


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
            "serves": int(request.form.get("serves")),
            "prep_time": int(request.form.get("prep_time")),
            "cook_time": int(request.form.get("cook_time")),
            "photo_url": request.form.get("photo_url")}

        mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {
            "$set": edit})
        flash("Recipe successfully updated")
        return redirect(session["url"])

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "edit_recipe.html",
        categories=categories,
        recipe=recipe,
        user=user)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
    flash("Recipe successfully deleted")
    # Redirects the user to recipes page if they
    # delete the recipe they were viewing in detail 
    if session["url"].split("/")[-1] == request.url.split("/")[-1]:
        return redirect(url_for("recipes"))
    return redirect(session["url"])


@app.route("/recipe_like/<recipe_id>")
def recipe_like(recipe_id):
    likes = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})["likes"]
    if session["user"] in likes["id"]:
        new_count = likes["count"]-1
        mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {
            "$pull": {"likes.id": session["user"]},
            "$set": {"likes.count": new_count}})
        return redirect(session["url"])

    new_count = likes["count"]+1
    mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {
        "$push": {"likes.id": session["user"]},
        "$set": {"likes.count": new_count}})
    return redirect(session["url"])


@app.route("/categories")
def categories():
    categories = mongo.db.categories.find().sort("category_name", 1)
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
    user = get_user(session["user"])

    if request.method == "POST":
        # Adds new category to the database
        category = {
            "category_name": request.form.get("category_name"),
            "category_description": request.form.get("category_description"),
            "category_color": request.form.get("category_color")}
        mongo.db.categories.insert_one(category)

        flash("New category added!")
        return redirect(url_for("categories"))

    return render_template("add_category.html", user=user)


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    user = get_user(session["user"])
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
            "categories.$.category_description":
            request.form.get("category_description"),
            "categories.$.category_color":
            request.form.get("category_color")}
        }
        mongo.db.recipes.update_many(query, update)

        flash("Category successfully updated")
        return redirect(url_for("categories"))

    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template(
        "edit_category.html",
        category=category,
        user=user)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.recipes.update_many(
        {"categories._id": ObjectId(category_id)},
        {"$pull": {"categories": {"_id": ObjectId(category_id)}}})
    mongo.db.categories.delete_one({"_id": ObjectId(category_id)})

    flash("Category successfully deleted")
    return redirect(url_for("categories"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        message = {
            "user_name": request.form.get("name"),
            "user_email": request.form.get("email"),
            "message_content": request.form.get("message"),
            "message_date": datetime.now()}
        mongo.db.messages.insert_one(message)
        flash("Thanks for your message, "
              "we will look to respond in the next 48 hours.")
        return redirect(url_for("home"))

    if "user" in session:
        user = get_user(session["user"])
        return render_template("contact.html", user=user)
        
    return render_template("contact.html")


@app.route("/users")
def users():
    session["url"] = request.url
    if "user" in session:
        user = get_user(session["user"])
        if user["is_admin"]:
            users = mongo.db.users.find().sort("username", 1)
            return render_template("users.html", users=users, user=user)
    # Redirects non-admin users back home with "Access denied" flash
    flash("Access denied to users page")
    return redirect(url_for("home"))

@app.route("/messages")
def messages():
    if "user" in session:
        user = get_user(session["user"])
        if user["is_admin"]:
            messages = mongo.db.messages.find().sort("date", -1)
            return render_template("messages.html", messages=messages, user=user)
    # Redirects non-admin users back home with "Access denied" flash
    flash("Access denied to messages page")
    return redirect(url_for("home"))


@app.route("/delete_message/<message_id>")
def delete_message(message_id):
    mongo.db.messages.delete_one({"_id": ObjectId(message_id)})
    flash("Message successfully deleted")
    return redirect(url_for("messages"))


@app.route("/super_user/<user_id>")
def super_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user["is_super"]:
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {
            "$set": {"is_super": False}})
    else:
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {
            "$set": {"is_super": True}})
    return redirect(session["url"])


@app.route("/admin_user/<user_id>")
def admin_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user["is_admin"]:
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {
            "$set": {"is_admin": False}})
    else:
        mongo.db.users.update_one({"_id": ObjectId(user_id)}, {
            "$set": {"is_admin": True}})
    return redirect(session["url"])


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
