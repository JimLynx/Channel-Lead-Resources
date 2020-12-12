import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from datetime import datetime
import math
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# email server
email_settings = {
    # "TESTNG": True,
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465,
    "MAIL_USE_SSL": True,
    "MAIL_ASCII_ATTACHMENTS": True,
    "MAIL_USERNAME": os.environ.get('MAIL_USERNAME'),
    "MAIL_PASSWORD": os.environ.get('MAIL_PASSWORD'),
    "MAIL_DEFAULT_SENDER": os.environ.get('MAIL_DEFAULT_SENDER'),
    "ADMIN_EMAIL": os.environ.get('ADMIN_EMAIL')
}

app.config.update(email_settings)

print(email_settings)
mail = Mail(app)

currentDate = datetime.today().strftime('%d-%m-%Y')


def sendEmail(result):
    msg = Message("Contact form submission from Channel Lead Resources",
                  recipients=[email_settings["ADMIN_EMAIL"]]
                  )

    msg.body = """
    Hi there,

    A user has submiited the following feedback:

    Category Name:  {}
    Subject:    {}
    Feedback:   {}
    Suggestion: {}
    Name:   {}
    Slack:  {}
    Email:  {}

    Regards,
    The CI Channel Lead team

    """.format(result['category'],
               result['subject'],
               result['feedback'],
               result['feedback_url'],
               result['name'],
               result['slackName'],
               result['emailAddress']
               )

    mail.send(msg)


# -------- CONTACT PAGE-------- #

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if session['user']:
        if request.method == 'POST':
            result = {
                'category': request.form.get('category_name'),
                'subject': request.form.get('subject'),
                'feedback': request.form.get('feedback'),
                'feedback_url': request.form.get('feedback_url'),
                'name': request.form.get('yourName'),
                'slackName': request.form.get('slackName'),
                'emailAddress': request.form.get('emailAddress')
            }
            sendEmail(result)
            flash("Thanks, your feedback has been sent!", "success")
            return redirect(url_for('contact'))

        resources = list(mongo.db.cl_resources.find())
        categories = mongo.db.categories.find().sort('category_name', 1)
        return render_template('contact.html', resources=resources, categories=categories)
    return redirect(url_for('login'))
# create variables for user groups to shorten code - TBA

# admin_1 = mongo.db.users.find(session['user'] == 'superuser' or session['user'] == 'assessor')
# admin_2 = mongo.db.users.find(session['user'] == 'superuser' or session['user'] == 'assessor' or session['user'] == 'lead')
# admin_3 = mongo.db.users.find(session['user'] == 'superuser' or session['user'] == 'assessor' or session['user'] == 'lead' or session['user'] == 'student')


# Render Home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    user_types = list(mongo.db.users.find())
    if request.method == 'POST':
        username = mongo.db.users.find_one(
            {'user_type': request.form.get('username')})
        if check_password_hash(username['password'], request.form.get('password')):
            session['user'] = request.form.get('username')
            return redirect(url_for('resources'))
        else:
            flash("Incorrect password please try again", "danger")
    return render_template('login.html', users=user_types)


# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Successfully LOGGED OUT - Please visit again soon!", "success")
    return redirect(url_for('home'))


# -------- RESOURCES PAGE-------- #

# Render Resources page.
@app.route('/resources')
def resources():
    # If there are logged in users
    if session['user']:
        # Pagination
        # get the page number from request or set the page 1 if first page
        page = int(request.args.get('page') or 1)
        # results limit to find
        num = 5
        # count documents to calculate number of pagination options
        count = int(math.ceil(mongo.db.cl_resources.count_documents({}) / num))
        if page > count or page < 1:
            return render_template('errors/404.html'), 404
        # page - 1 ensures that the first items can be found
        # multiply the page number  by the item limit for current page results
        resources = list(mongo.db.cl_resources.find(
            {}).skip((page - 1) * num).limit(num))
        return render_template('resources.html', resources=resources, page=page, count=count, search=False)
    return redirect(url_for('login'))


