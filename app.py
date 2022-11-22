from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)


class Users(db.Model):
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


if __name__ == "__main__":
    app.run(debug=True)
