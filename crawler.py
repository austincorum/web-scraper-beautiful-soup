from numpy import product
import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd

baseurl = "https://drop.com"

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
    if "buy" in path:
        productLinks.append(baseurl + path)
    else:
        pass

for link in productLinks:
    k = requests.get(str(link)).text
    con = Soup(k, "html.parser")

    ### Write HTML into file for testing ###
    # file = open("test.txt", "w")
    # file.write(str(con))
    # file.close()

    try:
        title = (
            con.find(
                "div",
                {"class": "DropPageHeader__drop_name__32Nat"},
            )
            .find("h1", {"class": "Text__type--title-0__2XDay"})
            .text.strip()
        )
        print(title)
    except:
        title = None

    product = {"title": title}
    productData.append(product)

df = pd.DataFrame(productData)
print(df)
