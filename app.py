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
    """
    gets user from users DB using user_id passed in
    """
    user = mongo.db.users.find_one({"user_id": user_id})
    return user


@app.route("/")
@app.route("/home")
def home():
    """
    Gets newest three recipes and three most liked recipes, adds url to
    session cookie and user if signed in, returns to home with or without
    the user object depending on if they are signed in
    """
    session["url"] = request.url
    new_recipes = mongo.db.recipes.find().sort("created_date", -1).limit(3)
    popular_recipes = mongo.db.recipes.find().sort("likes.count", -1).limit(3)
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
        """
        Checks if username and email are already in users collection
        and that passwords match, displays relevant flashed messages
        and reloads page until user info is all valid
        """
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
            """
            Adds unique id to new user and stores this id to
            used_id database for future reference in while loop
            """
            user_id = 1
            existing_id = True
            while existing_id:
                if user_id not in mongo.db.used_ids.find_one({
                        "name": "used_ids"})["ids"]:
                    existing_id = False
                    break
                else:
                    user_id += 1

            mongo.db.used_ids.update_one({"name": "used_ids"}, {
                "$push": {"ids": user_id}})

            """
            builds new user dict with default superuser and admin permissions
            """
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

            """puts new user id into session cookie"""
            session["user"] = user_id
            flash("Successfully Registered!")
            return redirect(url_for("profile"))

    """
    If user already signed in, redirects with
    flashed message to their profile page
    """
    if "user" in session:
        flash("You are already registered")
        return redirect(url_for("profile"))

    return render_template("register.html")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        """
        Checks if email exists on user in database and
        checks the input password matches the hashed password
        stored for the user. Puts signed in user into session
        cookie if successful, redirects to sign in with flashed
        message if unsuccessful
        """
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email")})

        if existing_user:
            if check_password_hash(
                    existing_user["password"],
                    request.form.get("password")):
                session["user"] = existing_user["user_id"]
                flash("Welcome, {}".format(
                    existing_user["username"]))
                return redirect(url_for(
                    "profile"))
            else:
                flash("Incorrect email and/or password")
                return redirect(url_for("sign_in"))
        else:
            flash("Incorrect email and/or password")
            return redirect(url_for("sign_in"))

    """
    If user already signed in, redirects with
    flashed message to their profile page
    """
    if "user" in session:
        flash("You are already signed in")
        return redirect(url_for("profile"))

    return render_template("sign_in.html")


@app.route("/cancel")
def cancel():
    if "url" in session:
        return redirect(session["url"])
    return redirect(url_for("home"))


@app.route("/profile")
def profile():
    """
    Puts page url into session cookie, user into session
    cookie if signed in and gets the users liked and owned recipes
    from the database
    """
    session["url"] = request.url
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

    flash("You are not signed in")
    return redirect(url_for("home"))


@app.route("/edit_details/<user_id>", methods=["GET", "POST"])
def edit_details(user_id):
    """
    Gets current user to check if they are admin or the user that
    they are attempting to edit, otherwise redirects to home with
    flashed message if not signed in
    """
    if "user" in session:
        user = get_user(session["user"])
        editing = mongo.db.users.find_one({"_id": ObjectId(user_id)})

        if user["is_admin"] or user["_id"] == editing["_id"]:
            if request.method == "POST":
                """
                Attemps to get a user with the same updated email address
                or username to user in checks later in function
                """
                existing_user = mongo.db.users.find_one({
                    "$and": [{"_id": {"$ne": ObjectId(user_id)}}, {
                        "username": request.form.get("username")}]})
                existing_email = mongo.db.users.find_one({
                    "$and": [{"_id": {"$ne": ObjectId(user_id)}}, {
                        "email": request.form.get("email")}]})
                """
                Checks confirmation password is correct when submitting
                updated user details, flashed message if incorrect
                """
                if not check_password_hash(
                        user["password"],
                        request.form.get("password_confirm")):
                    flash("Incorrect password")
                    return redirect(url_for(
                        "edit_details",
                        user_id=user_id))
                """
                Check if username and email are already in users
                collection excluding current user so as not to allow
                multiple users to have the same email when updating details,
                checks both new passwords match, builds user object with new
                details from request form
                """
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
                elif request.form.get("password") != request.form.get(
                        "password_check"):
                    flash("Passwords do not match")
                    return redirect(url_for(
                        "edit_details",
                        user_id=user_id))
                edit = {
                    "f_name": request.form.get("f_name").capitalize(),
                    "l_name": request.form.get("l_name").capitalize(),
                    "email": request.form.get("email"),
                    "username": request.form.get("username").lower(),
                    "photo_url": request.form.get("photo_url"),
                }
                """
                Adds password to the edit user object if new password
                is entered in the edit details form
                """
                if request.form.get("password"):
                    edit["password"] = generate_password_hash(
                        request.form.get("password"))
                mongo.db.users.update_one({"_id": ObjectId(user_id)}, {
                    "$set": edit})
                """
                Changes the username on recipes created by user to the
                new updated username, returns to previously stored url in
                session with flashed message
                """
                query = {"created_by.user_id": editing["user_id"]}
                update = {"$set": {
                    "created_by.username": request.form.get(
                        "username").lower()}}
                mongo.db.recipes.update_many(query, update)
                flash("User details updated successfuly")
                return redirect(session["url"])

            return render_template(
                "edit_details.html",
                editing=editing,
                user=user)

        return redirect(url_for("home"))

    flash("You are not signed in")
    return redirect(url_for("home"))


