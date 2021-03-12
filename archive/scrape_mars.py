#!/usr/bin/env python
# coding: utf-8

#Dependencies

import os
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
#create chrome webpage that allows manipulation from jupyter notebook coding
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

# # NASA Mars News
def scrape_info():

#url of news page to be scraped
    news_url = 'https://mars.nasa.gov/news'

#retrieve page with the requests module
response = requests.get(news_url)

#Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, 'html.parser')
title = soup.title.text
paragraphs = soup.find_all('a')

title = soup.find_all('div', class_='content_title')
nasa_title = title[0].text.strip()

para = soup.find_all('div', class_='rollover_description_inner')
nasa_paragraph = para[0].text.strip()

# # JPL Mars Space Images - Featured Image

#url of JPL Featured Space Image
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

html = browser.html
soup = bs(html,'html.parser')

images = soup.find_all('div', class_='floating_text_area')

for img in images:
    
    link = img.find('a')
    href = link['href']
    
    
    print( 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + href )

featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + href

browser.quit()


# # Mars Facts

facts_url = 'https://space-facts.com/mars/'

tables = pd.read_html(facts_url)

df = tables[0]


html_table = df.to_html()
clean_html_table = html_table.replace('\n', ' ')

# # Mars Hemispheres

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemi_url)

html = browser.html
soup = bs(html,'html.parser')

mars_hemis = []

# loop through the four tags and load the data to the dictionary

for i in range (4):
    time.sleep(5)
    images = browser.find_by_tag('h3')
    images[i].click()
    html = browser.html
    soup = bs(html, 'html.parser')
    partial = soup.find("img", class_="wide-image")["src"]
    img_title = soup.find("h2",class_="title").text
    img_url = 'https://astrogeology.usgs.gov'+ partial
    dictionary={"title":img_title,"img_url":img_url}
    mars_hemis.append(dictionary)
    browser.back()

mars_data = {
    'mars_hemis': mars_hemis, 
    "clean_html_table": clean_html_table,
    "featured_image_url": featured_image_url,
    "nasa_title": nasa_title,
    "nasa_paragraph": nasa_paragraph

}

print(mars_hemis)

browser.quit()

return mars_data

