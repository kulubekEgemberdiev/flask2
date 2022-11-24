from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = '1de413123ecdd3f7765b65170b90a1cefda37679'
db = SQLAlchemy(app)
manager = LoginManager(app)


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"users {self.id}."


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer)
    country = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"users {self.id}."


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/employees")
def second_page():
    return render_template("second.html")


@app.route("/contacts")
def third_page():
    return render_template("third.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html")


@app.errorhandler(401)
def page_not_found(error):
    return render_template("page_401.html")


@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        try:
            hash = generate_password_hash(request.form['password'])
            user = Users(email=request.form['email'], password=hash)
            db.session.add(user)
            db.session.flush()

            profile = Profiles(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                age=request.form['age'],
                country=request.form['country'],
                user_id=user.id
            )
            db.session.add(profile)
            db.session.commit()
        except:
            db.session.rollback()
    return render_template("register.html")


@app.route('/login', methods=("POST", "GET"))
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(2000), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Articles {self.title}."


@app.route("/add-article", methods=("POST", "GET"))
@login_required
def articles():
    if request.method == "POST":
        try:
            title = request.form['title']
            description = request.form['desc']
            article = Articles(title=title, description=description)
            db.session.add(article)
            db.session.commit()
        except:
            db.session.rollback()
    return render_template("article.html")


if __name__ == "__main__":
    app.run(debug=True)
