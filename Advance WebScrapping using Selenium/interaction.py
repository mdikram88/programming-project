from selenium import webdriver
from selenium.webdriver.common.keys import Keys


chrome_driver_path = "D:/software/chromedriver"

driver = webdriver.Chrome(executable_path=chrome_driver_path)

# ----------------------------Scrapping Wikipedia-----------------------

# driver.get("https://en.wikipedia.org/wiki/Main_Page")

# article_count = driver.find_element_by_css_selector("#articlecount a")
# print(article_count.text)

# to click on an element in selenium
# article_count.click()


# to click on an element by link name
# all_portals = driver.find_element_by_link_text("Talk")
# all_portals.click()


# To enter input in the website using selenium and send it
# search = driver.find_element_by_name("search")
# search.send_keys("Python")
# search.send_keys(Keys.ENTER)
# driver.quit()

# ----------------------------Filling a form--------------------------#

driver.get("http://secure-retreat-92358.herokuapp.com/")

fname = driver.find_element_by_name("fName")
fname.send_keys("Mohd")

lname = driver.find_element_by_name("lName")
lname.send_keys("Ikram")


email = driver.find_element_by_name("email")
email.send_keys("game388019@gmail.com")

# btn = driver.find_element_by_class_name("btn")
btn = driver.find_element_by_tag_name("button")
btn.send_keys(Keys.ENTER)

driver.quit()
