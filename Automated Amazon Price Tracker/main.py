from bs4 import BeautifulSoup
import requests
import smtplib

URL = "https://www.amazon.com/Samsung-Factory-Unlocked-Smartphone-Pro-Grade/dp/B08FYV84JT/?_encoding=UTF8&pf_rd_p=a6eed03c-49da-47d6-ac11-598532cc753a&pd_rd_wg=VFq6D&pf_rd_r=TMYM4623DRNEHN15708Y&pd_rd_w=Ei1aq&pd_rd_r=c6d2df58-7560-4d07-83ae-1e7ede5bafda&ref_=pd_gw_exports_top_sellers_unrec&th=1"
RECEIVER_MAIl = "mohdikram888@yahoo.com"
SENDER_MAIL = "game388019@gmail.com"
SENDER_PASSWORD = "GoZameer88@$"

headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

response = requests.get(url=URL, headers=headers)
contents = response.text
# print(contents)

soup = BeautifulSoup(contents, "html.parser")
# print(soup.prettify())

price = soup.find(name="span", class_="a-offscreen")
price_float = float(price.getText()[1:])
print(price_float)

if price_float < 600:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=SENDER_MAIL, password=SENDER_PASSWORD)
        connection.sendmail(
            from_addr=SENDER_MAIL,
            to_addrs=RECEIVER_MAIl,
            msg=f"Subject:OFFER!\n\nThe SAMSUNG Galaxy S20 FE 5G Factory Unlocked Android Cell Phone 128GB US is avaliable under your budget."
                f"The price is just ${price_float}"
        )

