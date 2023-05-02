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
        title_string = ''
    return title_string


def get_price(soup):
    try:
        price = soup.find('span', attrs={'class': 'a-price-whole'})
        price_value = price.text
        price_str = price_value.strip()
    except AttributeError:
        price_str = ''
    return price_str


def get_rating(soup):
    try:
        rating = soup.find('span', attrs={'class': 'a-icon-alt'})
        rating_value = rating.text
        rating_str = rating_value.strip()
    except AttributeError:
        rating_str = ''
    return rating_str


def get_nrating(soup):
    try:
        nrating = soup.find('span', attrs={'id': 'acrCustomerReviewText'})
        nrating_value = nrating.text
        nrating_str = nrating_value.strip()
    except AttributeError:
        nrating_str = ''
    return nrating_str


def get_brand(soup):
    try:
        brand = soup.find('tr', attrs={'class': 'a-spacing-small po-brand'})
        brand_value = brand.text
        brand_real = brand_value.replace('Brand   ', '')
        brand_str = brand_value.strip()
    except AttributeError:
        brand_str = ''
    return brand_str


def get_model(soup):
    try:
        model = soup.find('tr', attrs={'class': 'a-spacing-small po-model_name'})
        model_value = model.text
        model_real = model_value.replace('Model Name   ', '')
        model_str = model_real.strip()
    except AttributeError:
        model_str = ''
    return model_str


def get_use(soup):
    try:
        model = soup.find('tr', attrs={'class': 'a-spacing-small po-recommended_uses_for_product'})
        use_value = model.text
        use_real = use_value.replace('Recommended Uses For Product   ', '')
        use_str = use_real.strip()
    except AttributeError:
        use_str = ''
    return use_str


def get_connectivity(soup):
    try:
        model = soup.find('tr', attrs={'class': 'a-spacing-small po-connectivity_technology'})
        connectivity_value = model.text
        connectivity_real = connectivity_value.replace('Connectivity Technology   ', '')
        connectivity_str = connectivity_real.strip()
    except AttributeError:
        connectivity_str = ''
    return connectivity_str


def get_sf(soup):
    try:
        model = soup.find('tr', attrs={'class': 'a-spacing-small po-special_feature'})
        sf_value = model.text
        sf_real = sf_value.replace('Special Feature   ', '')

        sf_str = sf_real.strip()
    except AttributeError:
        sf_str = ''
    return sf_str


def get_usage(soup):
    try:
        model = soup.find('tr', attrs={'class': 'a-spacing-small po-indoor_outdoor_usage'})
        usage_value = model.text
        usage_real = usage_value.replace('Indoor/Outdoor Usage   ', '')
        usage_str = usage_real.strip()
    except AttributeError:
        usage_str = ''
    return usage_str


def get_cd(soup):
    try:
        model = soup.find('tr', attrs={'class': 'a-spacing-small po-compatible_devices'})
        cd_value = model.text
        cd_real = cd_value.replace('Compatible Devices   ', '')
        cd_str = cd_real.strip()
    except AttributeError:
        cd_str = ''
    return cd_str


def get_ps(soup):
    try:
        model = soup.find('tr', attrs={'class': 'a-spacing-small po-power_source_type'})
        ps_value = model.text
        ps_real = ps_value.replace('Power Source   ', '')
        ps_str = ps_real.strip()
    except AttributeError:
        ps_str = ''
    return ps_str


def get_protocol(soup):
    try:
        model = soup.find('tr', attrs={'class': 'a-spacing-small po-connectivity_protocol'})
        protocol_value = model.text
        protocol_real = protocol_value.replace('Connectivity Protocol   ', '')
        protocol_str = protocol_real.strip()
    except AttributeError:
        protocol_str = ''
    return protocol_str


def get_ct(soup):
    try:
        model = soup.find('tr', attrs={'class': 'a-spacing-small po-controller_type'})
        ct_value = model.text
        ct_real = ct_value.replace('Controller Type   ', '')
        ct_str = ct_real.strip()
    except AttributeError:
        ct_str = ''
    return ct_str


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
    url = 'https://www.amazon.in/s?k=cctv+camera&page=' + str(r)
    urls.append(url)
for i in urls:
    req = requests.get(i, headers=Headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    links = soup.find_all('a', attrs={
        'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    for link in links:
        links_list.append(link.get('href'))

# Scraping the features of the products and creating a dictionary from it

d = {'Name': [], 'Price': [], 'Rating': [], 'No_of_rating': [], 'Brand': [], 'Model': [], 'Recommended Uses For Product': [],
     'Connectivity Technology': [], 'Special Feature': [], 'Indoor/Outdoor Usage': [], 'Compatible Devices': [], 'Power Source': [], 'Connectivity Protocol': [], 'Controller Type': [],
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
    d['Recommended Uses For Product'].append(get_use(new_soup))
    d['Connectivity Technology'].append(get_connectivity(new_soup))
    d['Special Feature'].append(get_sf(new_soup))
    d['Indoor/Outdoor Usage'].append(get_usage(new_soup))
    d['Compatible Devices'].append(get_cd(new_soup))
    d['Power Source'].append(get_ps(new_soup))
    d['Connectivity Protocol'].append(get_protocol(new_soup))
    d['Controller Type'].append(get_ct(new_soup))
    d['Product_URL'].append('https://www.amazon.in' + link)

# Creating dataframe
df = pd.DataFrame.from_dict(d)

# Dataframe
df

# Converting dataframe into csv format

df.to_csv('cctv.csv')


# Converting to json format

json = df.to_json('cctv.json')