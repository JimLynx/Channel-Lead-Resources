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


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/ms1')
def ms1():
    resources = list(mongo.db.cl_resources.find())
    return render_template('ms1.html', resources=resources)


@app.route('/ms2')
def ms2():
    resources = list(mongo.db.cl_resources.find())
    return render_template('ms2.html', resources=resources)


@app.route('/ms3')
def ms3():
    resources = list(mongo.db.cl_resources.find())
    return render_template('ms3.html', resources=resources)


@app.route('/ms4')
def ms4():
    resources = list(mongo.db.cl_resources.find())
    return render_template('ms4.html', resources=resources)


@app.route('/version_control')
def version_control():
    resources = list(mongo.db.cl_resources.find())
    return render_template('version-control.html', resources=resources)


@app.route('/general')
def general():
    resources = list(mongo.db.cl_resources.find({'category_name': request.form.get('topic')}))
    return render_template('general.html', resources=resources)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_types = list(mongo.db.users.find())
    if request.method == 'POST':
        username = mongo.db.users.find_one({'user_type': request.form.get('username')})
        if check_password_hash(username['password'], request.form.get('password')):
            session['user'] = request.form.get('username')
            if request.form.get('username') == 'superuser':
                return redirect(url_for('superuser', user=session['user']))
            return redirect(url_for('add_resource'))
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
    return redirect(url_for('home'))


@app.route('/add_resource', methods=['GET', 'POST'])
def add_resource():
    if session['user'] == 'lead' or session['user'] == 'superuser' or session['user'] == 'assessor':
        if request.method == 'POST':
            upload = {
                "category_name": request.form.get("category_name"),
                "title": request.form.get("title"),
                "description": request.form.get("description"),
                "url": request.form.get("url"),
                "created_by": request.form.get("created_by"),
                "date": request.form.get("date")
            }
            mongo.db.ci_resources.insert_one(upload)
            return redirect(url_for(''))


    categories = mongo.db.categories.find().sort('category_name', 1)
    return render_template('add_resource.html', categories=categories)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