@app.route("/delete_user/<user_id>", methods=["GET", "POST"])
def delete_user(user_id):
    """
    Checks user is in session, checks their confirmation password
    against their user object, deletes the user account if the
    current user is the same or admin and their confirmation password
    is entered correctly. Removes user from session if they delete themself
    """
    if "user" in session:
        user = get_user(session["user"])
        if request.method == "POST":
            if check_password_hash(
                    user["password"],
                    request.form.get("password_confirm{0}".format(user_id))):
                deleted = mongo.db.users.find_one({"_id": ObjectId(user_id)})
                if deleted["user_id"] == user["user_id"]:
                    session.pop("user")
                    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
                    flash("Account successfully removed")
                    return redirect(url_for("home"))
                elif user["is_admin"]:

                    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
                    flash("Account successfully removed")
                    return redirect(session["url"])
                return redirect(url_for("home"))

            flash("Incorrect Password")
            return redirect(session["url"])

    return redirect(url_for("home"))


@app.route("/recipe_details/<recipe_id>")
def recipe_details(recipe_id):
    """
    Puts page url into session cookie, gets the recipe the user clicked
    to see more details on, gets the user from users db if signed in
    """
    session["url"] = request.url
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    if "user" in session:
        user = get_user(session["user"])
        return render_template(
            "recipe_details.html",
            recipe=recipe,
            user=user)

    return render_template("recipe_details.html", recipe=recipe)


@app.route("/recipes")
def recipes():
    """
    Puts page url into session cookie, gets all recipes
    and sorts alphabetically, gets user if signed in
    """
    session["url"] = request.url
    recipes = mongo.db.recipes.find().sort("recipe_name", 1)
    if "user" in session:
        user = get_user(session["user"])
        return render_template("recipes.html", recipes=recipes, user=user)

    return render_template("recipes.html", recipes=recipes)


