# Importing the necessary libraries
import random
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
user_agents = user_agent=['Insert your 1 browser user agent','Insert your 2 browser user agent','...']
# Defining the headers for HTTP requests
HEADERS = {
    'User-Agent': random.choice(user_agents),
    'Accept-Language': 'en-US, en;q=0.5'
}

# Sending an HTTP request to the Amazon webpage
URL = "https://www.amazon.in/s?k=3d+printer+filaments"
webpage = requests.get(URL, headers=HEADERS)

# Creating a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(webpage.content, "html.parser")

# Function to extract Product Title
def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("span", attrs={'data-hook':'rating-out-of-text','class':'a-size-medium a-color-base'}).text
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating

# Function to extract Material
def get_material(soup):
    try:
        material_label = soup.find("span", class_="a-size-base a-text-bold", string="Material")
        if material_label:
            material = material_label.find_next("span", class_="a-size-base po-break-word").text.strip()
        else:
            material = ""
    except AttributeError:
        material = ""

    return material

# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={'class':'a-price-whole'}).text

    except AttributeError:
        try:
            # If there is some deal price
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()
        except:
            price = ""

    return price

# Function to extract Brand Name
def get_brand_name(soup):
    try:
        brand = soup.find("span", attrs={'class':'a-size-base po-break-word'}).text

    except AttributeError:
        brand = ""
        
    return brand

# Function to extract Item Weight
def get_item_weight(soup):
    try:
        weight_label = soup.find("span", class_="a-size-base a-text-bold", string="Item weight")
        if weight_label:
            item_weight = weight_label.find_next("span", class_="a-size-base po-break-word").text.strip()
        else:
            item_weight = ""
    except AttributeError:
        item_weight = ""

    return item_weight

# Function to extract Color
def get_color(soup):
    try:
        color_label = soup.find("span", class_="a-size-base a-text-bold", string="Colour")
        if color_label:
            color = color_label.find_next("span", class_="a-size-base po-break-word").text.strip()
        else:
            color = ""
    except AttributeError:
        color = ""

    return color

#display
d = {"title": [], "brand":[], 
    "material": [], "review": [], 
    "price": [], "item weight":[], "color":[], "link":[]}

for i in range(1):
        
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

        # Store the links
    links_list = []

        # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    # Loop for extracting product details from each link 
    i= 1
    for link in links_list:
        # Adding a delay between each request
        print(i,len(links_list))
        delay = random.uniform(1, 3)
        time.sleep(delay)
        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d["review"].append(get_rating(new_soup))
        d["price"].append(get_price(new_soup))
        d["brand"].append(get_brand_name(new_soup))
        d["material"].append(get_material(new_soup))
        d["color"].append(get_color(new_soup))
        d["item weight"].append(get_item_weight(new_soup))
        d["link"].append(webpage)

        i +=1
    URL=soup.select_one('.s-pagination-item.s-pagination-next')['href']
    webpage = requests.get("https://www.amazon.in" + URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")


len(d)

df=pd.DataFrame(d)