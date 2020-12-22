from flask import Flask, request, render_template, jsonify, make_response, abort
import json
import datetime
import random
import string
import uuid
from werkzeug.utils import redirect

app = Flask(__name__)


# app.config["JSON_AS_ASCII"] = False


# ３２文字のランダムな文字列生成
def rand_str(n):
    randstr = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randstr)


# session_idからuser_id
def user_idGET(id):
    dt = datetime.datetime.now()

    with open('session.json') as f:
        session_data = json.load(f)
    session_list = list(session_data)

    tmp_list = session_list
    for i in range(len(tmp_list)):
        # print(tmp_list[i])
        tstr = tmp_list[i].get('life_time')
        tdatetime = dt.strptime(tstr, '%Y-%m-%d %H:%M:%S')
        # 差分を計算
        sub = dt - tdatetime
        # 60分以上経過しているものを削除
        if sub.seconds > 3600:
            session_list.remove(tmp_list[i])
    with open('session.json', 'w') as f:
        json.dump(session_list, f, indent=4, ensure_ascii=False)

    for i in range(len(session_list)):
        if id == session_list[i].get('session_id'):
            return session_list[i].get('user_id')
    return None


# user_idからsession_id
def session_idGET(id):
    dt = datetime.datetime.now()

    with open('session.json') as f:
        session_data = json.load(f)
    session_list = list(session_data)

    tmp_list = session_list
    for i in range(len(tmp_list)):
        tstr = tmp_list[i].get('life_time')
        tdatetime = dt.strptime(tstr, '%Y-%m-%d %H:%M:%S')
        # 差分を計算
        sub = dt - tdatetime
        # 60分以上経過しているものを削除
        if sub.seconds > 3600:
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
                # print(haiku_list[i].get('user_id')+"="+user_list[j].get('user_id'))
                # print(user_list[j].get('name'))
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
                # print(dic)
                data_list.insert(0, dic)

    return jsonify(data_list)


@app.route('/haiku', methods=["POST"])
def haiku_post():
    text = request.json.get('text', None)
    cget = request.cookie.get('session_id', None)
    print(cget)
    user_id = user_idGET(cget)
    favorite = 0

    if user_id is None:
        return jsonify({"message": "Error"})

    # date
    dt = datetime.datetime.now()
    now = "{0:%Y-%m-%d %H:%M:%S}".format(dt)

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
    cget = request.cookie.get('session_id', None)
    user_id = user_idGET(cget)
    print(user_id)

    # 追加した処理　ver4
    if user_id is None:
        return jsonify({"message": "Error"})
    with open('user.json') as f:
        user_data = json.load(f)
    user_list = list(user_data)
    for i in range(len(user_list)):
        if user_id == user_list[i].get('user_id'):
            favorite_id = list(user_list[i].get('favorite'))
            add_list = []
            print(favorite_id[1])
            for j in range(len(favorite_id)):
                add_list.append(favorite_id[j])
            add_list.append(id)
            # print(add_list)
            user_list[i]['favorite'] = add_list
            with open('user.json', 'w') as f:
                json.dump(user_list, f, indent=4, ensure_ascii=False)

    # JSON読み込み
    with open('haiku.json') as f:
        haiku_data = json.load(f)

    # リスト型に変換
    haiku_list = list(haiku_data)

    # 認証
    for i in range(len(haiku_list)):
        if haiku_list[i].get("id") == id:
            # いいねを加算
            favorite_num = int(haiku_list[i].get('favorite')) + 1
            tmp_list = haiku_list[i]
            # 元データを削除
            haiku_list.remove(haiku_list[i])
            # 新しいデータを定義
            add_favorite = {
                "id": tmp_list.get("id"),
                "date": tmp_list.get("date"),
                "text": tmp_list.get("text"),
                "user_id": tmp_list.get("user_id"),  # 変更箇所 ServerSide_ver3
                "favorite": favorite_num  # 変更
            }
            # 新しいデータを追加
            haiku_list.insert(i, add_favorite)
            # ファイル書き込み
            with open('haiku.json', 'w') as f:
                json.dump(haiku_list, f, indent=4, ensure_ascii=False)

            return jsonify({"message": "Success"})
        else:
            continue

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
                    flag = True

            dt = datetime.datetime.now()
            now = "{0:%Y-%m-%d %H:%M:%S}".format(dt)

            if not flag:
                dic = {'session_id': session_id, 'user_id': user_id, 'life_time': now}
                session_list.append(dic)

            with open('session.json', 'w') as f:
                json.dump(session_list, f, indent=4, ensure_ascii=False)

            response.set_cookie("session_id", value=session_id)

            return response

    return jsonify({"message": "Error"})


# セッション認証
@app.route('/user/session', methods=["POST"])
def session():
    cget = request.cookies.get('session_id', None)
    print(cget)

    # JSON読み込み
    with open('session.json') as f:
        session_data = json.load(f)

    session_list = list(session_data)

    for i in range(len(session_list)):
        if session_list[i].get('session_id') == cget:
            # 成功なら成功を返す
            return jsonify({"message": "Success"})

    # それ以外ならログインページをリダイレクト
    return redirect('/login')


# アカウント情報の取得
@app.route('/user/<user_id>', methods=["POST", "GET"])
def account_info(user_id):
    # JSON読み込み
    with open('user.json') as f:
        user_data = json.load(f)
    user_list = list(user_data)
    # user_idが一致するか
    flag = False
    for i in range(len(user_list)):
        if user_id == user_list[i].get('user_id'):
            flag = True
    # user_idが存在しなかった場合
    if not flag:
        abort(404, description="Page Not Found")

    if request.method == 'POST':
        # JSON読み込み
        with open('user.json') as f:
            user_data = json.load(f)
        user_list = list(user_data)
        # JSON読み込み
        with open('haiku.json') as f:
            haiku_data = json.load(f)
        haiku_list = list(haiku_data)

        haiku = []
        for i in range(len(haiku_list)):
            if user_id == haiku_list[i].get('user_id'):
                haiku.append(haiku_list[i])

        return jsonify({
            "user_id": user_id,
            "haiku": haiku
        })

    if request.method == 'GET':
        return render_template('user.html')


# http://127.0.0.1:5000/
@app.route('/')
def index():
    cget = request.cookies.get('session_id', None)
    if user_idGET(cget) is None:
        return redirect('/login')

    return render_template("main.html")


# http://127.0.0.1:5000/login
@app.route('/login')
def login():
    cget = request.cookies.get('session_id', None)
    if user_idGET(cget) is None:
        return render_template("login.html")

    return redirect('/')


if __name__ == "__main__":
    # print(session_idGET("admin"))
    # print(user_idGET("bc203eee-3396-464e-b400-830e53e92236"))
    app.run()
