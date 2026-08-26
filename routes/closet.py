from flask import Blueprint, render_template, request, jsonify, session
from services.closet_service import create_closet_item
from bson.objectid import ObjectId
from db import items

from db import *

closet_bp = Blueprint("closet", __name__)
cloth_type_id = {'상의': 1, '하의': 2, '외투': 3, '신발': 4, '악세서리': 5}

@closet_bp.route('/', methods=['GET'])
def index():
    button_ctrl = [False for _ in range(6)]
    cloth_type = request.args.get('type')
    user = session['user_id']
    if cloth_type:
        closet_items = items.find({'user_id': user, 'type': cloth_type})
        button_ctrl[cloth_type_id.get(cloth_type)] = True
    else:
        closet_items = items.find({'user_id': user})
        button_ctrl[0] = True
    return render_template('closet/index.html', user=user, items=closet_items, btn_ctrl=button_ctrl)

# 등록 API
@closet_bp.route("/register", methods=["GET", "POST"])
def register_item():

    if request.method == "POST":
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

    return render_template("closet/register.html")


# 옷 상세 API
@closet_bp.route("/<item_id>")
def get_item(item_id):
    item = items.find_one({
        "_id": ObjectId(item_id)
    })

    if not item:
        return jsonify({"message": "옷을 찾을 수 없습니다."}), 404

    item["_id"] = str(item["_id"])

    return jsonify(item), 200

# 옷 상세 - 수정 API
@closet_bp.route("/<item_id>/edit", methods=["POST"])
def fix_item(item_id):
    #try-except로 리팩토링
    
    items.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": {
                "name": request.form.get("name"),
                "brand": request.form.get("brand"),
                "type": request.form.get("type"),
                "size": request.form.get("size"),
                "season": request.form.get("season"),
                "buy_date": request.form.get("buy_date"),
                "price": request.form.get("price"),
                "buy_method": request.form.get("buy_method")
            }}
        )

    return jsonify({"message": "수정 완료"}), 200

# 옷 상세 - 삭제 API
@closet_bp.route("/<item_id>/delete", methods=["DELETE"])
def delete_item(item_id):
    items.deleteOne({"_id": item_id})

    return jsonify({"message": "삭제 완료"}), 200

# 옷 상세 - 오늘 입었어요 API
# @closet_bp.route("/<item_id>/wear", methods=["DELETE"])
# def wear_item(item_id):
#     items.update_one({"_id": item_id},
#                      {"$set": )

#     return jsonify({"message": "삭제 완료"}), 200


# /closet/<item_id>/life-fit
# /closet/life-fit
# /closet/unworn
