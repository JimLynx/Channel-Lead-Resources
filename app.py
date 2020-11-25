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

'''
Renders Home page
'''


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


'''
Renders Resources page. 
Finds all key and values 
in the  cl_resources 
collection on MongoDB
'''


@app.route('/resources')
def resources():
    resources = list(mongo.db.cl_resources.find())
    return render_template('resources.html', resources=resources)


@app.route('/contact')
def contact():
    resources = list(mongo.db.cl_resources.find())
    categories = mongo.db.categories.find().sort('category_name', 1)
    return render_template('contact.html', resources=resources, categories=categories)


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_types = list(mongo.db.users.find())
    if request.method == 'POST':
        username = mongo.db.users.find_one(
            {'user_type': request.form.get('username')})
        if check_password_hash(username['password'], request.form.get('password')):
            session['user'] = request.form.get('username')
            if request.form.get('username') == 'superuser':
                return redirect(url_for('superuser', user=session['user']))
            return redirect(url_for('resources'))
    return render_template('login.html', users=user_types)


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('login'))


@app.route('/<user>', methods=['GET', 'POST'])
def superuser(user):
    if session['user'] == 'superuser' or session['user'] == 'assessor':
        if request.method == 'POST':
            mongo.db.users.insert_one(
                {'user_type': request.form.get('username'),
                 'password': generate_password_hash(request.form.get('password'))}
            )
        return render_template('superuser.html', user=session['user'])
    return redirect(url_for('resources'))


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
            flash("Thanks, your resource has been added!")
            return redirect(url_for('resources'))

    categories = mongo.db.categories.find().sort('category_name', 1)
    return render_template('add_resource.html', categories=categories)


'''
Editing tasks
'''


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
            flash("Thanks, your resource has been updated!")

    resource = mongo.db.cl_resources.find_one({'_id': ObjectId(resource_id)})
    categories = mongo.db.categories.find().sort('category_name', 1)
    return render_template('edit_resource.html', resource=resource, categories=categories)


'''
Delete resources
'''


@app.route('/delete_resource/<resource_id>')
def delete_resource(resource_id):
    mongo.db.cl_resources.remove({'_id': ObjectId(resource_id)})
    flash("Your resource has been Deleted. Please add new material soon!")
    return redirect(url_for('resources'))


'''
Manage Categories
'''


@app.route('/resource_categories')
def resource_categories():
    if session['user'] == 'superuser' or session['user'] == 'assessor':

        categories = list(mongo.db.categories.find().sort('category_name', 1))
        return render_template('resource_categories.html', categories=categories)
    return redirect(url_for('resources'))



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
