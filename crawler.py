import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd

baseurl = "https://drop.com"

productUrls = []
count = 0
productData = []

# hardcoded url
r = requests.get("https://drop.com/all-communities/drops").text

# BeautifulSoup HTML parser
soup = Soup(r, "html.parser")

# add all products into a list
productList = soup.find_all(
    "div",
    {"class": "Grid__gridItem__2qOsq"},
)

# extract all product links
for product in productList:
    path = product.find(
        "a",
        {"class": "Link2__link__1aAsF"},
    ).get("href")

    # error checking
    # + prevent '//' in product link
    # + product links all contain 'buy'
    if path[0] == "/" and baseurl[-1] == "/":
        path = path[1:]
    else:
        pass
    if "buy" in path:
        productUrls.append(baseurl + path)
    else:
        pass

# Extract all product data
for link in productUrls:
    k = requests.get(str(link)).text
    con = Soup(k, "html.parser")

    ### Write to HTML file for testing ###
    # file = open("test.txt", "w")
    # file.write(str(con))
    # file.close()

    # TITLE #
    try:
        title = (
            con.find(
                "div",
                {"class": "DropPageHeader__drop_name__32Nat"},
            )
            .find("h1", {"class": "Text__type--title-0__2XDay"})
            .text.strip()
        )
    except:
        title = None

    # PRICE #
    try:
        price = con.find(
            "div",
            {"class": "Text__type--price__1mumP"},
        ).text.strip()
    except:
        price = None

    # DESCRIPTION #
    try:
        description = con.find(
            "div",
            {"class": "SingleTextColumn__description_text__OHaPK"},
        ).text.strip()
    except:
        description = None

    product = {"title": title, "price": price, "description": description}
    productData.append(product)

# Add product data into DataFrame
df = pd.DataFrame(productData)
print(df)
