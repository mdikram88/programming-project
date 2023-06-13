import requests
from bs4 import BeautifulSoup
# import lxml
#  lxml can be an alternative parser for html, because in some website may html parser may not work

# bs4 is a module for Beautiful Soup module, I have no idea why they name it bs4

# ------------------------------------------LEARNING--------------------------------- #
# with open("website.html", encoding="utf8") as file:
#     contents = file.read()
#     # print(contents)
#
# soup = BeautifulSoup(contents, "html.parser")
# all_anchors_tags = soup.find_all(name="a")


# for tag in all_anchors_tags:
#     print(tag.getText())
#     print(tag.get("href"))
#
# heading = soup.find(name="h1", id="name")
# print(heading)
#
# h3_heading = soup.find_all(name="h3", class_="heading")
# print(h3_heading)
#
# company_url = soup.select_one(selector="p a")
# print(company_url)
#
# name = soup.select_one(selector="#name")
# print(name)
#
# headings = soup.select(selector=".heading")
# print(headings)
#

# -----------------------------------------WEB SCRAPPER CODE--------------------------- #

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html,"html.parser")

all_movies = soup.find_all(name="h3", class_="title")
movies_name = [movie.getText() for movie in all_movies]
print(movies_name[::-1])
with open("movies.txt", "w") as file:
    for movie in movies_name[::-1]:
        file.write(f"{movie}\n")
