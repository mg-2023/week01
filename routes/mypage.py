from flask import Blueprint

mypage_bp = Blueprint("mypage", __name__)

@mypage_bp.route("/mypage")
def mypage():
    return "마이페이지"