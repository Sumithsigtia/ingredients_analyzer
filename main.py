import requests
from bs4 import BeautifulSoup
import streamlit as st

def extract_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = None

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

    # Extract product title
    try:
        title = soup.find("span", {"class": "VU-ZEz"}).text.strip()
    except (AttributeError, TypeError):
        title = None

    # Extract price
    try:
        price = soup.find("div", {"class": "Nx9bqj CxhGGd"}).text.strip()
    except (AttributeError, TypeError):
        price = None

    # Extract image URL
    try:
        image_div = soup.find("div", {"class": "z1kiw8"})
        image_url = image_div.find("img")["src"] if image_div else None
    except (AttributeError, TypeError):
        image_url = None

    # Extract Ingredients
    try:
        description = soup.find("td", string="Ingredients").find_next_sibling("td").text.strip()
        ingredients_website = [ingredient.strip() for ingredient in description.split(",")]
    except (AttributeError, TypeError):
        ingredients_website = []

    return title, price, image_url, ingredients_website

st.title("Flipkart Product Analyzer")

url = st.text_input("Enter the Flipkart product URL:")

if st.button("Show All Details"):
    if url:
        title, price, image_url, ingredients_website = extract_product_info(url)

        if title and price and image_url:
            st.subheader(title)
            st.write(f"Price: {price}")
            st.image(image_url)
        else:
            st.write("Unable to extract product information. Please check the URL and try again.")

    # Clear previous content
    st.empty()
