import os
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "Secretproductionkey1234"
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"), debug=True)