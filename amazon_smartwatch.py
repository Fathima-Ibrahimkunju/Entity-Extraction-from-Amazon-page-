
# Importing libraries

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import csv

# Defining functions to scrape the features of products

def get_title(soup):
    
    try:
        title = soup.find('span',attrs={'id':'productTitle'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ''
    return title_string

def get_price(soup):
    try:
        price = soup.find('span',attrs={'class':'a-price-whole'})
        price_value = price.text
        price_str = price_value.strip()
    except AttributeError:
        price_str =''
    return price_str


def get_rating(soup):
    
    try:
        rat = soup.find('i',attrs={'class':'a-icon-alt'})
        rat_value = rat.text
        rat_string = rat_value.strip()
    except AttributeError:
        rat_string = ''
    return rat_string



def get_nrating(soup):
    
    try:
        ratn = soup.find('span',attrs={'id':'acrCustomerReviewText'})
        ratn_value = ratn.text
        ratn_strin = ratn_value.split()
        ratn_string = ratn_strin[0]
    except AttributeError:
        ratn_string = ''
    return ratn_string



def get_brand(soup):
    try:
        brand = soup.find('tr',attrs = {'class':'a-spacing-small po-brand'})
        brand_value = brand.text
        brand_real = brand_value.replace('Brand   ','')
        brand_str = brand_value.strip()
    except AttributeError:
        brand_str = ''
    return brand_str


def get_model(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-model_name'})
        model_value = model.text
        model_real = model_value.replace('Model Name   ','')
        model_str = model_real.strip()
    except AttributeError:
        model_str = ''
    return model_str


def get_style(soup):
    try:
        model = soup.find_all('tr',attrs = {'class':'a-spacing-small po-style'})
        style_value = model.text
        style_real = style_value.replace('Style   ','')
        style_str = style_value.strip()
    except AttributeError:
        style_str = ''
    return style_str


def get_colour(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-color'})
        colour_value = model.text
        colour_real = colour_value.replace('Colour   ','')
        colour_str = colour_real.strip()
    except AttributeError:
        colour_str = ''
    return colour_str



def get_screen(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-display.size'})
        screen_value = model.text
        screen_real = screen_value.replace('Screen Size   ','')
        screen_str = screen_real.strip()
    except AttributeError:
        screen_str = ''
    return screen_str

# Defining the number of pages
pages = []
for i in range (1,21):
  pages.append(i)

# Getting the product links

Headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'Accept-Language':'en-US, en;q=0.5'})
d = {'title':[], 'price':[], 'rating':[], 'no_of_rating':[], 'brand':[], 'model':[], 'style':[], 'screen':[], 'colour':[], 'Product_URL':[]}
urls = []
links_list = []
for r in pages:
  url = 'https://www.amazon.in/s?k=smart+watch&page='+str(r)
  urls.append(url)
for i in urls:
  req = requests.get(i, headers = Headers)
  soup = BeautifulSoup(req.content, 'html.parser')
  links = soup.find_all('a', attrs = {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        
  for link in links:
    links_list.append(link.get('href'))

# Scraping the features of the products and creating a dictionary from it

for link in links_list:
  new_web = requests.get('https://www.amazon.in'+link, headers=Headers)
  new_soup = BeautifulSoup(new_web.content, 'html.parser')
         
  d['title'].append(get_title(new_soup))
  d['price'].append(get_price(new_soup))
  d['rating'].append(get_rating(new_soup))
  d['no_of_rating'].append(get_nrating(new_soup))
  d['brand'].append(get_brand(new_soup))
  d['model'].append(get_model(new_soup))
  d['style'].append(get_style(new_soup))
  d['colour'].append(get_colour(new_soup))
  d['screen'].append(get_screen(new_soup))
  d['Product_URL'].append('https://www.amazon.in'+link)

# Creating dataframe
df = pd.DataFrame.from_dict(d)

#Dataframe
df

