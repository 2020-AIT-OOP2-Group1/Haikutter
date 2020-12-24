from datetime import datetime
import json
import random
import string
import copy

LIMIT_TIME = 3600

# ３２文字のランダムな文字列生成
def rand_str(n):
    randstr = [random.choice(string.ascii_letters + string.digits)
               for i in range(n)]
    return ''.join(randstr)


# session_idからuser_id
def getUserId(id):
    with open('session.json') as f:
        session_data = json.load(f)
    session_list = list(session_data)
    tmp_list = copy.deepcopy(session_list)

    now_time = datetime.now()

    for i in range(len(tmp_list)):
        life_time = datetime.strptime(
            tmp_list[i]['life_time'], '%Y-%m-%d %H:%M:%S')
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
        life_time = datetime.strptime(
            tmp_list[i]['life_time'], '%Y-%m-%d %H:%M:%S')
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