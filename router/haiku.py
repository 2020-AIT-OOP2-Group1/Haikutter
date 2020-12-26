from flask import request, jsonify, Blueprint
from datetime import datetime
import json
from module.function import getUserId, rand_str

app = Blueprint('haiku', __name__)


# http://127.0.0.1:5000/haiku
@app.route('/haiku', methods=["GET"])
def haiku_get():  # 変更箇所 ServerSide_ver3
    session_id = request.cookies.get('session_id', None)
    user_id = getUserId(session_id)

    liked_haiku_list = []
    with open('user.json') as f:
        user_data = json.load(f)
    user_list = list(user_data)
    for i in range(len(user_list)):
        if user_id == user_list[i].get('user_id'):
            liked_haiku_list = user_list[i]['favorite']

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
                    "id": haiku_list[i].get('id'),
                    "text": haiku_list[i].get('text'),
                    "date": haiku_list[i].get('date'),
                    "favorite": haiku_list[i].get('favorite'),
                    "user": {
                        "id": user_list[j].get('user_id'),
                        "name": user_list[j].get('name'),
                        "image": user_list[j].get('image')
                    },
                }
                if not user_id is None:
                    dic["liked"] = "True" if haiku_list[i].get(
                        'id') in liked_haiku_list else "False"

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
    json_list.append(dic)
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


@app.route('/haiku/delete', methods=["POST"])
def haiku_delete():
    id = request.json.get('id', None)
    session_id = request.cookies.get('session_id', None)
    user_id = getUserId(session_id)
    flag = False

    if user_id is None:
        return jsonify({"message": "Error"})

    with open('haiku.json') as f:
        haiku_data = json.load(f)
    haiku_list = list(haiku_data)
    tmp_list = list(haiku_data)

    for i in range(len(haiku_list)):
        if id == haiku_list[i]['id'] and user_id == haiku_list[i]['user_id']:
            flag = True
            tmp_list.remove(haiku_list[i])

    with open('haiku.json', 'w') as f:
        json.dump(tmp_list, f, indent=4, ensure_ascii=False)

    if not flag:
        return jsonify({"message": "Error"})

    return jsonify({"message": "Success"})
