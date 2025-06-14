import requests
import lxml
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

TARGET_PRICE = float(100)
SOURCE_EMAIL = os.getenv("SOURCE_EMAIL")
SOURCE_EMAIL_PW = os.getenv("SOURCE_EMAIL_PW")
to_email = os.getenv("TO_EMAIL")

header = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0"
}
source_url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
amazon_response = requests.get(url=source_url, headers=header)
item_data = amazon_response.text

soup = BeautifulSoup(item_data, "lxml")

item_price = float(soup.select_one(selector=".aok-offscreen").getText().strip().split("$")[1].split()[0])

if item_price < TARGET_PRICE:
    with smtplib.SMTP("smtp-mail.outlook.com") as connection:
        connection.starttls()
        connection.login(user=SOURCE_EMAIL, password=SOURCE_EMAIL_PW)
        connection.sendmail(from_addr=SOURCE_EMAIL,
                            to_addrs=to_email,
                            msg=f"Subject: Item Price Drop\n\nInstant Pot Duo Evo 9 in 1 is now ${item_price}. "
                                f"This is below the price you had set as your target price.\n\n{source_url}")
        print("Email Sent")