@app.route("/filter_recipes/<category_name>")
def filter_recipes(category_name):
    """
    Puts page url into session cookie, gets the category the user
    clicked on, gets all recipes tagged with that cateogry, gets user
    if signed in
    """
    session["url"] = request.url
    category = mongo.db.categories.find_one({
        "category_name": category_name})
    recipes = mongo.db.recipes.find({
        "categories.category_name": category_name})
    if "user" in session:
        user = get_user(session["user"])
        return render_template(
            "filter_recipes.html",
            recipes=recipes,
            category=category,
            user=user)

    return render_template(
        "filter_recipes.html",
        recipes=recipes,
        category=category)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    """
    Gets user if signed in, redirects to home with flashed message if not,
    gets all categories to display within add recipe form.
    builds array of selected category objects from request form by pulling
    the relevent catgeories from the categories DB, builds recipe object
    using all details on add recipe form, inserts into recipes DB, gets new
    recipe ObjectId to pass to redirect.
    """
    if "user" in session:
        user = get_user(session["user"])

        if request.method == "POST":
            selected_categories = request.form.getlist("category_name")
            recipe_categories = []
            for category in selected_categories:
                category_object = mongo.db.categories.find_one(
                    {"category_name": category})
                recipe_categories.append(category_object)

            recipe = {
                "categories": recipe_categories,
                "recipe_name": request.form.get("recipe_name"),
                "ingredients": request.form.getlist("ingredient"),
                "instructions": request.form.getlist("instruction"),
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
            """
            returns the _id of the newly created recipe to use in the redirect
            """
            new_recipe_id = mongo.db.recipes.find_one(recipe)["_id"]
            flash("Recipe successfully added")
            return redirect(url_for("recipe_details", recipe_id=new_recipe_id))

        categories = mongo.db.categories.find().sort("category_name", 1)
        return render_template(
            "add_recipe.html",
            categories=categories,
            user=user)

    flash("You are not signed in")
    return redirect(url_for("home"))


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    """
    Gets user if signed in, redirects to home if not. Gets all categories,
    sorted alphabetically and recipe the user wants to edit.
    checks if user attempting to edit is either the owner of the recipe
    or an admin user, recirects home if not. Builds object in the same way
    as the add_recipe function and updates the recipe in the recipes DB that
    matches the ObjectID of the selected recipe. Redirects with flashed message
    to the last URL in session cookie.
    """
    if "user" in session:
        user = get_user(session["user"])
        recipe_user = mongo.db.recipes.find_one(
            {"_id": ObjectId(recipe_id)})["created_by"]
        if user["user_id"] == recipe_user["user_id"] or user["is_admin"]:
            if request.method == "POST":
                selected_categories = request.form.getlist("category_name")
                recipe_categories = []
                for category in selected_categories:
                    category_object = mongo.db.categories.find_one(
                        {"category_name": category})
                    recipe_categories.append(category_object)

                edit = {
                    "categories": recipe_categories,
                    "recipe_name": request.form.get("recipe_name"),
                    "ingredients": request.form.getlist("ingredient"),
                    "instructions": request.form.getlist("instruction"),
                    "recipe_description": request.form.get(
                        "recipe_description"),
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

    return redirect(url_for("home"))


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    """
    Gets user if signed in, checks user is either owner of the selected recipe
    or admin. Deletes the recipe that has been selected if the user has the
    right permission. Checks if the URL in session if for the recipe that is
    being deleted and if so, redirects to all recipes, otherwise redirects the
    user to the last URL in session.
    """
    if "user" in session:
        user = get_user(session["user"])
        recipe_user = mongo.db.recipes.find_one(
            {"_id": ObjectId(recipe_id)})["created_by"]
        if user["user_id"] == recipe_user["user_id"] or user["is_admin"]:
            mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
            flash("Recipe successfully deleted")
            if session["url"].split("/")[-1] == request.url.split("/")[-1]:
                return redirect(url_for("recipes"))

    return redirect(session["url"])


@app.route("/recipe_like/<recipe_id>")
def recipe_like(recipe_id):
    """
    Checks if user is in session, otherwise recirects to URL in session cookie
    with flashed message. Gets 'Likes' array from selected recipe, checks if
    User ID from session is in the array ids, if so, removes them and
    decrements likes count by one, if not, adds them and increments
    likes count by one. Redirects to URL in session cookie.
    """
    if "user" in session:
        likes = mongo.db.recipes.find_one({
            "_id": ObjectId(recipe_id)})["likes"]
        if session["user"] in likes["id"]:
            new_count = likes["count"]-1
            mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {
                "$pull": {"likes.id": session["user"]},
                "$set": {"likes.count": new_count}})
        else:
            new_count = likes["count"]+1
            mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {
                "$push": {"likes.id": session["user"]},
                "$set": {"likes.count": new_count}})
        return redirect(session["url"])
    flash("You are not signed in")
    return redirect(session["url"])


