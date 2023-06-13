from main import celery
import datetime as dt
import application
from os.path import basename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from application.models import *
from jinja2 import Environment, PackageLoader
from application.additional_variables import EMAIL, PASSWORD
from application.additional_functions import create_charts, create_pdf_report, send_email
from celery.schedules import crontab
# print("crontab ", crontab)


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=11, minute=26), daily_alert.s(), name='Daily Alert')
    sender.add_periodic_task(crontab(hour=23, minute=30, day_of_month=1), monthly_reports.s(), name="Monthly Reports")
    # sender.add_periodic_task(10.0, monthly_report.s(), name="Monthly Reports")


@celery.task()
def monthly_reports():
    folder = os.path.dirname(os.path.abspath(__file__))
    url = 'file://' + os.path.join(folder, 'static', 'charts')
    users = Users.query.all()
    # Creating charts for the trackers
    for user in users:
        create_charts(user, pdf=True)

        create_pdf_report(url, user)

        send_email(user)

    return "Monthly Report For Users Are Sent Successfully"


@celery.task()
def monthly_report():
    file_loader = PackageLoader("application", "templates")
    env = Environment(loader=file_loader)
    # Extracting user
    users = Users.query.all()
    # Creating charts for the trackers

    for user in users:
        create_charts(user)
        # Creating Monthly Report in Html
        rendered = env.get_template("report_template.html").render(trackers=user.trackers)
        filename = "report.html"
        with open(f"./application/static/{filename}", "w") as f:
            f.write(rendered)

        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = user.email
        msg["Subject"] = "Monthly Report"
        body = MIMEText("Inside Body, Testing", "plain")
        msg.attach(body)
        with open(f"./application/static/{filename}", "r") as f:
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

    return "Monthly Report Send"


@celery.task()
def daily_alert():
    users = Users.query.all()
    date_day = dt.datetime.today().day

    for user in users:
        missed_trackers = []

        for tracker in user.trackers:
            if not int(tracker.logs[-1].time[8:10]) == date_day:
                missed_trackers.append(str(tracker.tracker_name))

        if len(missed_trackers) == 1:
            message = f"Daily Reminder!, \nPlease log in the following tracker:\n" + missed_trackers[0]
        elif len(missed_trackers) > 1:
            s = ""
            for tracker in missed_trackers:
                s += tracker + "\n"
            message = f"Daily Reminder!, \nPlease log in the following trackers:\n" + s

        if len(missed_trackers) > 0:
            # Sending Daily Alert using Mail
            with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=PASSWORD)
                connection.sendmail(
                    from_addr=EMAIL,
                    to_addrs=user.email,
                    msg=f"Subject:Daily Reminder!\n\n{message}"
                )

    return "Sending Alert"
