import mail_settings
import math
import re
from datetime import datetime
from app import app, mongo
from flask import flash, render_template, redirect, request, session, url_for
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

currentDate = datetime.today().strftime('%d-%m-%Y')

# Variables for MongoDB collections
cl = mongo.db.cl_resources
cat = mongo.db.categories
cl.users = mongo.db.users


# Functions for user access groups
def admin_1():
    return session['user'] == 'superuser' or session['user'] == 'assessor'


def admin_2():
    return session['user'] == 'superuser' or session['user'] == 'assessor' or session['user'] == 'lead'


# Render Home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    user_types = list(cl.users.find())
    if request.method == 'POST':
        username = cl.users.find_one(
            {'user_type': request.form.get('username')})
        if check_password_hash(username['password'], request.form.get('password')):
            session['user'] = request.form.get('username')
            flash(
                "Welcome, you've successfully logged in to Channel Lead Resources!", "success")
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
    '''

    '''
    # If there are logged in users
    if session['user']:
        # Pagination
        # get the page number from request or set the page 1 if first page
        page = int(request.args.get('page') or 1)
        # results limit to find
        num = 5
        # count documents to calculate number of pagination options
        count = int(math.ceil(cl.count_documents({}) / num))
        if page > count or page < 1:
            return render_template('errors/404.html'), 404
        # page - 1 ensures that the first items can be found
        # multiply the page number  by the item limit for current page results
        resources = list(cl.find(
            {}).skip((page - 1)*num).limit(num))
        categories = cat.find().sort('category_name', 1)
        return render_template('resources.html', resources=resources, categories=categories, page=page, count=count, search=False)
    return redirect(url_for('login'))


# Search function for Resources page
@app.route('/search', methods=['GET', 'POST'])
def search():
    resources = []
    if request.method == 'POST':
        # parse values from form
        search = request.form.get('search', '')
        select = request.form.get('category_name', '')
        # perform mongo with search only
        if search and not select:
            resources = cl.find({'$text': {'$search': search}})
        # perform mongo with select only
        elif select and not search:
            resources = cl.find({'category_name': select})
        elif search and select:
            resources = cl.find(
                {'$and': [{'category_name':  select}, {'$text': {'$search': search}}]})
        # if no search and no filter
        else:
            resources = cl.find({})
        resources = [item for item in resources]

    categories = cat.find().sort('category_name', 1)
    print(resources)
    return render_template('resources.html', resources=resources, categories=categories)


# -------- MANAGE USERS PAGE -------- #

# Render Manage Users page
@app.route('/manage_users')
def manage_users():
    if admin_1():
        users = list(cl.users.find().sort('user_type', 1))
        return render_template('manage_users.html', users=users)
    return redirect(url_for('resources'))


