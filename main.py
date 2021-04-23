from flask import Flask, render_template, redirect, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from Forms import SignUpForm, LoginForm, EditForm
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get("S_KEY")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


uri = os.getenv("DATABASE_URL", "sqlite:///crypto.db")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    frequency = db.Column(db.String(1), nullable=False)


db.create_all()


@app.route('/', methods=('GET', 'POST'))
def signup():
    form = SignUpForm()
    if form.validate_on_submit():

        if User.query.filter_by(username=form.username.data).first():
            print(User.query.filter_by(username=form.username.data).first())
            flash("You appear to be already signed up, maybe try to log in?")
            return redirect(url_for('login'))

        hash_password = generate_password_hash(password=form.password.data, method='pbkdf2:sha256', salt_length=12)
        new_user = User(username=form.username.data, password=hash_password, frequency=form.frequency.data)

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("access"))

    return render_template('index.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Username does not appear in our system, please try again")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Password  is incorrect, try again")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for("access"))

    return render_template('login.html', form=form)


@app.route("/edit/<int:user_id>", methods=('GET', 'POST'))
def edit(user_id):
    user_to_update = User.query.get(user_id)
    form = EditForm(
        username=current_user.username,
        frequency=current_user.frequency
    )

    if form.validate_on_submit():
        user_to_update.username = form.username.data
        user_to_update.frequency = form.frequency.data
        db.session.commit()
        print("success")
        return redirect(url_for('access'))

    else:
        print(form.errors)

    return render_template('login.html', form=form, is_edit=True)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/access', methods=('GET', 'POST'))
def access():
    articles = pd.read_csv("articles.csv")
    return render_template('access.html', current_user=current_user, articles=articles)


@app.route('/delete/<int:user_id>', methods=('GET', 'POST'))
def delete(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/')
def about():
    return render_template('index.html')


@app.route('/')
def services():
    return render_template('index.html')


@app.route('/')
def reviews():
    return render_template('index.html')


@app.route('/')
def contact():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
