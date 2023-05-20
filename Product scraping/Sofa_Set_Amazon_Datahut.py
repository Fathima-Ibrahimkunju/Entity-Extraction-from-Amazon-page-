#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing libraries

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import csv


# In[2]:


# To show the whole content of a column

pd.set_option('display.max_colwidth', None)


# In[3]:


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


def get_rat(soup):
    
    try:
        rat = soup.find('i',attrs={'class':'a-icon a-icon-star a-star-4-5'})
        rat_value = rat.text
        rat_string = rat_value.strip()
    except AttributeError:
        rat_string = ''
    return rat_string



def get_ratn(soup):
    
    try:
        ratn = soup.find('span',attrs={'id':'acrCustomerReviewText'})
        ratn_value = ratn.text
        ratn_string = ratn_value.strip()
    except AttributeError:
        ratn_string = ''
    return ratn_string

def get_product_dimensions(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-item_depth_width_height'})
        product_dimensions = model.text
        product_dimensions_real = product_dimensions.replace('Product Dimensions','')
        product_dimensions_str = product_dimensions_real.strip()
    except AttributeError:
        product_dimensions_str = None
    return product_dimensions_str


def get_color(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-color'})
        color = model.text
        color_real = color.replace('Color','')
        color_str = color_real.strip()
    except AttributeError:
        color_str = None
    return color_str


def get_brand(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-brand'})
        brand_value = model.text
        brand_real = brand_value.replace('Brand','')
        brand_str = brand_real.strip()
    except AttributeError:
        brand_str = ''
    return brand_str


def get_style(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-style'})
        style = model.text
        style_real = style.replace('Style','')
        style_str = style_real.strip()
    except AttributeError:
        style_str = ''
    return style_str



def get_special_features(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-special_feature'})
        special_feature = model.text
        special_feature_real = special_feature.replace('Special Feature','')
        special_feature_str = special_feature_real.strip()
    except AttributeError:
        special_feature_str= ''
    return special_feature_str



def get_sofa_type(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-sofa_type'})
        sofa_type = model.text
        sofa_type_real = sofa_type.replace('Type','')
        sofa_type_str = sofa_type_real.strip()
    except AttributeError:
        sofa_type_str= ''
    return sofa_type_str


def get_upholstery_fabric(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-upholstery.fabric_type'})
        upholstery_fabric= model.text
        upholstery_fabric_real = upholstery_fabric.replace('Upholstery Fabric Type','')
        upholstery_fabric_str = upholstery_fabric_real.strip()
    except AttributeError:
        upholstery_fabric_str= ''
    return upholstery_fabric_str



def get_room_type(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-room_type'})
        room_type= model.text
        room_type_real = room_type.replace('Room Type','')
        room_type_str = room_type_real.strip()
    except AttributeError:
        room_type_str= ''
    return room_type_str


def get_seating_capacity(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-seating_capacity'})
        seating_capacity= model.text
        seating_capacity_real = seating_capacity.replace('Seating Capacity','')
        seating_capacity_str = seating_capacity_real.strip()
    except AttributeError:
        seating_capacity_str= ''
    return seating_capacity_str


def get_frame_material(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-frame.material'})
        frame_material= model.text
        frame_material_real = frame_material.replace('Frame Material','')
        frame_material_str = frame_material_real.strip()
    except AttributeError:
        frame_material_str= ''
    return frame_material_str


def get_shape(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-item_shape'})
        shape= model.text
        shape_real = shape.replace('Shape','')
        shape_str = shape.strip()
    except AttributeError:
        shape_str= ''
    return shape_str


# In[4]:


# Getting the product links

Headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'Accept-Language':'en-US, en;q=0.5'})
links_list = []
for page in range(1,8):
    url ="https://www.amazon.in/s?k=sofa+set&page="+str(page)
    req = requests.get(url, headers = Headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    links = soup.find_all('a', attrs = {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    
    for link in links:
        links_list.append(link.get('href'))

# To remove duplicates

links_final=list(set(links_list))

# To find the total number of links

print(len(links_final))


# In[6]:


# Scraping the features of the products and creating a dictionary from it

d = {'Title':[], 'Price':[], 'Rating':[], 'No_of_ratings':[],  'Product Dimensions':[], 'Color':[], 'Brand':[], 'Style':[], 'Special Feature':[],'Sofa Type':[], 'Upholstery Fabric Type':[],'Room Type':[], 'Seating Capacity':[],'Frame Material':[],'Shape':[],'URL':[]}

for link in links_final:
    new_web = requests.get('https://www.amazon.in'+str(link), headers=Headers)
    new_soup = BeautifulSoup(new_web.content, 'html.parser')

    d['Title'].append(get_title(new_soup))
    d['Price'].append(get_price(new_soup))
    d['Rating'].append(get_rat(new_soup))
    d['No_of_ratings'].append(get_ratn(new_soup))
    d['Product Dimensions'].append(get_product_dimensions(new_soup))
    d['Color'].append(get_color(new_soup))
    d['Brand'].append(get_brand(new_soup))
    d['Style'].append(get_style(new_soup))
    d['Special Feature'].append(get_special_features(new_soup))
    d['Sofa Type'].append(get_sofa_type(new_soup))
    d['Upholstery Fabric Type'].append(get_upholstery_fabric(new_soup))
    d['Room Type'].append(get_room_type(new_soup))
    d['Seating Capacity'].append(get_seating_capacity(new_soup))
    d['Frame Material'].append(get_frame_material(new_soup))
    d['Shape'].append(get_shape(new_soup))
    d['URL'].append('https://www.amazon.in'+str(link))

# Creating dataframe from the dictionary

df = pd.DataFrame.from_dict(d)


# In[7]:


df


# In[10]:


# Converting dataframe into csv format

df.to_csv('Sofa_set.csv')


# In[11]:


# Converting to json format

js = df.to_json('Sofa_Set.json')


# In[ ]:




