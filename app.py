
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///password_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.user_id}-{self.password}"


class Password(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    user_id_sno = db.Column(db.Integer, nullable=False)
    website = db.Column(db.String(200), nullable=False)
    website_username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.user_id_sno}-{self.website_username}-{self.password}"


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        allUsers = User.query.all()
        l = []
        print(l)
        for i in allUsers:
            l.append(i.user_id)

        if username not in l:
            user = User()
            user.user_id = username
            user.password = password
            db.session.add(user)
            db.session.commit()
            return redirect(f"/{user.sno}")
        else:
            return render_template("user_already_exists.html")
    return render_template("signup.html")


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(user_id=username).first()

        allUsers = User.query.all()
        l = []
        for i in allUsers:
            l.append(i.user_id)

        if (username not in l) or (user.password != password):
            return render_template("invalid_credentials.html")

        elif user.password == password:
            return redirect(f"/{user.sno}")
    return render_template("login.html")


@app.route("/<int:sno>", methods=['GET', 'POST'])
def hello_world(sno):
    allPass = Password.query.filter_by(user_id_sno=sno)
    t = []
    for i in allPass:
        t.append(i)
    return render_template("index.html", allPass=t, sno=sno)


@app.route("/add/<int:sno>", methods=['GET', 'POST'])
def add(sno):
    if request.method == "POST":
        website = request.form['website']
        website_username = request.form['username']
        password = request.form['password']
        password_entry = Password(user_id_sno=sno, website=website,
                                  website_username=website_username, password=password)
        db.session.add(password_entry)
        db.session.commit()
        return redirect(f"/{sno}")
    return render_template("add.html", sno=sno)


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        website = request.form['website']
        website_username = request.form['username']
        password = request.form['password']

        password_entry = Password.query.filter_by(sno=sno).first()
        user_id_sno = password_entry.user_id_sno
        password_entry.website = website
        password_entry.website_username = website_username
        password_entry.password = password

        db.session.add(password_entry)
        db.session.commit()

        return redirect(f"/{user_id_sno}")
    password_entry = Password.query.filter_by(sno=sno).first()
    return render_template("update.html", password=password_entry)


@app.route("/delete/<int:sno>")
def delete(sno):
    password = Password.query.filter_by(sno=sno).first()
    user_id_sno = password.user_id_sno
    db.session.delete(password)
    db.session.commit()
    allPass = Password.query.all()
    return redirect(f'/{user_id_sno}')


@app.route("/show")
def show():
    return "printed all users"


if __name__ == "__main__":
    app.run(debug=True, port=8000)
