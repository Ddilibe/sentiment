from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

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

if __name__ == "__main__":
  app.run(debug=False)
