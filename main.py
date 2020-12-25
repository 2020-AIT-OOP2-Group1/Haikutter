from flask import Flask, request, render_template, jsonify, make_response, abort, Blueprint
from werkzeug.utils import redirect
from router import haiku, user
from module.function import getUserId

app = Flask(__name__)
# app.config["JSON_AS_ASCII"] = False
app.register_blueprint(haiku.app)
app.register_blueprint(user.app)

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
