from flask import Flask, request, render_template, jsonify, make_response, abort
from werkzeug.utils import redirect
from datetime import datetime
import json, random, string, uuid, copy

app = Flask(__name__)
# app.config["JSON_AS_ASCII"] = False

LIMIT_TIME = 3600

# ３２文字のランダムな文字列生成
def rand_str(n):
    randstr = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randstr)


# session_idからuser_id
def getUserId(id):
    with open('session.json') as f:
        session_data = json.load(f)
    session_list = list(session_data)
    tmp_list = copy.deepcopy(session_list)

    now_time = datetime.now()

    for i in range(len(tmp_list)):
        life_time = datetime.strptime(tmp_list[i]['life_time'], '%Y-%m-%d %H:%M:%S')
        # 差分を計算
        sub = now_time - life_time
        # LIMIT_TIME以上経過しているものを削除
        if sub.seconds > LIMIT_TIME:
            session_list.remove(tmp_list[i])

    with open('session.json', 'w') as f:
        json.dump(session_list, f, indent=4, ensure_ascii=False)

    for i in range(len(session_list)):
        if id == session_list[i].get('session_id'):
            return session_list[i].get('user_id')

    return None


# user_idからsession_id
def getSessionId(id):
    with open('session.json') as f:
        session_data = json.load(f)
    session_list = list(session_data)
    tmp_list = copy.deepcopy(session_list)

    now_time = datetime.now()

    for i in range(len(tmp_list)):
        life_time = datetime.strptime(tmp_list[i]['life_time'], '%Y-%m-%d %H:%M:%S')
        # 差分を計算
        sub = now_time - life_time
        # LIMIT_TIME分以上経過しているものを削除
        if sub.seconds > LIMIT_TIME:
            session_list.remove(tmp_list[i])

    with open('session.json', 'w') as f:
        json.dump(session_list, f, indent=4, ensure_ascii=False)

    for i in range(len(session_list)):
        if id == session_list[i].get('user_id'):
            return session_list[i].get('session_id')

    return None


# http://127.0.0.1:5000/haiku
@app.route('/haiku', methods=["GET"])
def haiku_get():  # 変更箇所 ServerSide_ver3
    with open('haiku.json') as f:
        haiku_data = json.load(f)
    haiku_list = list(haiku_data)
    
    with open('user.json') as f:
        user_data = json.load(f)
    user_list = list(user_data)

    data_list = []

    for i in range(len(haiku_list)):
        for j in range(len(user_list)):
            if haiku_list[i].get('user_id') == user_list[j].get('user_id'):
                dic = {
                    "date": haiku_list[i].get('date'),
                    "favorite": haiku_list[i].get('favorite'),
                    "id": haiku_list[i].get('id'),
                    "user": {
                        "id": user_list[j].get('user_id'),
                        "name": user_list[j].get('name'),
                        "image": user_list[j].get('image')
                    },
                    "text": haiku_list[i].get('text'),
                }
                data_list.insert(0, dic)

    return jsonify(data_list)


@app.route('/haiku', methods=["POST"])
def haiku_post():
    text = request.json.get('text', None)
    session_id = request.cookies.get('session_id', None)
    user_id = getUserId(session_id)
    favorite = 0

    if user_id is None:
        return jsonify({"message": "Error"})

    # date
    now_time = datetime.now()
    now = "{0:%Y-%m-%d %H:%M:%S}".format(now_time)

    # id
    id = rand_str(32)

    dic = {
        "id": id,
        "date": now,
        "text": text,
        "user_id": user_id,
        "favorite": favorite
    }

    # 値が入ってなかった場合の処理
    if not id or not now or not text or not user_id or not favorite == 0:
        return jsonify({"message": "Error"})

    # JSON読み込み
    with open('haiku.json') as f:
        haiku_data = json.load(f)
    # list変換
    json_list = list(haiku_data)
    # 入力されたデータを追加
    json_list.insert(0, dic)
    # 追加されたlistを書き込み
    with open('haiku.json', 'w') as f:
        json.dump(json_list, f, indent=4, ensure_ascii=False)

    return jsonify({"message": "Success"})


@app.route('/haiku/favorite', methods=["POST"])
def haiku_favorite():
    id = request.json.get('id', None)
    session_id = request.cookies.get('session_id', None)
    user_id = getUserId(session_id)

    # 追加した処理　ver4
    if user_id is None:
        return jsonify({"message": "Error"})

    num = 0

    with open('user.json') as f:
        user_data = json.load(f)
    user_list = list(user_data)

    for i in range(len(user_list)):
        if user_id == user_list[i].get('user_id'):
            if id in user_list[i]['favorite']:
                user_list[i]['favorite'].remove(id)
                num = -1
            else:
                user_list[i]['favorite'].append(id)
                num = 1

            with open('user.json', 'w') as f:
                json.dump(user_list, f, indent=4, ensure_ascii=False)

    with open('haiku.json') as f:
        haiku_data = json.load(f)
    haiku_list = list(haiku_data)

    # 認証
    for i in range(len(haiku_list)):
        if haiku_list[i].get("id") == id:
            haiku_list[i]['favorite'] = int(haiku_list[i]['favorite']) + num
            # ファイル書き込み
            with open('haiku.json', 'w') as f:
                json.dump(haiku_list, f, indent=4, ensure_ascii=False)

            return jsonify({"message": "Success"})

    return jsonify({"message": "Error"})


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
            response = make_response(render_template('main.html'))
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
                dic = {'session_id': session_id, 'user_id': user_id, 'life_time': now}
                session_list.append(dic)

            with open('session.json', 'w') as f:
                json.dump(session_list, f, indent=4, ensure_ascii=False)

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

        haiku = []
        for i in range(len(haiku_list)):
            if user.get('user_id') == haiku_list[i].get('user_id'):
                haiku.append(haiku_list[i])

        if user == {}:
            return jsonify({"message": "Error"})

        return jsonify({
            "user_id": user['user_id'],
            "name": user['name'],
            "image": user['image'],
            "haiku": haiku
        })


# http://127.0.0.1:5000/
@app.route('/')
def index():
    session_id = request.cookies.get('session_id', None)
    if getUserId(session_id) is None:
        return redirect('/login')

    return render_template("main.html")


# http://127.0.0.1:5000/login
@app.route('/login')
def login():
    session_id = request.cookies.get('session_id', None)
    if getUserId(session_id) is None:
        return render_template("login.html")

    return redirect('/')


if __name__ == "__main__":
    app.run()
