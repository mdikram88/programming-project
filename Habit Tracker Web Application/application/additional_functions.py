# import pandas as pd
import re
import json
import csv
import smtplib
from os.path import basename
import jsonpickle
import matplotlib.pyplot as plt
from weasyprint import HTML
from functools import wraps
from jinja2 import Template
from flask import request, jsonify, make_response
import jwt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from application.additional_variables import TRACKER_INFO, TRACKER_HEADERS, LOG_INFO, LOG_HEADER, REGREX, EMAIL, PASSWORD
from application.keys import SECRET_KEY


def clean_json(record):
    # Making Whole Object active
    if record.trackers:
        for i in range(len(record.trackers)):
            if record.trackers[i].logs:
                pass

    json_record = jsonpickle.encode(record, unpicklable=False)
    temp = json.loads(json_record)
    del temp["_sa_instance_state"]
    return json.dumps(temp)


def update_headers(req, tk=None, status=False):
    req.headers["Content-Type"] = "application/json"
    req.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:8080"

    if status:
        req.headers["Authorization-Token"] = tk
        req.headers["Access-Control-Expose-Headers"] = "Authorization-Token"
    return req


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers["Authorization-Token"]
        except KeyError:
            return make_response(jsonify({'message': 'Token is Missing!'}), 401)

        try:
            jwt.decode(token, SECRET_KEY, algorithms="HS256")
            return f(*args, **kwargs)

        except:
            return make_response(jsonify({'message': 'Token is invalid!'}), 401)

    return decorated


def validate_email(email):
    return re.fullmatch(REGREX, email)


def validate_user_data(ag):
    # Ensuring if all required parameters are passed
    if ag["email"] is None:
        return make_response(jsonify({"message": "email is required"}), 400), False
    if ag["password"] is None:
        return make_response(jsonify({"message": "password is required"}), 400), False
    if ag["name"] is None:
        return make_response(jsonify({"message": "name is required"}), 400), False
    if ag["age"] is None:
        return make_response(jsonify({"message": "age is required"}), 400), False
    if ag["backup"] is None:
        return make_response(jsonify({"message": "backup code required"}), 400), False
    if ag["gender"] is None:
        return make_response(jsonify({"message": "gender required"}), 400), False

    # For validating passed parameters
    if validate_email(ag["email"]):
        if len(ag["password"].strip()) >= 8:
            if (not ag["name"].isdigit()) and (len(ag["name"].strip()) > 2):
                try:
                    age = int(float(ag["age"]))
                    if age < 1:
                        raise ValueError
                except :
                    return make_response(jsonify({"message": "Age should be Positive Number only"}), 400), False

                if ag["gender"].strip().upper() in ['F', 'M']:
                    if len(ag["backup"].strip()) >= 4:
                        return None, True

                    else:
                        return make_response(jsonify({"message": "Backup code should be at least 4 characters long"}),
                                             400), False
                else:
                    return make_response(jsonify({"message": "Invalid gender, choose 'F' or 'M'"}), 400), False
            else:
                return make_response(jsonify({"message": "Invalid Name"}), 400), False
        else:
            return make_response(jsonify({"message": "Password should be at least 8 characters long"}), 400), False
    else:
        return make_response(jsonify({"message": "Invalid Email"}), 400), False


