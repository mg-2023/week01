from flask import Blueprint, render_template, session

mypage_bp = Blueprint("mypage", __name__)

@mypage_bp.route("/")
def mypage():
    user = session['user_id']
    return render_template('mypage/index.html', user=user)

