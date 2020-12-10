from flask import Flask, request, render_template, jsonify
import json
import datetime
import random
import string

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


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
    text = request.form.get('text', None)
    name = request.form.get('name', None)
    favorite = request.form.get('favorite', None)

    # date
    dt = datetime.datetime.now()
    now = "{0:%Y-%m-%d-%H:%M}".format(dt)

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
    if not id or not now or not text or not name or not favorite:
        return jsonify({
            "message": "Error"
        })

    # JSON読み込み
    with open('haiku.json') as f:
        haiku_data = json.load(f)
    # list変換
    json_list = list(haiku_data)
    # 入力されたデータを追加
    json_list.append(dic)
    # 追加されたlistを書き込み
    with open('haiku.json', 'w') as f:
        json.dump(json_list, f, indent=3)

    return jsonify({
        "message": "Success"
    })


@app.route('/haiku/favorite', methods=["POST"])
def haiku_post_favorite():
    id = request.form.get('id', None)
    date = request.form.get('date', None)
    text = request.form.get('text', None)
    name = request.form.get('name', None)
    favorite = request.form.get('favorite', None)

    # 認証用
    check = {
        "id": id,
        "date": date,
        "text": text,
        "name": name,
        "favorite": favorite
    }

    # JSON読み込み
    with open('haiku.json') as f:
        haiku_data = json.load(f)

    # リスト型に変換
    haiku_list = list(haiku_data)

    # フラグ
    flag = False

    # 認証
    for i in range(len(haiku_list)):
        if haiku_list[i] == check:
            flag = True
            # いいねを加算
            favorite_num = int(check.get('favorite')) + 1
            # 元データを削除
            haiku_list.remove(check)
            # 新しいデータを定義
            add_favorite = {
                "id": id,
                "date": date,
                "text": text,
                "name": name,
                "favorite": favorite_num  # 変更
            }
            # 新しいデータを追加
            haiku_list.append(add_favorite)
            # ファイル書き込み
            with open('haiku.json', 'w') as f:
                json.dump(haiku_list, f, indent=3)
        else:
            continue

    if not flag:
        return jsonify({
            "message": "Error"
        })

    return jsonify({
        "message": "Success"
    })


# http://127.0.0.1:5000/
@app.route('/')
def index():
    return render_template("main.html")


if __name__ == "__main__":
    app.run()
