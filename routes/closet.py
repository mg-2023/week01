from flask import Blueprint, render_template

closet_bp = Blueprint('closet', __name__)

@closet_bp.route('/')
def index():
    return render_template('closet/index.html')