@app.route("/categories")
def categories():
    """
    Gets all categories, sorted alphabetically. Checks if user is signed in,
    adds them to the front end if so, renders categories template
    """
    categories = mongo.db.categories.find().sort("category_name", 1)
    if "user" in session:
        user = get_user(session["user"])
        return render_template(
            "categories.html",
            categories=categories,
            user=user)

    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    """
    gets user if signed in, checks if user is super user or admin,
    redirects home if not.
    Builds category object from request form and inserts into
    categories DB
    """
    if "user" in session:
        user = get_user(session["user"])
        if user["is_super"] or user["is_admin"]:
            if request.method == "POST":
                category = {
                    "category_name": request.form.get("category_name"),
                    "category_description": request.form.get(
                        "category_description"),
                    "category_color": request.form.get("category_color")}
                mongo.db.categories.insert_one(category)

                flash("New category added!")
                return redirect(url_for("categories"))

            return render_template("add_category.html", user=user)

    return redirect(url_for("home"))


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    """
    Gets user if signed in, Checks if user is super user or admin,
    redirects home if neither.
    Builds category object in the same way as add_category function and
    updates the entry in DB using the ObjectID.
    """
    if "user" in session:
        user = get_user(session["user"])
        if user["is_super"] or user["is_admin"]:
            if request.method == "POST":
                edit = {
                    "category_name": request.form.get("category_name"),
                    "category_description": request.form.get(
                        "category_description"),
                    "category_color": request.form.get("category_color")}
                mongo.db.categories.update_one({
                    "_id": ObjectId(category_id)}, {"$set": edit})
                """
                Updates the instance of this category on all recipes
                that have it tagged.
                """
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

            category = mongo.db.categories.find_one({
                "_id": ObjectId(category_id)})
            return render_template(
                "edit_category.html",
                category=category,
                user=user)

    return redirect(url_for("home"))


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    """
    gets user is signed in, checks if user is super or admin,
    redirects to home if not.
    Deletes category from any applicable recipes before removing it
    from the categories DB.
    """
    if "user" in session:
        user = get_user(session["user"])
        if user["is_super"] or user["is_admin"]:
            mongo.db.recipes.update_many(
                {"categories._id": ObjectId(category_id)},
                {"$pull": {"categories": {"_id": ObjectId(category_id)}}})
            mongo.db.categories.delete_one({"_id": ObjectId(category_id)})

            flash("Category successfully deleted")
            return redirect(url_for("categories"))

    return redirect(url_for("home"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Builds message from all info within the contact form, inserts
    the message into the messages DB. redirects back home with flash
    message. Gets user if signed in to padd to the ront end for use
    on forms.
    """
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
    """
    Puts URL into session, gets user if signed in, checks that user is admin,
    directs non admin home. Gets all users from users DB
    """
    session["url"] = request.url
    if "user" in session:
        user = get_user(session["user"])
        if user["is_admin"]:
            users = mongo.db.users.find().sort("username", 1)
            return render_template("users.html", users=users, user=user)
    return redirect(url_for("home"))


@app.route("/messages")
def messages():
    """
    gets user if signed in, checks if they are admin, recirects gome if not.
    gets all messages from messages DB.
    """
    if "user" in session:
        user = get_user(session["user"])
        if user["is_admin"]:
            messages = mongo.db.messages.find().sort("date", -1)
            return render_template(
                "messages.html",
                messages=messages,
                user=user)
    return redirect(url_for("home"))


@app.route("/delete_message/<message_id>")
def delete_message(message_id):
    """
    gets user if signed in, checks if admin, redirects home if not.
    Removes the selected message from the messages DB and redirects
    back to messages.
    """
    if "user" in session:
        user = get_user(session["user"])
        if user["is_admin"]:
            mongo.db.messages.delete_one({"_id": ObjectId(message_id)})
            flash("Message successfully deleted")
            return redirect(url_for("messages"))
    # Redirects non-admin users back home
    return redirect(url_for("home"))


@app.route("/super_user/<user_id>")
def super_user(user_id):
    """
    gets user if signed in, checks if admin.
    checks if selected user is super, removes the super user
    status if so, adds super user status if not.
    redirects to URL in session.
    """
    if "user" in session:
        admin = get_user(session["user"])
        if admin["is_admin"]:
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
    """
    gets user if signed in, checks if admin.
    checks if selected user is admin, removes the admin
    status if so, adds admin status if not.
    redirects to URL in session.
    """
    if "user" in session:
        admin = get_user(session["user"])
        if admin["is_admin"]:
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
    """
    gets user if signed in, pops them out of session cookie,
    recirects home with successful flash. Redirects non
    signed in users back home with different flashed message.
    """
    if "user" in session:
        # remove user_id from session cookie
        flash("You have been signed out")
        session.pop("user")
        return redirect(url_for("home"))

    flash("You are not signed in")
    return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
