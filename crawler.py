from numpy import product
import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd

baseurl = "https://drop.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}

productLinks = []
count = 0
productData = []

# hardcoded url for v1
r = requests.get("https://drop.com/all-communities/drops").text
soup = Soup(r, "html.parser")

# add all product items into a list
productList = soup.find_all(
    "div",
    {"class": "Grid__gridItem__2qOsq"},
)

# find all product links
for product in productList:
    path = product.find(
        "a",
        {"class": "Link2__link__1aAsF"},
    ).get("href")

    # error checking - preventing product link from containing '//'
    if path[0] == "/" and baseurl[-1] == "/":
        path = path[1:]
    else:
        pass
    productLinks.append(baseurl + path)

for link in productLinks:
    k = requests.get(link, headers=headers).link
    con = Soup(r, "html.parser")

    try:
        price = con.find