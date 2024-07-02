#!/usr/bin/env python3

import pickle
from flask import Flask, redirect, request, render_template, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from dotenv import load_dotenv
import os
# from nltk.stem import PorterStemmer
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# import joblib
# import nltk
# import re
# import string
load_dotenv()

app = Flask(__name__)
# with open('models/amazon_sentient.sav', 'rb') as file:
#    model = pickle.load(file)
# vect = joblib.load('models/sentiment_vectorizer.joblib', 'rb')
# nltk.download('punkt')
# nltk.download('stopwords')

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

def process_answer(ans):
   ans = sorted(ans[0], key=lambda x: x['score'])
   if ans['label_0'] > 0.65:
      return 'Negative'
   elif ans['label_1'] > 0.65:
      return 'Positive'
   else:
      return 'Netural'

# def process_text(text):
#   stop_words = set(stopwords.words('english'))
#   def processing(data):
#     pattern = r"(?:^a-zA-Z0-9)|(?:https\S+|www\S+https\S+)|[@#]\W+"
#     text = re.sub(pattern, " ", data)
#     data = data.lower()
#     data_tok = word_tokenize(data.translate(str.maketrans('', '', string.punctuation)))
#     filter_text = [w for w in data_tok if not w in stop_words]
#     return " ".join(filter_text)
#   def stemming(data):
#     text = [PorterStemmer().stem(word) for word in data]
#     return data
#   text = stemming(processing(text))
#   text = vect.transform([text])
#   return text
   

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/', methods=["GET"])
def home():
  return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
  import requests
  # Access data from request (if any)
  body = request.json
  text = body.get('text')
  # ans = model.predict(text)

  API_URL = "https://api-inference.huggingface.co/models/ashok2216/gpt2-amazon-sentiment-classifier-V1.0"
  headers = {"Authorization": f"Bearer {os.environ['huggingface']}"}

  def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
    
  output = query({
    "inputs": text,
  })
  return jsonify({'ans':process_answer(output)}), 200


  # Perform your logic here and generate the content
  # content = f"Hello, {name}! This is the updated content segment."
  # The logic goes here

  # Return the generated content as a string
  # return jsonify({'answer':'True'})

@app.route('/login', methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
     if user := Users.query.filter_by(username=request.form.get('username')).first():
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
  app.run(debug=True)
