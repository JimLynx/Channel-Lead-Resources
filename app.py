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
@app.route('/resources')
def resources():
    resources = list(mongo.db.cl_resources.find())
    return render_template('resources.html', resources=resources)


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_types = list(mongo.db.users.find())
    if request.method == 'POST':
        username = mongo.db.users.find_one({'user_type': request.form.get('username')})
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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
