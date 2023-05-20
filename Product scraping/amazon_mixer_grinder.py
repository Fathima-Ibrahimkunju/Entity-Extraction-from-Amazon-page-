
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
        title_string = 'Information not available'
    return title_string

def get_price(soup):
    try:
        price = soup.find('span',attrs={'class':'a-price-whole'})
        price_value = price.text
        price_str = price_value.strip()
    except AttributeError:
        price_str ='Information not available'
    return price_str


def get_rating(soup):
    
    try:
        rat = soup.find('i',attrs={'class':'a-icon-alt'})
        rat_value = rat.text
        rat_string = rat_value.strip()
    except AttributeError:
        rat_string = 'Information not available'
    return rat_string



def get_nrating(soup):
    
    try:
        ratn = soup.find('span',attrs={'id':'acrCustomerReviewText'})
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
        brand_str = brand_value.strip()
    except AttributeError:
        brand_str = 'Information not available'
    return brand_str


def get_material(soup):
    try:
        material = soup.find('tr',attrs = {'class':'a-spacing-small po-material'})
        material_value = material.text
        material_real = material_value.replace('Material   ','')
        material_str = material_real.strip()
    except AttributeError:
        material_str = 'Information not available'
    return material_str


def get_blade(soup):
    try:
        blade_material = soup.find_all('tr',attrs = {'class':'a-spacing-small po-blade.material'})
        blade_material_value = blade_material.text
        blade_material_real = blade_material_value.replace('Blade Material   ','')
        blade_material_str = blade_material_value.strip()
    except AttributeError:
        blade_material_str = 'Information not available'
    return blade_material_str


def get_colour(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-color'})
        colour_value = model.text
        colour_real = colour_value.replace('Colour   ','')
        colour_str = colour_real.strip()
    except AttributeError:
        colour_str = 'Information not available'
    return colour_str



def get_speed(soup):
    try:
        no_of_speed = soup.find('tr',attrs = {'class':'a-spacing-small po-number_of_speeds'})
        no_of_speed_value = no_of_speed.text
        no_of_speed_real = no_of_speed_value.replace('Number of Speeds   ','')
        no_of_speed_str = no_of_speed_real.strip()
    except AttributeError:
        no_of_speed_str = 'Information not available'
    return no_of_speed_str



def get_dimension(soup):
    try:
        prod_dim = soup.find('tr',attrs = {'class':'a-spacing-small po-item_depth_width_height'})
        prod_dim_value = prod_dim.text
        prod_dim_real = prod_dim_value.replace('Product Dimensions   ','')
        prod_dim_str = prod_dim_real.strip()
    except AttributeError:
        prod_dim_str = 'Information not available'
    return prod_dim_str



def get_voltage(soup):
    try:
        voltage = soup.find('tr',attrs = {'class':'a-spacing-small po-voltage'})
        voltage_value = voltage.text
        voltage_real = voltage_value.replace('Voltage   ','')
        voltage_str = voltage_real.strip()
    except AttributeError:
        voltage_str = 'Information not available'
    return voltage_str



def get_wattage(soup):
    try:
        wattage = soup.find('tr',attrs = {'class':'a-spacing-small po-wattage'})
        wattage_value = wattage.text
        wattage_real = wattage_value.replace('Wattage   ','')
        wattage_str = wattage_real.strip()
    except AttributeError:
        wattage_str = 'Information not available'
    return wattage_str



def get_weight(soup):
    try:
        weight = soup.find('tr',attrs = {'class':'a-spacing-small po-item_weight'})
        weight_value = weight.text
        weight_real = weight_value.replace('Item Weight   ','')
        weight_str = weight_real.strip()
    except AttributeError:
        weight_str = 'Information not available'
    return weight_str



def get_model(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-model_name'})
        model_value = model.text
        model_real = model_value.replace('Model Name   ','')
        model_str = model_real.strip()
    except AttributeError:
        model_str = 'Information not available'
    return model_str

# Defining the number of pages
pages = []
for i in range (1,21):
  pages.append(i)

# Getting the product links

if __name__ == '__main__':
    Headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'Accept-Language':'en-US, en;q=0.5'})
    
    d = {'Name':[], 'Price':[], 'Rating':[], 'Number of rating':[], 'Brand':[], 'Model':[], 'Material':[], 'Blade Material':[], 'Colour':[], 'Number of speeds':[], 'Product Dimensions':[], 'Voltage':[], 'Wattage':[], 'Item Weight':[], 'Product_URL':[]}
    urls = []
    links_list = []
    for r in pages:
        url = 'https://www.amazon.in/s?k=mixer+grinder&page='+str(r)
        urls.append(url)
    for i in urls:
        req = requests.get(i, headers = Headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        links = soup.find_all('a', attrs = {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        
        for link in links:
            links_list.append(link.get('href'))

for link in links_list:
            new_web = requests.get('https://www.amazon.in'+link, headers=Headers)
            new_soup = BeautifulSoup(new_web.content, 'html.parser')
        
        
            d['Name'].append(get_title(new_soup))
            d['Price'].append(get_price(new_soup))
            d['Rating'].append(get_rating(new_soup))
            d['Number of rating'].append(get_nrating(new_soup))
            d['Brand'].append(get_brand(new_soup))
            d['Model'].append(get_model(new_soup))
            d['Material'].append(get_material(new_soup))
            d['Blade Material'].append(get_blade(new_soup))
            d['Colour'].append(get_colour(new_soup))
            d['Number of speeds'].append(get_speed(new_soup))
            d['Product Dimensions'].append(get_dimension(new_soup))
            d['Voltage'].append(get_voltage(new_soup))
            d['Wattage'].append(get_wattage(new_soup))
            d['Item Weight'].append(get_weight(new_soup))
            d['Product_URL'].append('https://www.amazon.in'+link)

# Creating dataframe
df = pd.DataFrame.from_dict(d)

#Dataframe
df

