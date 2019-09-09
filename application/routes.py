"""Routes for core Flask app."""
from flask import Blueprint, render_template

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@main_bp.route('/')
def home():
    """Landing page."""
    return render_template('index.html',
                           title='Data Breach Project',
                           template='home-template')
