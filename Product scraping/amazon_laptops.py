
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
        title = soup.find('span',attrs={'id':'productTitle'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = 'No information available'
    return title_string

def get_price(soup):
    try:
        price = soup.find('span',attrs={'class':'a-price-whole'})
        price_value = price.text
        price_str = price_value.strip()
    except AttributeError:
        price_str ='No information available'
    return price_str


def get_rating(soup):
    try:
        rating = soup.find('span',attrs={'class':'a-icon-alt'})
        rating_value = rating.text
        rating_str = rating_value.strip()
    except AttributeError:
        rating_str ='No information available'
    return rating_str



def get_nrating(soup):
    try:
        nrating = soup.find('span',attrs={'id':'acrCustomerReviewText'})
        nrating_value = nrating.text
        nrating_str = nrating_value.strip()
    except AttributeError:
        nrating_str ='No information available'
    return nrating_str




def get_brand(soup):
    try:
        brand = soup.find('tr',attrs = {'class':'a-spacing-small po-brand'})
        brand_value = brand.text
        brand_real = brand_value.replace('Brand   ','')
        brand_str = brand_real.strip()
    except AttributeError:
        brand_str = 'No information available'
    return brand_str


def get_model(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-model_name'})
        model_value = model.text
        model_real = model_value.replace('Model Name   ','')
        model_str = model_real.strip()
    except AttributeError:
        model_str = 'No information available'
    return model_str


def get_screen(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-display.size'})
        screen_value = model.text
        screen_real = screen_value.replace('Screen Size   ','')
        screen_str = screen_real.strip()
    except AttributeError:
        screen_str = 'No information available'
    return screen_str


def get_colour(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-color'})
        colour_value = model.text
        colour_real = colour_value.replace('Colour   ','')
        colour_str = colour_real.strip()
    except AttributeError:
        colour_str = 'No information available'
    return colour_str


def get_cpu(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-cpu_model.family'})
        cpu_value = model.text
        cpu_real = cpu_value.replace('CPU Model   ','')
        
        
        cpu_str = cpu_real.strip()
    except AttributeError:
        cpu_str = 'No information available'
    return cpu_str


def get_RAM(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-ram_memory.installed_size'})
        RAM_value = model.text
        RAM_real = RAM_value.replace('RAM Memory Installed Size   ','')
        RAM_str = RAM_real.strip()
    except AttributeError:
        RAM_str = 'No information available'
    return RAM_str


def get_OS(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-operating_system'})
        OS_value = model.text
        OS_real = OS_value.replace('Operating System   ','')
        OS_str = OS_real.strip()
    except AttributeError:
        OS_str = 'No information available'
    return OS_str



def get_SF(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-special_feature'})
        SF_value = model.text
        SF_real = SF_value.replace('Special Feature   ','')
        SF_str = SF_real.strip()
    except AttributeError:
        SF_str = 'No information available'
    return SF_str


def get_graphics(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-graphics_description'})
        graphics_value = model.text
        graphics_real = graphics_value.replace('Graphics Card Description   ','')
        graphics_str = graphics_real.strip()
    except AttributeError:
        graphics_str = 'No information available'
    return graphics_str


def get_graphicsCo(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-graphics_coprocessor'})
        graphicsCo_value = model.text
        graphicsCo_real = graphicsCo_value.replace('Graphics Coprocessor   ','')
        graphicsCo_str = graphicsCo_real.strip()
    except AttributeError:
        graphicsCo_str = 'No information available'
    return graphicsCo_str

# Defining the number of pages
pages = []
for i in range (1,21):
  pages.append(i)

# Getting the product links


Headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 'Accept-Language':'en-US, en;q=0.5'})
    
d = {'Name':[], 'Price':[], 'Rating':[], 'No_of_rating':[], 'Brand':[], 'Model':[], 'Screen_size':[], 'Colour':[], 'CPU_model':[], 'RAM_size':[], 'Operating_system':[], 'Special_feature':[], 'Graphics_card_description':[], 'Graphics_coprocessor':[], 'Product_URL':[]}
urls = []
links_list = []
for r in pages:
  url = 'https://www.amazon.in/s?k=laptop&s=relevanceblender&page='+str(r)
  urls.append(url)
for i in urls:
  req = requests.get(i, headers = Headers)
  soup = BeautifulSoup(req.content, 'html.parser')
  links = soup.find_all('a', attrs = {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}) 
  for link in links:
    links_list.append(link.get('href'))

# Scraping the features of the products and creating a dictionary from it

d = {'Name':[], 'Price':[], 'Rating':[], 'No_of_rating':[], 'Brand':[], 'Model':[], 'Screen_size':[], 'Colour':[], 'CPU_model':[], 'RAM_size':[], 'Operating_system':[], 'Special_feature':[], 'Graphics_card_description':[], 'Graphics_coprocessor':[], 'Product_URL':[]}
    
for link in links_list:
    new_web = requests.get('https://www.amazon.in'+str(link), headers=Headers)
    new_soup = BeautifulSoup(new_web.content, 'html.parser')

    d['Name'].append(get_title(new_soup))
    d['Price'].append(get_price(new_soup))
    d['Rating'].append(get_rating(new_soup))
    d['No_of_rating'].append(get_nrating(new_soup))
    d['Brand'].append(get_brand(new_soup))
    d['Model'].append(get_model(new_soup))
    d['Screen_size'].append(get_screen(new_soup))
    d['Colour'].append(get_colour(new_soup))
    d['CPU_model'].append(get_cpu(new_soup))
    d['RAM_size'].append(get_RAM(new_soup))
    d['Operating_system'].append(get_OS(new_soup))
    d['Special_feature'].append(get_SF(new_soup))
    d['Graphics_card_description'].append(get_graphics(new_soup))
    d['Graphics_coprocessor'].append(get_graphicsCo(new_soup))
    d['Product_URL'].append('https://www.amazon.in'+link)

# Creating dataframe
df = pd.DataFrame.from_dict(d)

#Dataframe
df

