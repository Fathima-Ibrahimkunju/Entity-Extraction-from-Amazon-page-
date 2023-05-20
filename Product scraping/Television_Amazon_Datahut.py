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


# To show the whole content in a column

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

def get_screensize(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-display.size'})
        Screen_Size = model.text
        screensize_real = Screen_Size.replace('Screen Size','')
        screensize_str = screensize_real.strip()
    except AttributeError:
        screensize_str = None
    return screensize_str


def get_brand(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-brand'})
        Brand = model.text
        brand_real = Brand.replace('Brand','')
        brand_str = brand_real.strip()
    except AttributeError:
        brand_str = None
    return brand_str


def get_sup_int_serv(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-supported_internet_services'})
        sis_value = model.text
        sis_real = sis_value.replace('Supported Internet Services','')
        sis_str = sis_real.strip()
    except AttributeError:
        sis_str = ''
    return sis_str


def get_display(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-display.technology'})
        Display = model.text
        display_real = Display.replace('Display Technology','')
        display_str = display_real.strip()
    except AttributeError:
        display_str = ''
    return display_str



def get_resolution(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-resolution'})
        Resolution = model.text
        resolution_real = Resolution.replace('Resolution','')
        resolution_str = resolution_real.strip()
    except AttributeError:
        resolution_str= ''
    return resolution_str



def get_refresh_rate(soup):
    try:
        model = soup.find('tr',attrs = {'a-spacing-small po-refresh_rate'})
        refresh_rate = model.text
        refresh_rate_real = refresh_rate.replace('Refresh Rate','')
        refresh_rate_str = refresh_rate_real.strip()
    except AttributeError:
        refresh_rate_str= ''
    return refresh_rate_str


def get_special_features(soup):
    try:
        model = soup.find('tr',attrs = {'a-spacing-small po-special_feature'})
        special_features= model.text
        special_features_real = special_features.replace('Special Feature','')
        special_features_str = special_features_real.strip()
    except AttributeError:
        special_features_str= ''
    return special_features_str



def get_model_name(soup):
    try:
        model = soup.find('tr',attrs = {'a-spacing-small po-model_name'})
        model_name= model.text
        model_name_real = model_name.replace('Model Name','')
        model_name_str = model_name_real.strip()
    except AttributeError:
        model_name_str= ''
    return model_name_str


def get_mounting_hardware(soup):
    try:
        model = soup.find('tr',attrs = {'a-spacing-small po-included_components'})
        mounting_hardware= model.text
        mounting_hardware_real = mounting_hardware.replace('Mounting Hardware','')
        mounting_hardware_str = mounting_hardware_real.strip()
    except AttributeError:
        mounting_hardware_str= ''
    return mounting_hardware_str



def get_connector_type(soup):
    try:
        model = soup.find('tr',attrs = {'class':'a-spacing-small po-connectivity_technology'})
        connector_type= model.text
        connector_type_real = connector_type.replace('Connector Type','')
        connector_type_str = connector_type.strip()
    except AttributeError:
        connector_type_str= ''
    return connector_type_str


# In[5]:


# Getting the product links

Headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 'Accept-Language':'en-US, en;q=0.5'})
links_list = []
for page in range(1,21):
    url ="https://www.amazon.in/s?k=television&page="+str(page)
    req = requests.get(url, headers = Headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    links = soup.find_all('a', attrs = {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    
    for link in links:
        links_list.append(link.get('href'))
    time.sleep(2)
    
# To remove duplicates

links_final=list(set(links_list))

# To find the total number of links

print(len(links_final))


# In[6]:


# Scraping the features of the products and creating a dictionary from it

d = {'Title':[], 'Price':[], 'Rating':[], 'No_of_ratings':[],  'Screen Size':[], 'Brand':[], 'Supporting Internet Services':[], 'Display':[], 'Resolution':[],'Refresh Rate':[], 'Special Features':[],'Model Name':[], 'Mounting Hardware':[],'Connector Type':[],'URL':[]}

for link in links_final:
    new_web = requests.get('https://www.amazon.in'+str(link), headers=Headers)
    new_soup = BeautifulSoup(new_web.content, 'html.parser')

    d['Title'].append(get_title(new_soup))
    d['Price'].append(get_price(new_soup))
    d['Rating'].append(get_rat(new_soup))
    d['No_of_ratings'].append(get_ratn(new_soup))
    d['Screen Size'].append(get_screensize(new_soup))
    d['Brand'].append(get_brand(new_soup))
    d['Supporting Internet Services'].append(get_sup_int_serv(new_soup))
    d['Display'].append(get_display(new_soup))
    d['Resolution'].append(get_resolution(new_soup))
    d['Refresh Rate'].append(get_refresh_rate(new_soup))
    d['Special Features'].append(get_special_features(new_soup))
    d['Model Name'].append(get_model_name(new_soup))
    d['Mounting Hardware'].append(get_mounting_hardware(new_soup))
    d['Connector Type'].append(get_connector_type(new_soup))
    d['URL'].append('https://www.amazon.in'+str(link))

# Creating dataframe from the dictionary
    
df = pd.DataFrame.from_dict(d)


# In[7]:


df


# In[8]:


# Converting dataframe into csv format

df.to_csv('Television.csv')


# In[9]:


# Converting to json format

json = df.to_json('Television.json')


# In[ ]:




