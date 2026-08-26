from flask import Blueprint, render_template

mypage_bp = Blueprint("mypage", __name__)

@mypage_bp.route("/")
def mypage():
    return render_template('mypage/index.html')
