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

# Render Home page


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


# Render Resources page.
@app.route('/resources')
def resources():
    # If there is any logged in user
    if session['user']:
        # Find all key and values in the  cl_resources
        # collection on MongoDB
        resources = list(mongo.db.cl_resources.find())
    return render_template('resources.html', resources=resources)


# Search function
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query')
    # search through all on db
    resources = list(mongo.db.cl_resources.find({'$text': {'$search': query}}))
    return render_template('resources.html', resources=resources)


# Contact page
@app.route('/contact')
def contact():
    if session['user']:
        resources = list(mongo.db.cl_resources.find())
    categories = mongo.db.categories.find().sort('category_name', 1)
    return render_template('contact.html', resources=resources, categories=categories)


# -------- USERS -------- #


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    user_types = list(mongo.db.users.find())
    if request.method == 'POST':
        username = mongo.db.users.find_one(
            {'user_type': request.form.get('username')})
        if check_password_hash(username['password'], request.form.get('password')):
            session['user'] = request.form.get('username')
            if request.form.get('username') == 'superuser':
                flash(
                    "You have successfully logged in", "success")
                # change redirect when manage dashboard is ready
                return redirect(url_for('manage_users', user=session['user']))
            flash(
                "You have successfully logged in", "success")
            return redirect(url_for('resources'))
        else:
            flash("Incorrect password please try again", "danger")
    return render_template('login.html', users=user_types)


# Manage Users page
@app.route('/manage_users')
def manage_users():
    if session['user'] == 'superuser' or session['user'] == 'assessor':

        users = list(mongo.db.users.find().sort('user_type', 1))
        return render_template('manage_users.html', users=users)
    return redirect(url_for('resources'))


# Add User
@app.route('/add_users', methods=['GET', 'POST'])
def add_users():
    if session['user'] == 'superuser' or session['user'] == 'assessor':
        if request.method == 'POST':
            mongo.db.users.insert_one(
                {'user_type': request.form.get('username'), 'password': generate_password_hash(
                    request.form.get('password'))}
            )
            flash("New User Added!", "success")
            return redirect(url_for('manage_users'))
        return render_template('add_users.html')
    return redirect(url_for('resources'))


# Delete User
@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    if session['user'] == 'superuser' or session['user'] == 'assessor':

        mongo.db.users.remove({'_id': ObjectId(user_id)})
        flash("Selected User Successfully Deleted.", "info")
        return redirect(url_for('manage_users'))
    return redirect(url_for('resources'))


# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Successfully LOGGED OUT - Please visit again soon!", "success")
    return redirect(url_for('login'))


# -------- RESOURCES -------- #


# Add resource
@app.route('/add_resource', methods=['GET', 'POST'])
def add_resource():
    if session['user'] == 'superuser' or session['user'] == 'assessor' or session['user'] == 'lead':
        if request.method == 'POST':
            upload = {
                "category_name": request.form.get("category_name"),
                "title": request.form.get("title"),
                "description": request.form.get("description"),
                "video_url": request.form.get("video_url"),
                "document_url": request.form.get("document_url"),
                "created_by": request.form.get("created_by"),
                "date": request.form.get("date")
            }
            mongo.db.cl_resources.insert_one(upload)
            flash(
                "Thanks! - Your Awesome New Resource Was Successfully Added.", "success")
            return redirect(url_for('resources'))

        categories = mongo.db.categories.find().sort('category_name', 1)
        return render_template('add_resource.html', categories=categories)
    return redirect(url_for('resources'))


# Edit resources
@app.route('/edit_resource/<resource_id>', methods=['GET', 'POST'])
def edit_resource(resource_id):
    if session['user'] == 'superuser' or session['user'] == 'assessor' or session['user'] == 'lead':
        if request.method == 'POST':
            upload = {
                "category_name": request.form.get("category_name"),
                "title": request.form.get("title"),
                "description": request.form.get("description"),
                "video_url": request.form.get("video_url"),
                "document_url": request.form.get("document_url"),
                "created_by": request.form.get("created_by"),
                "date": request.form.get("date")
            }
            mongo.db.cl_resources.update(
                {'_id': ObjectId(resource_id)}, upload)
            flash("Selected Resource Successfully Updated.", "success")
            return redirect(url_for('resources'))

        resource = mongo.db.cl_resources.find_one(
            {'_id': ObjectId(resource_id)})
        categories = mongo.db.categories.find().sort('category_name', 1)
        return render_template('edit_resource.html', resource=resource, categories=categories)
    return redirect(url_for('resources'))


# Delete resources
@app.route('/delete_resource/<resource_id>')
def delete_resource(resource_id):
    if session['user'] == 'superuser' or session['user'] == 'assessor':
        mongo.db.cl_resources.remove({'_id': ObjectId(resource_id)})
        flash("Selected Resource Successfuly Deleted.", "info")
        return redirect(url_for('resources'))
    return redirect(url_for('resources'))


# -------- CATEGORIES -------- #


# Manage Categories page
@app.route('/manage_categories')
def manage_categories():
    if session['user'] == 'lead' or session['user'] == 'superuser' or session['user'] == 'assessor':

        categories = list(mongo.db.categories.find().sort('category_name', 1))
        return render_template('manage_categories.html', categories=categories)
    return redirect(url_for('resources'))


# Add new category
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if session['user'] == 'lead' or session['user'] == 'superuser' or session['user'] == 'assessor':
        if request.method == "POST":
            category = {
                "category_name": request.form.get('category_name')
            }
            mongo.db.categories.insert_one(category)
            flash("New Category Added!", "success")
            return redirect(url_for('manage_categories'))
        return render_template('add_category.html')
    return redirect(url_for('resources'))


# Edit category
@app.route('/edit_category/<category_id>', methods=['GET', 'POST'])
def edit_category(category_id):

    if session['user'] == 'lead' or session['user'] == 'superuser' or session['user'] == 'assessor':
        if request.method == "POST":
            submit = {
                "category_name": request.form.get('category_name')
            }
            mongo.db.categories.update({'_id': ObjectId(category_id)}, submit)
            flash("Selected Category Successfully Updated.", "success")
            return redirect(url_for('manage_categories'))

    category = mongo.db.categories.find_one({'_id': ObjectId(category_id)})
    return render_template('edit_category.html', category=category)


# Delete Category


@app.route('/delete_category/<category_id>')
def delete_category(category_id):

    if session['user'] == 'superuser' or session['user'] == 'assessor':
        mongo.db.categories.remove({'_id': ObjectId(category_id)})
        flash("Selected Category Successfully Deleted.", "info")
        return redirect(url_for('manage_categories'))
    return redirect(url_for('resources'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
