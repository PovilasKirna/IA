from flask import Blueprint, render_template, redirect, url_for
from werkzeug.exceptions import HTTPException
from flask_login import current_user

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', user=current_user), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', user=current_user), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', user=current_user), 500

@errors.app_errorhandler(HTTPException)
def handle_exception(error):
    return render_template('errors/500.html', user=current_user), 500