def validate_tracker_data(ag):
    if ag["tracker_name"] is None:
        return make_response(jsonify({"message": "tracker_name is required"}), 400), False
    if ag["description"] is None:
        return make_response(jsonify({"message": "description is required"}), 400), False
    if ag["tracker_type"] is None:
        return make_response(jsonify({"message": "tracker_type is required"}), 400), False
    if ag["setting"] is None:
        return make_response(jsonify({"message": "setting is required"}), 400), False
    if ag["user_id"] is None:
        return make_response(jsonify({"message": "user_id required"}), 400), False
    if ag["last_time"] is None:
        return make_response(jsonify({"message": "last_time required"}), 400), False

    # Validating Tracker name and User ID
    if ag["tracker_name"].strip() != '':
        try:
            int(ag["user_id"])
        except TypeError:
            return make_response(jsonify({"message": "Invalid user_id"}), 400), False
    else:
        return make_response(jsonify({"message": "tracker_name cannot be empty"}), 400), False

    # Validating TrackerType
    if not ag["tracker_type"] in ['Numerical', 'Multiple Choice', 'Boolean', 'Time Duration']:
        return make_response(jsonify({"message": "Choose Numerical or Multiple Choice or Boolean or Time Duration"}),
                             400), False

    # Validating Last Time
    if ag["last_time"].strip() == '':
        return make_response(jsonify({"message": "last_time cannot be empty"}), 400), False

    return None, True


def validate_log_data(ag):
    if ag["time"] is None:
        return make_response(jsonify({"message": "time is required"}), 400), False
    if ag["value"] is None:
        return make_response(jsonify({"message": "value is required"}), 400), False
    if ag["note"] is None:
        return make_response(jsonify({"message": "note is required"}), 400), False
    if ag["tracker_id"] is None:
        return make_response(jsonify({"message": "setting is required"}), 400), False

    if ag["time"].strip() == "":
        return make_response(jsonify({"message": "time cannot be empty"}), 400), False

    if ag["value"].strip() == "":
        return make_response(jsonify({"message": "value cannot be empty"}), 400), False

    # if not ag["value"].isalnum():
    #     return make_response(jsonify({"message": "value should be alphanumeric"}), 400), False

    return None, True


# def get_trackers_csv(user):
#     dt = []
#     for i in range(len(user.trackers)):
#         d = dict()
#         d["tracker_name"] = user.trackers[i].tracker_name
#         d["description"] = user.trackers[i].description
#         d["tracker_type"] = user.trackers[i].tracker_type
#         d["setting"] = user.trackers[i].setting
#         d["last_time"] = user.trackers[i].last_time
#         dt.append(d)
#
#     with open('../application/static/test4.csv', 'w') as csvfile:
#         file_writer = csv.DictWriter(csvfile, fieldnames=TRACKER_INFO)
#         file_writer.writeheader()
#         file_writer.writerows(dt)
#
#     df = pd.read_csv("../application/static/test4.csv")
#     correct_df = df.copy()
#     correct_df.rename(columns=TRACKER_HEADERS, inplace=True)
#     correct_df.to_csv('./application/static/export.csv', index=False, header=True)
#
#
# def get_logs_csv(tracker):
#     dt = list()
#
#     for i in range(len(tracker.logs)):
#         d = dict()
#         d["time"] = tracker.logs[i].time
#         d["value"] = tracker.logs[i].value
#         d["note"] = tracker.logs[i].note
#         dt.append(d)
#
#     with open('../application/static/test4.csv', 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=LOG_INFO)
#         writer.writeheader()
#         writer.writerows(dt)
#
#     df = pd.read_csv("../application/static/test4.csv")
#     correct_df = df.copy()
#     correct_df.rename(columns=LOG_HEADER, inplace=True)
#     correct_df.to_csv('./application/static/export.csv', index=False, header=True)


