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

# Function to extract Brand Name
def get_brand_name(soup):
    try:
        brand = soup.find("span", attrs={'class':'a-size-base po-break-word'}).text

    except AttributeError:
        brand = ""
        
    return brand
# Function to extract other details from website
def get_extract_details(soup):
    
    
    rows = soup.find_all('tr')
    details = {"screen_size": [], "battery_power": [], "ram": [], "storage": [],
     "operating_system": [], "item_weight": []}
    
    for row in rows:
        span_element = row.find('span', class_='a-size-base')
        
        if span_element and span_element.text == 'Screen Size':
            td_element = row.find('td')
            if td_element:
                details['screen_size'] = td_element.text.strip()
            else:
                details['screen_size'] =''
        
        if span_element and span_element.text == 'Battery Power (In mAH)':
            td_element = row.find('td')
            if td_element:
                details['battery_power'] = td_element.text.strip()
            else:
                details['battery_power'] =''
        
        if span_element and span_element.text == 'RAM':
            td_element = row.find('td')
            if td_element:
                details['ram'] = td_element.text.strip()
            else:
                details['ram'] =''
        
        if span_element and span_element.text == 'Inbuilt Storage (in GB)':
            td_element = row.find('td')
            if td_element:
                details['storage'] = td_element.text.strip()
            else:
                details['storage'] =''
        
        if span_element and span_element.text == 'Operating System':
            td_element = row.find('td')
            if td_element:
                details['operating_system'] = td_element.text.strip()
            else:
                details['operating_system'] =''
        
        if span_element and span_element.text == 'Item Weight':
            td_element = row.find('td')
            if td_element:
                details['item_weight'] = td_element.text.strip()
            else:
                details['item_weight'] =''
            
    
    return details

    
d = {"title": [], "price": [], "rating": [],"brand":[],
        "screen_size": [], "battery_power": [], "ram": [], "storage": [],
        "operating_system": [], "item_weight": []}

import time
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
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['brand'].append(get_brand_name(new_soup))
        details = get_extract_details(new_soup)

        # Append the values from the 'details' dictionary to the main dictionary 'd'
        for key, value in details.items():
            
            d[key].append(value)
            if value=='':
                print('null' ,key,'value',value)
        i +=1
    # Adding URL of the next page
    URL=soup.select_one('.s-pagination-item.s-pagination-next')['href']
    webpage = requests.get("https://www.amazon.in" + URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")


#for key, value in d.items():
#        print(len(d[key]),key)

len(d)


phone_data=pd.DataFrame(d)


#phone_data.to_csv('amazon_phones.csv')