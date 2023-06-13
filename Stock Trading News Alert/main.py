import requests
import datetime as dt
from twilio.rest import Client

UP_ARROW = "🔺"
DOWN_ARROW = "🔻"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# -----------------------------PRE-SETUP--------------------------- #

flag = True
STOCK_API_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "FLHAIQLOEH0UTY3O"

NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "e8275b748a6f40709fc79f32d8e63dd9"

TWILIO_ACCOUNT_SID = "AC6fd8fb0b2ed2660e2ccc6d27b8b3afdf"
TWILIO_AUTH_TOKEN = "ec092433772d10b7fd3248f0043f600c"

# Getting Dates
yesterday = dt.datetime.today().date() - dt.timedelta(days=1)
day_before_yesterday = dt.datetime.today().date() - dt.timedelta(days=2)

# kinda like login
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# STEP 1: Use https://www.alphavantage.co

stock_api_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
# Asking for data
response = requests.get(STOCK_API_ENDPOINT, params=stock_api_params)

# Checking if stock market has info of yesterday and day before yesterday
try:
    yesterday_close = float(response.json()["Time Series (Daily)"][str(yesterday)]["4. close"])
    day_before_yesterday_close = float(response.json()["Time Series (Daily)"][str(day_before_yesterday)]["4. close"])
except KeyError:
    flag = False

# If trade info is fetched then proceed
if flag:
    # Finding the percentage in difference of stock price between closing price of 2 days
    percent = round(((day_before_yesterday_close-yesterday_close)/day_before_yesterday_close) * 100, 0)
    # When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
    if abs(percent) >= 5:
        if percent < 0:
            arrow = DOWN_ARROW
        elif percent >= 0:
            arrow = UP_ARROW


        # STEP 2: Use https://newsapi.org

        news_api_params = {
            "q": COMPANY_NAME,
            "from": str(day_before_yesterday),
            "sortBy": "publishedAt",
            "apiKey": NEWS_API_KEY
        }

        # Requesting news data from api
        response = requests.get(NEWS_API_ENDPOINT, params=news_api_params)
        top_3_articles = response.json()["articles"][:3]
        for article in top_3_articles:
            # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
            # STEP 3: Use https://www.twilio.com
            # Send a seperate message with the percentage change and each article's title and description to your phone number.
            message = client.messages.create(
                body=f"{STOCK}: {arrow}{abs(percent)}%\nHeadline: {article['title']}\nBrief: {article['description']}",
                from_="+17174834697",
                to="+918738801988"
            )
            print(message.status)


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

