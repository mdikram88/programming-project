from selenium import webdriver

chrome_driver_path = "E:/100 days rebooted/chromedriver.exe"

driver = webdriver.Chrome(executable_path=chrome_driver_path)

# --------------------------------Scrapping Amazon.com---------------------------- #

# driver.get("https://www.amazon.com/Z-Edge-1920x1080-Backlight-Eye-Care-Technology/dp/B08H8JM216/ref=sr_1_1_sspa?crid=Z3C5D8Z4668G&keywords=monitor&qid=1650537077&s=pc&sprefix=monit%2Ccomputers%2C614&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyQktGRjJCNTIwMUdDJmVuY3J5cHRlZElkPUEwNTQ3MDY5MlVHTEdXWVYzSTY2NyZlbmNyeXB0ZWRBZElkPUEwNzMyMDUxM1FaOVRGRjI2UjdHRyZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=")

# price = driver.find_element_by_class_name("apexPriceToPay")
# price = driver.find_element_by_xpath('//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[2]')
# print(price.text)

# driver.close()  this closes a single tab
# driver.quit()   # this closes the entire browser


# ------------------------Scrapping python.org-------------------

driver.get("https://www.python.org/")

times = driver.find_elements_by_css_selector(".event-widget time")
names = driver.find_elements_by_css_selector(".event-widget li a")


event = {i: {"time": times[i].text, "name": names[i].text} for i in range(len(times))}
print(event)

driver.quit()