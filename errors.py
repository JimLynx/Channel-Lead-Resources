from app import app
from flask import render_template


# -------- ERROR HANDLING PAGES -------- #

# 404 page not found error
@app.errorhandler(404)
def not_found_error(error):
    '''
    Handle 404 error and render 404 error page.
    '''
    return render_template('errors/404.html', error=error), 404


# 500 internal server error
@app.errorhandler(500)
def internal_error(error):
    '''
    Handle 500 error and render 500 error page.
    '''
    return render_template('errors/500.html', error=error), 500
