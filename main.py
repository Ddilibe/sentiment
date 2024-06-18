#!/usr/bin/env python3

from flask import Flask, redirect, request, render_template, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
 
db.init_app(app)
 
with app.app_context():
    db.create_all() 

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/', methods=["GET"])
def home():
  return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
  # Access data from request (if any)
  name = request.json
  print(name)

  # Perform your logic here and generate the content
  content = f"Hello, {name}! This is the updated content segment."
  # The logic goes here

  # Return the generated content as a string
  return jsonify({'answer':'True'})

@app.route('/login', methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
     user = Users.query.filter_by(username=request.form.get('username')).first()
     if user.password == request.form.get('password'):
        login_user(user)
        return redirect(url_for('dashboard'))
  return render_template('login.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  if request.method == "POST":
    user = Users(
       username=request.form.get('username'),
       password=request.form.get('password'),
       email=request.form.get('email')
       )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))
  return render_template('signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
   if not(current_user.is_authenticated):
      return redirect(url_for('login'))
   return render_template('dashboard.html')

@app.route('/logout', methods=['GET'])
def logout():
   logout_user()
   return redirect(url_for('home'))


if __name__ == "__main__":
  app.run(debug=False)
