from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask.ext.scss import Scss

app = Flask(__name__)
Scss(app, static_dir='static', asset_dir='assets')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hello.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    posts = db.relationship('Post', backref='user', lazy=True) # 複数の Post への紐付け

    def __init__(self, username, posts=[]):
        self.username = username
        self.posts = posts # ユーザ追加時は基本的に空だと思いますが、念のため追加できるようにしておく

# Post クラスを追加
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # 一人の User への紐付け

    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id

    def __str__(self):
        return self.title


@app.route("/")
def top():
    user_list = User.query.all()
    return render_template('top.html', title='ユーザ一覧', user_list=user_list)

@app.route("/add_user", methods=['POST'])
def add_user():
    username = request.form.get('username')
    if username:
        user = User(username)
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('top'))

@app.route("/user/<int:user_id>", methods=['GET'])
def show_user(user_id):
    target_user = User.query.get(user_id)

    return render_template('show.html', title='Query Share', target_user=target_user)

@app.route("/user/<int:user_id>", methods=['POST'])
def mod_user(user_id):
    target_user = User.query.get(user_id)
    username = request.form.get('username')
    if target_user and username:
        target_user.username = username
        db.session.commit()

    return redirect(url_for('top'))

@app.route("/del_user/<int:user_id>", methods=['POST'])
def del_user(user_id):
    target_user = User.query.get(user_id)
    if target_user:
        db.session.delete(target_user)
        db.session.commit()

    return redirect(url_for('top'))




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)
