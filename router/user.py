from flask import request, render_template, jsonify, make_response, abort, Blueprint
from datetime import datetime
import json
import uuid

app = Blueprint('user', __name__)


# アカウント認証
@app.route('/user/login', methods=["POST"])
def user_login():
    user_id = request.json.get('user_id', None)
    ps = request.json.get('password', None)

    # JSON読み込み
    with open('user.json') as f:
        user_data = json.load(f)
    user_list = list(user_data)

    session_id = str(uuid.uuid4())
    now_time = datetime.now()
    now = "{0:%Y-%m-%d %H:%M:%S}".format(now_time)

    for i in range(len(user_list)):
        if user_list[i].get('user_id') == user_id and user_list[i].get('password') == ps:
            # JSON読み込み
            with open('session.json') as f:
                session_data = json.load(f)
            session_list = list(session_data)
            # 追加
            flag = False

            for j in range(len(session_list)):
                if session_list[j].get('user_id') == user_id:
                    session_list[j]['session_id'] = session_id
                    session_list[j]['life_time'] = now
                    flag = True

            if not flag:
                dic = {'session_id': session_id,
                       'user_id': user_id, 'life_time': now}
                session_list.append(dic)

            with open('session.json', 'w') as f:
                json.dump(session_list, f, indent=4, ensure_ascii=False)

            response = make_response(jsonify({"message": "Success"}))
            response.set_cookie("session_id", value=session_id)
            return response

    return jsonify({"message": "Error"})


@app.route('/user/logout', methods=["POST"])
def user_logout():
    cookie = request.cookies.get('session_id', None)

    with open('session.json') as f:
        session_data = json.load(f)
    session_list = list(session_data)

    for i in range(len(session_list)):
        if session_list[i].get('session_id') == cookie:
            session_list.remove(session_list[i])
            with open('session.json', 'w') as f:
                json.dump(session_list, f, indent=4, ensure_ascii=False)
            return jsonify({"message": "Success"})

    return jsonify({"message": "Error"})


# セッション認証
@app.route('/user/session', methods=["POST"])
def session():
    cookie = request.cookies.get('session_id', None)

    # JSON読み込み
    with open('session.json') as f:
        session_data = json.load(f)
    session_list = list(session_data)

    for i in range(len(session_list)):
        if session_list[i].get('session_id') == cookie:
            # 成功なら成功を返す
            return jsonify({"message": "Success"})

    return jsonify({"message": "Error"})


# アカウント情報の取得
@app.route('/user/<user_id>', methods=["POST", "GET"])
def account_info(user_id):
    # JSON読み込み
    with open('user.json') as f:
        user_data = json.load(f)
    user_list = list(user_data)

    with open('haiku.json') as f:
        haiku_data = json.load(f)
    haiku_list = list(haiku_data)

    if request.method == 'GET':
        for i in range(len(user_list)):
            if user_id == user_list[i].get('user_id'):
                return render_template('user.html')
        abort(404, description="Page Not Found")

    if request.method == 'POST':
        user = {}
        for i in range(len(user_list)):
            if user_id == user_list[i].get('user_id'):
                user = user_list[i]

        haiku = {}
        for i in range(len(haiku_list)):
            if user.get('user_id') == haiku_list[i].get('user_id'):
                haiku = haiku_list[i]

        if user == {}:
            return jsonify({"message": "Error"})

        return jsonify({
            "id": haiku['id'],
            "text": haiku['text'],
            "date": haiku['date'],
            "favorite": haiku['favorite'],
            "user": {
                "id": user['user_id'],
                "name": user['name'],
                "image": user['image']
            }
        })
