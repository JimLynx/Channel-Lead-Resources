import mail_settings
import math
import re
from datetime import datetime
from app import app, mongo
from flask import flash, render_template, redirect, request, session, url_for
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# === Variable to store current date by dd/mm/yy
currentDate = datetime.today().strftime('%d-%m-%Y')

# === Variables for MongoDB collections

# Resources Collection
cl = mongo.db.cl_resources

# Categories Collection
cat = mongo.db.categories

# Users Collection
cl.users = mongo.db.users


# === Functions for user access groups
def admin_1():
    """
        Set Admin Level 1 to include
        Superuser and Assessor access only
    """

    return session['user'] == 'superuser' or session['user'] == 'assessor'


def admin_2():
    """
        Set Admin Level 2 to include
        Superuser, Assessor and Lead access
    """

    return session['user'] == 'superuser' or \
        session['user'] == 'assessor' or session['user'] == 'lead'


# === Render Landing page
@app.route('/')
@app.route('/home')
def home():
    """
        Renders default landing page
    """

    return render_template('home.html')


# === Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
        User log in.

        Pre-determined username is selected from
        the dropdown options.

        If user password is not correct
        flash error message to user.
    """

    user_types = list(cl.users.find())

    if request.method == 'POST':
        username = cl.users.find_one(
            {'user_type': request.form.get('username')})

        if check_password_hash(username['password'],
                               request.form.get('password')):
            session['user'] = request.form.get('username')
            flash(
                "Welcome, you've successfully logged in to \
                Channel Lead Resources!", "success")
            return redirect(url_for('resources'))
        else:
            flash("Incorrect password please try again", "danger")

    return render_template(
        'login.html',
        users=user_types
    )


# === Logout
@app.route('/logout')
def logout():
    """
        Remove user from session using
        pop() method.
    """

    session.pop('user', None)
    flash("Successfully LOGGED OUT - Please visit again soon!", "success")

    return redirect(url_for('home'))


# -------- MAIN SEARCH FUNCTION -------- #

def default_search(request):
    """
        Cycle through DB resource
        and categories collections and
        search by keyword or category or both
    """

    resources = []
    categories = cat.find().sort('category_name', 1)

    if request.method == 'POST':
        # parse values from search form input
        search = request.form.get('search', '')
        select = request.form.get('category_name', '')

        # perform DB search with keyword search only
        if search and not select:
            resources = cl.find({'$text': {'$search': search}})
        # perform DB search with select option only
        elif select and not search:
            resources = cl.find({'category_name': select})
        # perform DB search with keyword and select option
        elif search and select:
            resources = cl.find(
                {'$and': [{'category_name': select},
                          {'$text': {'$search': search}}]})
        # if no search and no filter
        else:
            resources = cl.find({})

        resources = [item for item in resources]

    return resources, categories


# -------- PAGINATION -------- #

def pagination(request, items_to_count, num_of_pages):
    """
    Pagination:
    get the page number from request or set the page 1 if first page
    limit results to find
    count documents to calculate number of pagination options
    """

    page = int(request.args.get('page') or 1)
    count = int(math.ceil(items_to_count.count_documents({}) / num_of_pages))

    if page > count or page < 1:
        return False

    resources = list(cl.find({}).skip((page - 1)*num_of_pages).limit(num_of_pages))
    categories = cat.find().sort('category_name', 1)

    return (resources, categories, page, count)


# -------- FORM DATA RETRIEVAL -------- #
def get_form_data(request):
    upload = {
        "category_name": request.form.get("category_name"),
        "title": request.form.get("title"),
        "description": request.form.get("description"),
        "video_url": request.form.get("video_url"),
        "document_url": request.form.get("document_url"),
        "created_by": request.form.get("created_by"),
        "date": currentDate
    }
    # replace end of returned url string from
    # user link to 'preview' for embedded PDF
    if upload["document_url"] is not None:
        upload["document_url"] = upload["document_url"].replace(
            "/view?usp=sharing", "/preview")
    # use regular expression to post only id of video to video_url
    if upload["video_url"] is not None:
        upload["video_url"] = ''.join(re.findall(
            '(?<=v=)(.{11})', upload["video_url"]))

    return upload


# -------- RESOURCES PAGE-------- #

# === Render Resources page.
@app.route('/resources')
def get_resources():
    """
        Set access for logged in session users.

        Call "pagination()" function.
    """

    if 'user' in session:
        pages = pagination(request, cl, 5)

        if not pages:
            return render_template('errors/404.html'), 404

        return render_template(
            'resources.html',
            resources=pages[0],
            categories=pages[1],
            page=pages[2],
            count=pages[3],
            search=False)

    flash("You need to Log in!", "danger")
    return redirect(url_for('home'))


# === Search function for Resources page
@app.route('/search', methods=['GET', 'POST'])
def search():
    """
        Call search function "default_search(request)"
        for new search on Resources page.
    """

    new_search = default_search(request)

    return render_template(
        'resources.html',
        resources=new_search[0],
        categories=new_search[1]
    )


# -------- MANAGE USERS PAGE -------- #

# === Render Manage Users page
@app.route('/manage_users')
def manage_users():
    """
        Set access for Admin level 1.

        Find all users in DB "users" collection.
    """

    if admin_1():
        users = list(cl.users.find().sort('user_type', 1))
        return render_template('manage_users.html', users=users)

    return redirect(url_for('resources'))


# === Add User
@app.route('/add_users', methods=['GET', 'POST'])
def add_users():
    """
        Set access for Admin level 1.

        Insert new username and password
        to DB "users" collection
    """

    if admin_1():
        if request.method == 'POST':
            cl.users.insert_one(
                {'user_type': request.form.get('username'),
                    'password': generate_password_hash(
                        request.form.get('password')
                )}
            )

            flash("New User Added!", "success")
            return redirect(url_for('manage_users'))

        return render_template('add_users.html')

    return redirect(url_for('resources'))


# === Delete User
@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    """
        Set access for Admin level 1.

        Use remove() method to delete
        selected user ID from DB
    """

    if admin_1():
        cl.users.remove({'_id': ObjectId(user_id)})
        flash("Selected User Successfully Deleted.", "info")

        return redirect(url_for('manage_users'))
    return redirect(url_for('resources'))


# -------- MANAGE RESOURCES PAGE -------- #

# === Render Manage Resources page
@app.route('/manage_resources')
def manage_resources():
    """
        Set access for Admin level 2.

        Call "pagination()" function.
    """

    if admin_2():
        pages = pagination(request, cl, 5)

        if not pages:
            return render_template('errors/404.html'), 404

        return render_template(
            'manage_resources.html',
            resources=pages[0],
            categories=pages[1],
            page=pages[2],
            count=pages[3],
            search=False)

    return redirect(url_for('resources'))


# === Search function for Manage Resources page
@app.route('/search_manage_resources', methods=['GET', 'POST'])
def search_manage_resources():
    """
    Call search function "default_search(request)"
    for new search on manage Resources page.
    """

    new_search = default_search(request)

    return render_template(
        'manage_resources.html',
        resources=new_search[0],
        categories=new_search[1]
    )


# === Add resource
@app.route('/add_resource', methods=['GET', 'POST'])
def add_resource():
    """
        Set access for Admin level 2.

        Get user input from form and create
        new resource entries in DB collection.
    """

    if admin_2():
        if request.method == 'POST':
            upload = get_form_data(request)

            cl.insert_one(upload)
            flash("Thanks, Your Awesome Resource Was Successfully Added!",
                  "success")
            return redirect(url_for('manage_resources'))

        resources = cl.find({})
        categories = cat.find({}).sort('category_name', 1)

        return render_template(
            'add_resource.html',
            resources=resources,
            categories=categories
        )

    return redirect(url_for('resources'))


# === Edit resources
@app.route('/edit_resource/<resource_id>', methods=['GET', 'POST'])
def edit_resource(resource_id):
    """
        Set access for Admin level 2.

        Get resources from DB and update.
    """

    if admin_2():
        if request.method == 'POST':
            upload = get_form_data(request)

            cl.update({'_id': ObjectId(resource_id)}, upload)

            flash("Selected Resource Successfully Updated.", "success")
            return redirect(url_for('manage_resources'))

        resource = cl.find_one({'_id': ObjectId(resource_id)})
        categories = cat.find().sort('category_name', 1)

        return render_template(
            'edit_resource.html',
            resource=resource,
            categories=categories
        )

    return redirect(url_for('resources'))


# === Delete resources
@app.route('/delete_resource/<resource_id>')
def delete_resource(resource_id):
    """
        Set access for Admin level 2.

        Use remove() method to delete
        selected resource ID from DB.
    """

    if admin_2():
        cl.remove({'_id': ObjectId(resource_id)})
        flash("Selected Resource Successfully Deleted.", "info")
        return redirect(url_for('manage_resources'))

    return redirect(url_for('resources'))


# -------- MANAGE CATEGORIES PAGE -------- #

# === Render Manage Categories page
@app.route('/manage_categories')
def manage_categories():
    """
        Set access for Admin level 2.

        Call "pagination()" function.
    """

    if admin_2():
        pages = pagination(request, cat, 5)

        if not pages:
            return render_template('errors/404.html'), 404

        return render_template(
            'manage_categories.html',
            categories=pages[0],
            page=page[1],
            count=page[2],
            search=False
        )

    return redirect(url_for('resources'))


# === Add new category
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    """
        Set access for Admin level 2.

        Get user input from form to  insert new
        category name into DB collection.
    """

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


# === Edit category
@app.route('/edit_category/<category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    """
        Set access for Admin level 2.

        Use update() method to update
        selected category
    """

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


# === Delete Category
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    """
        Set access for Admin level 1.

        Use remove() method to delete
        selected category ID from DB
    """

    if admin_1():
        cat.remove({'_id': ObjectId(category_id)})
        flash("Selected Category Successfully Deleted.", "info")
        return redirect(url_for('manage_categories'))

    return redirect(url_for('resources'))


# -------- CONTACT PAGE-------- #

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
        Set access to all session users.

        Fetch form user inputs and connect to Flask Mail
        to send email.
    """

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

        return render_template(
            'contact.html', resources=resources, categories=categories
        )

    return redirect(url_for('login'))
