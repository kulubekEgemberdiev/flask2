from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/employees")
def second_page():
    return render_template("second.html")


@app.route("/contacts")
def third_page():
    return render_template("third.html")


if __name__ == "__main__":
    app.run(debug=True)