# Search function for Resources page
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query')
    # search through all on db
    resources = list(mongo.db.cl_resources.find({'$text': {'$search': query}}))
    return render_template('resources.html', resources=resources)


# -------- MANAGE USERS PAGE -------- #

# Render Manage Users page
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


# -------- MANAGE RESOURCES PAGE -------- #

# Render Manage Resources page
@app.route('/manage_resources')
def manage_resources():
    if session['user'] == 'lead' or session['user'] == 'superuser' or session['user'] == 'assessor':
        page = int(request.args.get('page') or 1)
        num = 4
        count = int(math.ceil(mongo.db.cl_resources.count_documents({}) / num))
        if page > count or page < 1:
            return render_template('errors/404.html'), 404
        resources = list(mongo.db.cl_resources.find(
            {}).skip((page - 1) * num).limit(num))
        return render_template('manage_resources.html', resources=resources, page=page, count=count, search=False)
    return redirect(url_for('resources'))


# Search function for Manage Resources page
@app.route('/search_manage_resources', methods=['GET', 'POST'])
def search_manage_resources():
    query = request.form.get('query')
    resources = list(mongo.db.cl_resources.find({'$text': {'$search': query}}))
    return render_template('manage_resources.html', resources=resources)


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
                "date": currentDate
            }
            mongo.db.cl_resources.insert_one(upload)
            flash(
                "Thanks! - Your Awesome New Resource Was Successfully Added.", "success")
            return redirect(url_for('manage_resources'))

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
                "date": currentDate
            }
            mongo.db.cl_resources.update(
                {'_id': ObjectId(resource_id)}, upload)
            flash("Selected Resource Successfully Updated.", "success")
            return redirect(url_for('manage_resources'))
        resource = mongo.db.cl_resources.find_one(
            {'_id': ObjectId(resource_id)})
        categories = mongo.db.categories.find().sort('category_name', 1)
        return render_template('edit_resource.html', resource=resource, categories=categories)
    return redirect(url_for('resources'))


# Delete resources
@app.route('/delete_resource/<resource_id>')
def delete_resource(resource_id):
    if session['user'] == 'lead' or session['user'] == 'superuser' or session['user'] == 'assessor':
        mongo.db.cl_resources.remove({'_id': ObjectId(resource_id)})
        flash("Selected Resource Successfuly Deleted.", "info")
        return redirect(url_for('manage_resources'))
    return redirect(url_for('resources'))


# -------- MANAGE CATEGORIES PAGE -------- #

# Render Manage Categories page
@app.route('/manage_categories')
def manage_categories():
    if session['user'] == 'lead' or session['user'] == 'superuser' or session['user'] == 'assessor':
        page = int(request.args.get('page') or 1)
        num = 4
        count = int(math.ceil(mongo.db.cl_resources.count_documents({}) / num))
        if page > count or page < 1:
            return render_template('errors/404.html'), 404
        categories = list(mongo.db.categories.find(
            {}).skip((page - 1) * num).limit(num))
        return render_template('manage_categories.html', categories=categories, page=page, count=count, search=False)
    return redirect(url_for('resources'))


# Search function for Manage Categories page
@app.route('/search_manage_categories', methods=['GET', 'POST'])
def search_manage_categories():
    query = request.form.get('query')
    resources = list(mongo.db.cl_resources.find({'$text': {'$search': query}}))
    return render_template('manage_categories.html', resources=resources)


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
        return render_template('manage_categories.html')
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
    return redirect(url_for('resources'))


# Delete Category
@app.route('/delete_category/<category_id>')
def delete_category(category_id):

    if session['user'] == 'superuser' or session['user'] == 'assessor':
        mongo.db.categories.remove({'_id': ObjectId(category_id)})
        flash("Selected Category Successfully Deleted.", "info")
        return redirect(url_for('manage_categories'))
    return redirect(url_for('resources'))




# -------- ERROR HANDLING PAGES -------- #

# 404 page not found error
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html', error=error), 404


# 500 internal server error
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html', error=error), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
