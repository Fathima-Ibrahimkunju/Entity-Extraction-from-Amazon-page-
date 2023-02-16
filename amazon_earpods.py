
# Importing libraries

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import csv

# Defining the number of pages
pages = []
for i in range (1,21):
  pages.append(i)

# User defined functions

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
    price_str = 'Information not available'
  return price_str


def get_rating(soup):
  try:
    rat = soup.find('span', attrs={'class': 'a-icon-alt'})
    rat_value = rat.text
    rat_string = rat_value.strip()
  except AttributeError:
    rat_string = 'Information not available'
  return rat_string


def get_nrating(soup):
  try:
    ratn = soup.find('span', attrs={'id': 'acrCustomerReviewText'})
    ratn_value = ratn.text
    ratn_strin = ratn_value.split()
    ratn_string = ratn_strin[0]
  except AttributeError:
    ratn_string = 'Information not available'
  return ratn_string



def get_brand(soup):

  try:
      brand = soup.find('tr',attrs = {'class':'a-spacing-small po-brand'})
      brand_value = brand.text
      brand_real = brand_value.replace('Brand   ','')
      brand_str = brand_real.strip()
  except AttributeError:
      brand_str = 'Information not available'
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


def get_colour(soup):
  try:
    model = soup.find('tr', attrs={'class': 'a-spacing-small po-color'})
    colour_value = model.text
    colour_real = colour_value.replace('Colour   ', '')
    colour_str = colour_real.strip()
  except AttributeError:
    colour_str = 'Information not available'
  return colour_str


def get_formfactor(soup):
  try:
    model = soup.find('tr', attrs={'class': 'a-spacing-small po-headphones_form_factor'})
    form_value = model.text
    form_real = form_value.replace('Headphones Form Factor   ', '')
    form_str = form_real.strip()
  except AttributeError:
    form_str = 'Information not available'
  return form_str


def get_connector(soup):
  try:
    connector = soup.find('tr', attrs={'class': 'a-spacing-small po-connectivity_technology'})
    conn_value = connector.text
    conn_real = conn_value.replace('Connector Type   ', '')
    conn_str = conn_real.strip()
  except AttributeError:
    conn_str = 'Information not available'
  return conn_str

# Creating dataframe

Headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
urls = []
links_list = []
for r in pages:
  url = 'https://www.amazon.in/s?k=earpods&page=' + str(r)
  urls.append(url)
for i in urls:
  req = requests.get(i, headers=Headers)
  soup = BeautifulSoup(req.content, 'html.parser')
  links = soup.find_all('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    
  for link in links:
    links_list.append(link.get('href'))

d = {'Name': [], 'Price': [], 'Rating': [], 'Number of rating': [], 'Brand': [], 'Model': [], 'Colour': [], 'Headphones form factor': [], 'Connector type': [], 'Product_URL':[]}
for link in links_list:
  new_web = requests.get('https://www.amazon.in' + link, headers=Headers)
  new_soup = BeautifulSoup(new_web.content, 'html.parser')

  d['Name'].append(get_title(new_soup))
  d['Price'].append(get_price(new_soup))
  d['Rating'].append(get_rating(new_soup))
  d['Number of rating'].append(get_nrating(new_soup))
  d['Brand'].append(get_brand(new_soup))
  d['Model'].append(get_model(new_soup))
  d['Colour'].append(get_colour(new_soup))
  d['Headphones form factor'].append(get_formfactor(new_soup))
  d['Connector type'].append(get_connector(new_soup))
  d['Product_URL'].append('https://www.amazon.in' + link)

# Creating dataframe
df = pd.DataFrame.from_dict(d)

#Dataframe
df

