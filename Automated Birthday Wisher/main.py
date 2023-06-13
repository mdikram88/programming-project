import smtplib
import datetime as dt
import pandas as pd
import random

EMAIL = "mohdikram888@yahoo.com"
PASSWORD = "ckooawptkphzdgcv"

# Getting Today's Date
date = dt.date.today()
day = date.day
month = date.month

# For selecting a random quote
# with open("quotes.txt") as file:
#     all_quotes = file.readlines()
#     quote = random.choice(all_quotes)
#     print(quote)

# Reading csv file of birthdays
data = pd.read_csv("birthdays.csv")

# iterating through records in birthday csv file
for (index, record) in data.iterrows():

    # Selecting a random birthday letter template
    random_letter = random.choice([f"letter_1.txt", "letter_2.txt", "letter_3.txt"])

    # Checking if today's date mathces with any of the birthday date in record
    if record.month == month and record.day == day:

        # Opening the selected random bithday letter template and customising it with name
        with open(f"./letters/{random_letter}") as file:
            letter = file.read()
        custom_letter = letter.replace("[name]", record["name"])

        # Sending birthday mail to the respective sender through email
        sender_email = record.email
        with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL,
                                to_addrs=sender_email,
                                msg=f"Subject:Happy Birthday!\n\n{custom_letter}")
