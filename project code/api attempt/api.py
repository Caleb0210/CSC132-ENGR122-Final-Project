import requests
from bs4 import BeautifulSoup

# Replace the following variables with your Amazon account credentials
email = "calebcameron0210@gmail.com"
password = "Chigga^0210"

# Replace the following variables with the URL of the product you want to add to your cart
product_url = "https://www.amazon.com/dp/B06WLHN29W"
session_url = "https://www.amazon.com/gp/sign-in.html"

# Create a session to log in to Amazon
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})
session.get(session_url)

# Log in to Amazon
response = session.post(
    "https://www.amazon.com/ap/signin",
    data={
        "email": email,
        "password": password,
    },
    headers={"Referer": session_url},
)

# Get the product page and add the product to the cart
response = session.get(product_url)
soup = BeautifulSoup(response.content, "html.parser")
add_to_cart_url = soup.find("input", {"id": "add-to-cart-button"})["data-action"]
session.post(add_to_cart_url)

# Check if the product was successfully added to the cart
response = session.get("https://www.amazon.com/gp/cart/view.html")
soup = BeautifulSoup(response.content, "html.parser")
product_title = soup.find("span", {"class": "a-size-medium a-text-bold"}).text.strip()
print(f"Product '{product_title}' was successfully added to the cart.")