from flask import Blueprint, render_template, request, jsonify, session
from services.closet_service import create_closet_item

closet_bp = Blueprint("closet", __name__)


@closet_bp.route('/')
def index():
    return render_template('closet/index.html')


# 등록 화면
@closet_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

# 등록 API
@closet_bp.route("/register", methods=["POST"])
def register_item():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"message": "로그인 하세요."}), 401

    if "file" not in request.files or request.files["file"].filename == "":
        return jsonify({"message": "이미지 파일이 필요합니다."}), 400

    try:
        file = request.files["file"]
        item_id = create_closet_item(user_id, request.form, file)
        return jsonify({"message": "성공적으로 등록되었습니다.", "item_id": item_id}), 201
    except Exception as e:
        return jsonify({"message": f"등록 실패: {str(e)}"}), 500
