from flask import Blueprint

from flask import Blueprint, render_template, request, jsonify, session

from db import *

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/check-id", methods=['GET'])
def check_id_unique():
    ID = request.args.get('id')
    print(ID)
    test = users.find_one({'user_id': ID})
    if not test:
        return jsonify({'status': 'success', 'message': '사용 가능한 아이디입니다.'})
    else:
        return jsonify({'status': 'failure', 'message': '입력하신 아이디가 이미 존재합니다.'})

@auth_bp.route("/check-nickname", methods=['GET'])
def check_nick_unique():
    nick = request.args.get('nick')
    print(nick)
    test = users.find_one({'nickname': nick})
    if not test:
        return jsonify({'status': 'success', 'message': '사용 가능한 닉네임입니다.'})
    else:
        return jsonify({'status': 'failure', 'message': '입력하신 닉네임이 이미 존재합니다.'})

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        ID = request.form['final_id']
        pw = request.form['final_pw']
        nick = request.form['final_nick']
        users.insert_one({'user_id': ID, 'user_pw': pw, 'nickname': nick})
        return jsonify({'status': 'success', 'message': '회원가입이 완료되었습니다.'})
    
    return render_template('auth/signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ID = request.form['userid']
        pw = request.form['userpw']
        test = users.find_one({ 'user_id': ID, 'user_pw': pw })
        if test:
            session['user_id'] = ID
            return jsonify({ 'status': 'success', 'message': f'로그인 되었습니다.\n{ID}님, 환영합니다.' })
        else:
            return jsonify({ 'status': 'failure', 'message': '아이디와 비밀번호를 다시 확인해주세요. '})
    
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET'])
def proceed_logout():
    session.pop('user_id', None)
    return jsonify({ 'status': 'success' })