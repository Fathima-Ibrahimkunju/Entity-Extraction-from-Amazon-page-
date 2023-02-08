#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing libraries

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import csv
import time


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

def get_brand(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-brand'})
        Brand = model.text
        brand_real = Brand.replace('Brand','')
        brand_str = brand_real.strip()
    except AttributeError:
        brand_str = None
    return brand_str

def get_capacity(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-capacity'})
        capacity = model.text
        capacity_real = capacity.replace('Capacity','')
        capacity_str = capacity_real.strip()
    except AttributeError:
        capacity_str = None
    return capacity_str

def get_configuration(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-configuration'})
        configuration_value = model.text
        configuration_real = configuration_value.replace('Configuration','')
        configuration_str = configuration_real.strip()
    except AttributeError:
        configuration_str = ''
    return configuration_str


def get_energy_star(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-energy_star'})
        energy_star = model.text
        energy_star_real = energy_star.replace('Energy Star','')
        energy_star_str = energy_star_real.strip()
    except AttributeError:
        energy_star_str = ''
    return energy_star_str



def get_color(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-color'})
        color = model.text
        color_real = color.replace('Colour','')
        color_str = color_real.strip()
    except AttributeError:
        color_str= ''
    return color_str

def get_special_features(soup):
    try:
        model = soup.find('tr',attrs = {'a-spacing-small po-special_feature'})
        special_features= model.text
        special_features_real = special_features.replace('Special Feature','')
        special_features_str = special_features_real.strip()
    except AttributeError:
        special_features_str= ''
    return special_features_str


 


# In[4]:


# Getting the product links

Headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'Accept-Language':'en-US, en;q=0.5'})
links_list = []
for page in range(1,21):
    url ="https://www.amazon.in/s?k=refrigerator&page="+str(page)
    req = requests.get(url, headers = Headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    links = soup.find_all('a', attrs = {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    
    for link in links:
        links_list.append(link.get('href'))
        
# To remove duplicates

links_final=list(set(links_list))

# To find the total number of links

print(len(links_final))


# In[5]:


# Scraping the features of the products and creating a dictionary from it

d = {'Title':[], 'Price':[], 'Rating':[], 'No_of_ratings':[], 'Brand':[], 'Capacity':[], 'Configuration':[], 'Energy Star':[],'Color':[],'Special Features':[],'URL':[]}

for link in links_final:
    new_web = requests.get('https://www.amazon.in'+str(link), headers=Headers)
    new_soup = BeautifulSoup(new_web.content, 'html.parser')

    d['Title'].append(get_title(new_soup))
    d['Price'].append(get_price(new_soup))
    d['Rating'].append(get_rat(new_soup))
    d['No_of_ratings'].append(get_ratn(new_soup))
    d['Brand'].append(get_brand(new_soup))
    d['Capacity'].append(get_capacity(new_soup))
    d['Configuration'].append(get_configuration(new_soup))
    d['Energy Star'].append(get_energy_star(new_soup))
    d['Color'].append(get_color(new_soup))
    d['Special Features'].append(get_special_features(new_soup))
    d['URL'].append('https://www.amazon.in'+str(link))

# Creating dataframe from the dictionary

df = pd.DataFrame.from_dict(d)


# In[6]:


df


# In[7]:


# Converting dataframe into csv format

df.to_csv('Refrigerator.csv')


# In[8]:


# Converting to json format

json = df.to_json('Refrigerator.json')


# In[ ]:




