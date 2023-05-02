# Importing libraries

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import csv
import time


# Defining functions to scrape the features of products


def get_title(soup):
    try:
        title = soup.find('span', attrs={'id': 'productTitle'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = 'No information available'
    return title_string


def get_price(soup):
    try:
        price = soup.find('span', attrs={'class': 'a-price-whole'})
        price_value = price.text
        price_str = price_value.strip()
    except AttributeError:
        price_str = 'No information available'
    return price_str


def get_rating(soup):
    try:
        rating = soup.find('span', attrs={'class': 'a-icon-alt'})
        rating_value = rating.text
        rating_str = rating_value.strip()
    except AttributeError:
        rating_str = 'No information available'
    return rating_str


def get_nrating(soup):
    try:
        nrating = soup.find('span', attrs={'id': 'acrCustomerReviewText'})
        nrating_value = nrating.text
        nrating_str = nrating_value.strip()
    except AttributeError:
        nrating_str = 'No information available'
    return nrating_str


def get_brand(soup):
    try:
        brand = soup.find('tr', attrs={'class': 'a-spacing-small po-brand'})
        brand_value = brand.text
        brand_real = brand_value.replace('Brand   ', '')
        brand_str = brand_real.strip()
    except AttributeError:
        brand_str = 'No information available'
    return brand_str


def get_model(soup):
    try:
        model = soup.find('tr', attrs={'class': 'a-spacing-small po-model_name'})
        model_value = model.text
        model_real = model_value.replace('Model Name   ', '')
        model_str = model_real.strip()
    except AttributeError:
        model_str = 'No information available'
    return model_str


def get_speakertype(soup):
    try:
        model = soup.find('tr', attrs={'class': 'a-spacing-small po-speaker_type'})
        st_value = model.text
        st_real = st_value.replace('Network Service Provider   ', '')
        st_str = st_real.strip()
    except AttributeError:
        st_str = 'No information available'
    return st_str


def get_connector(soup):
    try:
        model = soup.find('tr', attrs={'class': 'a-spacing-small po-connectivity_technology'})
        connector_value = model.text
        connector_real = connector_value.replace('OS   ', '')
        connector_str = connector_real.strip()
    except AttributeError:
        connector_str = 'No information available'
    return connector_str


def get_sf(soup):
    try:
        model = soup.find('tr', attrs={'class': 'a-spacing-small po-special_feature'})
        sf_value = model.text
        sf_real = sf_value.replace('Cellular Technology   ', '')
        sf_str = sf_real.strip()
    except AttributeError:
        sf_str = 'No information available'
    return sf_str




# Defining the number of pages
pages = []
for i in range(1, 21):
    pages.append(i)

# Getting the product links


Headers = ({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'})


urls = []
links_list = []
for r in pages:
    url = 'https://www.amazon.in/s?k=bluetooth+speaker&page=' + str(r)
    urls.append(url)
for i in urls:
    req = requests.get(i, headers=Headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    links = soup.find_all('a', attrs={
        'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    for link in links:
        links_list.append(link.get('href'))

# Scraping the features of the products and creating a dictionary from it

d = {'Name': [], 'Price': [], 'Rating': [], 'No_of_rating': [], 'Brand': [], 'Model': [], 'Speaker Type': [],
     'Connector Type': [], 'Special Feature': [],
     'Product_URL': []}

for link in links_list:
    new_web = requests.get('https://www.amazon.in' + str(link), headers=Headers)
    new_soup = BeautifulSoup(new_web.content, 'html.parser')

    d['Name'].append(get_title(new_soup))
    d['Price'].append(get_price(new_soup))
    d['Rating'].append(get_rating(new_soup))
    d['No_of_rating'].append(get_nrating(new_soup))
    d['Brand'].append(get_brand(new_soup))
    d['Model'].append(get_model(new_soup))
    d['Speaker Type'].append(get_speakertype(new_soup))
    d['Connector Type'].append(get_connector(new_soup))
    d['Special Feature'].append(get_sf(new_soup))
    d['Product_URL'].append('https://www.amazon.in' + link)

# Creating dataframe
df = pd.DataFrame.from_dict(d)

# Dataframe
df

# Converting dataframe into csv format

df.to_csv('speaker.csv')


# Converting to json format

json = df.to_json('speaker.json')