# Add User
@app.route('/add_users', methods=['GET', 'POST'])
def add_users():
    if admin_1():
        if request.method == 'POST':
            cl.users.insert_one(
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
    if admin_1():

        cl.users.remove({'_id': ObjectId(user_id)})
        flash("Selected User Successfully Deleted.", "info")
        return redirect(url_for('manage_users'))
    return redirect(url_for('resources'))


# -------- MANAGE RESOURCES PAGE -------- #

# Render Manage Resources page
@app.route('/manage_resources')
def manage_resources():
    if admin_2():
        page = int(request.args.get('page') or 1)
        num = 4
        count = int(math.ceil(cl.count_documents({}) / num))
        if page > count or page < 1:
            return render_template('errors/404.html'), 404
        resources = list(cl.find(
            {}).skip((page - 1) * num).limit(num))
        return render_template('manage_resources.html', resources=resources, page=page, count=count, search=False)
    return redirect(url_for('resources'))


# Search function for Manage Resources page
@app.route('/search_manage_resources', methods=['GET', 'POST'])
def search_manage_resources():
    query = request.form.get('query')
    resources = list(cl.find({'$text': {'$search': query}}))
    return render_template('manage_resources.html', resources=resources)


# Add resource
@app.route('/add_resource', methods=['GET', 'POST'])
def add_resource():
    if admin_2():
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

            # replace end of returned url string from user link to 'preview' for embedded PDF
            if upload["document_url"] != None:
                upload["document_url"] = upload["document_url"].replace(
                    "/view?usp=sharing", "/preview")

            # use regular expression to post only id of video to video_url
            # Credit:Sean Murphy : regex code
            if upload["video_url"] != None:
                upload["video_url"] = ''.join(re.findall(
                    '(?<=v=)(.{11})', upload["video_url"]))

            cl.insert_one(upload)
            flash(
                "Thanks, Your Awesome Resource Was Successfully Added!", "success")
            return redirect(url_for('manage_resources'))

        categories = cat.find().sort('category_name', 1)
        return render_template('add_resource.html', categories=categories)
    return redirect(url_for('resources'))


# Edit resources
@app.route('/edit_resource/<resource_id>', methods=['GET', 'POST'])
def edit_resource(resource_id):
    if admin_2():
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

            # replace end of returned url string from user link to 'preview' for embedded PDF
            if upload["document_url"] != None:
                upload["document_url"] = upload["document_url"].replace(
                    "/view?usp=sharing", "/preview")

            if upload["video_url"] != None:
                upload["video_url"] = ''.join(re.findall(
                    '(?<=v=)(.{11})', upload["video_url"]))

            cl.update(
                {'_id': ObjectId(resource_id)}, upload)
            flash("Selected Resource Successfully Updated.", "success")
            return redirect(url_for('manage_resources'))
        resource = cl.find_one(
            {'_id': ObjectId(resource_id)})
        categories = cat.find().sort('category_name', 1)
        return render_template('edit_resource.html', resource=resource, categories=categories)
    return redirect(url_for('resources'))


# Delete resources
@app.route('/delete_resource/<resource_id>')
def delete_resource(resource_id):
    if admin_2():
        cl.remove({'_id': ObjectId(resource_id)})
        flash("Selected Resource Successfuly Deleted.", "info")
        return redirect(url_for('manage_resources'))
    return redirect(url_for('resources'))


# -------- MANAGE CATEGORIES PAGE -------- #

# Render Manage Categories page
@app.route('/manage_categories')
def manage_categories():
    if admin_2():
        page = int(request.args.get('page') or 1)
        num = 4
        count = int(math.ceil(cl.count_documents({}) / num))
        if page > count or page < 1:
            return render_template('errors/404.html'), 404
        categories = list(cat.find(
            {}).skip((page - 1) * num).limit(num))
        return render_template('manage_categories.html', categories=categories, page=page, count=count, search=False)
    return redirect(url_for('resources'))


# Search function for Manage Categories page
@app.route('/search_manage_categories', methods=['GET', 'POST'])
def search_manage_categories():
    query = request.form.get('query')
    resources = list(cl.find({'$text': {'$search': query}}))
    return render_template('manage_categories.html', resources=resources)


# Add new category
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if admin_2():
        if request.method == "POST":
            category = {
                "category_name": request.form.get('category_name')
            }
            cat.insert_one(category)
            flash("New Category Added!", "success")
            return redirect(url_for('manage_categories'))
        return render_template('manage_categories.html')
    return redirect(url_for('resources'))


# Edit category
@app.route('/edit_category/<category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    if admin_2():
        if request.method == "POST":
            submit = {
                "category_name": request.form.get('category_name')
            }
            cat.update({'_id': ObjectId(category_id)}, submit)
            flash("Selected Category Successfully Updated.", "success")
            return redirect(url_for('manage_categories'))

        category = cat.find_one({'_id': ObjectId(category_id)})
        return render_template('edit_category.html', category=category)
    return redirect(url_for('resources'))


# Delete Category
@app.route('/delete_category/<category_id>')
def delete_category(category_id):

    if session['user'] == 'superuser' or session['user'] == 'assessor':
        cat.remove({'_id': ObjectId(category_id)})
        flash("Selected Category Successfully Deleted.", "info")
        return redirect(url_for('manage_categories'))
    return redirect(url_for('resources'))


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
            mail_settings.sendEmail(result)
            flash("Thanks, your feedback has been sent!", "success")
            return redirect(url_for('contact'))

        resources = list(cl.find())
        categories = cat.find().sort('category_name', 1)
        return render_template('contact.html', resources=resources, categories=categories)
    return redirect(url_for('login'))
