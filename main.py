from flask import Flask, request, render_template, jsonify
import json
import datetime
import random
import string

app = Flask(__name__)
# app.config["JSON_AS_ASCII"] = False


# ３２文字のランダムな文字列生成
def rand_str(n):
    randstr = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randstr)


# http://127.0.0.1:5000/haiku
@app.route('/haiku', methods=["GET"])
def haiku_get():
    with open('haiku.json') as f:
        json_data = json.load(f)

    return jsonify(json_data)


@app.route('/haiku', methods=["POST"])
def haiku_post():
    text = request.json.get('text', None)
    name = request.json.get('name', None)
    favorite = 0

    # date
    dt = datetime.datetime.now()
    now = "{0:%Y-%m-%d-%H:%M:%S}".format(dt)

    # id
    id = rand_str(32)

    dic = {
        "id": id,
        "date": now,
        "text": text,
        "name": name,
        "favorite": favorite
    }

    # 値が入ってなかった場合の処理
    if not id or not now or not text or not name or not favorite==0:
        return jsonify({
            "message": "Error"
        })

    # JSON読み込み
    with open('haiku.json') as f:
        haiku_data = json.load(f)
    # list変換
    json_list = list(haiku_data)
    # 入力されたデータを追加
    json_list.insert(0,dic)
    # 追加されたlistを書き込み
    with open('haiku.json', 'w') as f:
        json.dump(json_list, f, indent=4, ensure_ascii=False)

    return jsonify({
        "message": "Success"
    })


@app.route('/haiku/favorite', methods=["POST"])
def haiku_post_favorite():
    id = request.json.get('id', None)

    # JSON読み込み
    with open('haiku.json') as f:
        haiku_data = json.load(f)

    # リスト型に変換
    haiku_list = list(haiku_data)

    # フラグ
    flag = False

    # 認証
    for i in range(len(haiku_list)):
        if haiku_list[i].get("id") == id:
            flag = True
            # いいねを加算
            favorite_num = int(haiku_list[i].get('favorite')) + 1
            tmp_list = haiku_list[i];
            # 元データを削除
            haiku_list.remove(haiku_list[i])
            # 新しいデータを定義
            add_favorite = {
                "id": tmp_list.get("id"),
                "date": tmp_list.get("date"),
                "text": tmp_list.get("text"),
                "name": tmp_list.get("name"),
                "favorite": favorite_num  # 変更
            }
            # 新しいデータを追加
            haiku_list.insert(i,add_favorite)
            # ファイル書き込み
            with open('haiku.json', 'w') as f:
                json.dump(haiku_list, f, indent=4, ensure_ascii=False)
        else:
            continue

    if not flag:
        return jsonify({
            "message": "Error"
        })

    return jsonify({
        "message": "Success"
    })


<<<<<<< Updated upstream
=======
# アカウント認証
@app.route('/user/login', methods=["POST"])
def user_login():
    print('/user/login(POST')
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
            print('test')
            dic = {'session_id': session_id,
                   'user_id': user_id
                   }
            # JSON読み込み
            with open('session.json') as f:
                session_data = json.load(f)

            session_list = list(session_data)
            # 追加
            session_list.append(dic)
            with open('session.json', 'w') as f:
                json.dump(dic, f, indent=4, ensure_ascii=False)

            return response.set_cookie('cookie_name', value=json.dumps(dic))

    return jsonify({"message": "Error"})


# セッション認証
@app.route('/session', methods=["POST"])
def session_main():
    print('session(POST)')
    cget = request.cookies.get('session_id', None)
    print(cget)

    # JSON読み込み
    with open('session.json') as f:
        session_data = json.load(f)
    session_list = list(session_data)

    for i in range(len(session_list)):
        if session_list[i].get('session_id') == cget:
            # 成功なら成功を返す
            return jsonify({
                "message": "Success"
            })
    # それ以外ならログインページをリダイレクト
    return redirect('login.html')


# アカウント情報の取得
@app.route('/user/<user_id>', methods=["POST", "GET"])
def account_info(user_id):
    print('/user/' + user_id)

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
        abort(404, description="Not Found")

    if request.method == 'POST':

        # JSON読み込み
        with open('user.json') as f:
            user_data = json.load(f)
        user_list = list(user_data)
        # JSON読み込み
        with open('haiku.json') as f:
            haiku_data = json.load(f)
        haiku_list = list(haiku_data)

        haiku_id = []
        # user_idが一致するアカウントの俳句idを取得　→ listにappend
        for i in range(len(user_list)):
            if user_id == user_list[i].get('user_id'):
                haiku_id.append(user_list[i].get('id'))

        haiku_text = []
        # haiku_idとhaiku_listの俳句idが一致したら俳句をlistにappend
        try:
            for i in range(len(haiku_list)):
                for j in range(len(haiku_list)):
                    if haiku_id[i] == haiku_list[j].get('id'):
                        haiku_text.append(haiku_list[j])
        except IndexError:
            pass

        return jsonify({
            "user_id": user_id,
            "haiku": haiku_text
        })

    if request.method == 'GET':
        return render_template('user.html')


>>>>>>> Stashed changes
# http://127.0.0.1:5000/
@app.route('/')
def index():
    return render_template("main.html")

# http://127.0.0.1:5000/login
@app.route('/login')
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run()