def create_charts(user, pdf=False):
    i = 1
    for tracker in user.trackers:
        data = {}
        if tracker.tracker_type in ["Numerical", "Time Duration"]:
            if tracker.tracker_type == "Numerical":
                for log in tracker.logs[-30:]:
                    date_day = log.time[5:10]
                    data[date_day] = data.get(date_day, 0) + int(log.value)
            else:
                for log in tracker.logs[-30:]:
                    date_day = log.time[5:10]
                    data[date_day] = data.get(date_day, 0) + int(log.value.split(":")[0])*60 + \
                                     int(log.value.split(":")[1])

            if data != {}:
                labels = list(data.keys())
                values = list(data.values())
                extreme = [labels[0], labels[-1]]
                meanvalue= [values[0], sum(values)/len(labels)]
                # Creating Line Graph
                if not pdf:
                    plt.figure(figsize=(11, 4))
                else:
                    plt.figure(figsize=(6, 4))
                plt.clf()
                # Plotting
                plt.plot(labels, values)
                plt.plot(extreme, meanvalue, "r--", label="Trend Line")
                # Configuring Graph
                plt.legend(frameon=True, loc='upper right')
                plt.scatter(labels, values, c="blue")
                # X axis
                plt.xlabel("Dates")
                plt.xticks(rotation=45)
                # Y axis
                plt.ylim(min(values) - 10, max(values) + 10)
                plt.ylabel("Values")
                # Save Figure
                plt.savefig(f"./application/static/charts/{i}a_chart.jpg")

                plt.clf()

                # Create Bar Chart
                plt.bar(labels, values, width=0.4, color="seagreen")
                plt.plot(labels, values, linestyle="--", c="red")
                # X axis
                plt.xlabel("Dates")
                plt.xticks(rotation=45)
                # Y axis
                plt.ylim(min(values) - 10, max(values) + 10)
                plt.ylabel("Value")
                # Saving Figure
                plt.savefig(f"./application/static/charts/{i}b_chart.jpg")
                plt.clf()
            else:
                plt.clf()
                plt.plot(0, 0)
                plt.savefig(f"./application/static/charts/{i}a_chart.jpg")
                plt.clf()
                plt.bar(0, 0)
                plt.savefig(f"./application/static/charts/{i}b_chart.jpg")
                plt.clf()

        elif tracker.tracker_type in ["Multiple Choice", "Boolean"]:
            data = {}
            for opt in tracker.setting.split("-"):
                data[opt] = 0

            for log in tracker.logs[-30:]:
                data[log.value] += 1

            labels = list(data.keys())
            values = list(data.values())

            # Creating Bar Chart
            plt.clf()
            if not pdf:
                plt.figure(figsize=(7, 4))
            else:
                plt.figure(figsize=(6, 4))
            plt.bar(labels, values, width=0.5, color="seagreen")
            plt.ylim(0, max(values) + 5)
            plt.savefig(f"./application/static/charts/{i}a_chart.jpg")
            plt.clf()

            # Creating Pie Chart
            plt.clf()
            if not pdf:
                plt.figure(figsize=(3, 4))
            else:
                plt.figure(figsize=(4, 4))
            plt.pie(values)
            circle = plt.Circle((0, 0), 0.7, color='white')
            p = plt.gcf()
            p.gca().add_artist(circle)
            plt.legend(labels, bbox_to_anchor=[0.75, 0.80])
            plt.savefig(f"./application/static/charts/{i}b_chart.jpg")
            plt.clf()

        # Incrementing the Count
        i += 1

    return None


def format_report(template_file, url, user):
    with open(template_file, "r") as f:
        template = Template(f.read())
        return template.render(link=url, trackers=user.trackers)


def create_pdf_report(url, user):
    message = format_report("./application/templates/report_template2.html", url, user)
    html = HTML(string=message)
    file_name = "Monthly Report" + ".pdf"
    html.write_pdf(target=f"./application/static/{file_name}")


def send_email(user):
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = user.email
    msg["Subject"] = "Monthly Report"
    body = MIMEText(f"Dear {user.name},\n Your last month report from quantified self app", "plain")
    msg.attach(body)
    filename = "Monthly Report.pdf"
    with open(f"./application/static/{filename}", "rb") as f:
        attachment = MIMEApplication(f.read(), Name=basename(filename))
        attachment["Content-Disposition"] = 'attachment; filename="{}"'.format(basename(filename))

    msg.attach(attachment)

    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.send_message(
            msg=msg,
            from_addr=EMAIL,
            to_addrs=[user.email],
        )
