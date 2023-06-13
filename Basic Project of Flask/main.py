import requests
from flask import Flask, render_template


AGE_API_URL = "https://api.agify.io/"
GENDER_API_URL = "https://api.genderize.io/"
app = Flask(__name__)


@app.route("/guess/<name>")
def guess(name):

    user_info = {"name": name}
    user_params = {
        "name": name
    }

    user_info["age"] = requests.get(url=AGE_API_URL, params=user_params).json()["age"]
    user_info["gender"] = requests.get(url=GENDER_API_URL, params=user_params).json()["gender"]

    return render_template("index.html", user=user_info)


if __name__ == "__main__":
    app.run(debug=True)