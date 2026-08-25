from flask import Flask, redirect, url_for, session, request, jsonify

from config import Config
from routes.auth import auth_bp
from routes.closet import closet_bp
from routes.mypage import mypage_bp

from db import *

app = Flask(__name__)
app.config.from_object(Config)

# Blueprint 등록
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(closet_bp, url_prefix="/closet")
app.register_blueprint(mypage_bp, url_prefix="/mypage")


@app.route("/")
def index():
    #로그인 유무에 따라 화면 이동
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return redirect(url_for("closet.index"))

@app.route("/check-id-unique", methods=['GET'])
def check_id_unique():
    ID = request.args.get('id')
    print(ID)
    test = users.find_one({'user_id': ID})
    if not test:
        return jsonify({'status': 'success', 'message': '사용 가능한 아이디입니다.'})
    else:
        return jsonify({'status': 'failure', 'message': '입력하신 아이디가 이미 존재합니다.'})

@app.route("/check-nick-unique", methods=['GET'])
def check_nick_unique():
    nick = request.args.get('nick')
    print(nick)
    test = users.find_one({'nickname': nick})
    if not test:
        return jsonify({'status': 'success', 'message': '사용 가능한 닉네임입니다.'})
    else:
        return jsonify({'status': 'failure', 'message': '입력하신 닉네임이 이미 존재합니다.'})

@app.route('/proceed-signup', methods=['POST'])
def proceed_signup():
    ID = request.form['final_id']
    pw = request.form['final_pw']
    nick = request.form['final_nick']
    users.insert_one({'user_id': ID, 'user_pw': pw, 'nickname': nick})
    return jsonify({'status': 'success', 'message': '회원가입이 완료되었습니다.'})

if __name__ == "__main__":
    app.run(debug=True)
