"""
Flask server innitializing
"""

from flask import Flask, render_template, request
from parsing import change_map

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("domain")
    try:
        try:
            if name:
                change_map(name)
                return render_template("Map.html")
            else:
                return render_template("failure.html")
        except IndexError:
            return render_template('error.html')
    except KeyError:
        return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=8080)
