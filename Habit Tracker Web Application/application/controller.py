from main import app
from flask import make_response, request, jsonify, send_file
from application.additional_functions import token_required
from application.models import *


@app.route("/", methods=["GET", "POST"])
def greetings():
    if request.method == "GET":
        return "Hello World from Get", 200
    data = request.get_json()

    return "Hello World from POST", 200


@app.route("/security", methods=["GET"])
@token_required
def security():
    print(request.headers["Authorization-Token"])
    return make_response(jsonify({"message": "Secured Area"}), 200)


# For Celery
# @app.route("/get_csv", methods=["POST"])
# @token_required
# def csv_file():
#     data = request.get_json()
#     if data["category"] == "user_trackers":
#         user = Users.query.get(data["id"])
#
#         if not user:
#             return make_response(jsonify({"message": "User id doesn't exist"}), 404)
#
#         get_trackers_csv(user)
#
#     elif data["category"] == "tracker_logs":
#         tracker = Trackers.query.get(data["id"])
#
#         if not tracker:
#             return make_response(jsonify({"message": "Tracker id doesn't exist"}), 404)
#
#         get_logs_csv(tracker)
#
#     resp = make_response(send_file("../application/static/export.csv", as_attachment=True, download_name="testing.csv"), 200)
#     resp.headers["Content-Type"] = "text/csv"
#
#     return resp
