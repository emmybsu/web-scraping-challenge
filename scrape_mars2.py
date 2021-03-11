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
#def scrape_info():
    #browser = init_browser()

    #url of news page to be scraped
    
def nasa_all():
    browser = init_browser()
    news_url = 'https://mars.nasa.gov/news'
    browser.visit(news_url)
    html = browser.html
    #Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')
    # title = soup.title.text
    #paragraphs = soup.find_all('a')
    

    #retrieve page with the requests module
    #response = requests.get(news_url)
    try:


        title = soup.find_all('div', class_='content_title')
        nasa_title = title[0].text.strip()
   
        para = soup.find_all('div', class_='rollover_description_inner')
        nasa_paragraph = para[0].text.strip()
    except AttributeError:
        return None, None

    return nasa_title, nasa_paragraph

    # # JPL Mars Space Images - Featured Image
def featured_image_url():
    browser = init_browser()
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
    return featured_image_url

def clean_html_table():
    # # Mars Facts
    #browser = init_browser()
    

    facts_url = 'https://space-facts.com/mars/'
    #browser.visit()
    try:
        tables = pd.read_html(facts_url)

        df = tables[0]
    except BaseException:
        return None


    html_table = df.to_html()
    clean_html_table = html_table.replace('\n', ' ')
    return clean_html_table

    # # Mars Hemispheres
def mars_hemis():
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=False)
    browser = init_browser()

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)

    # html = browser.html
    # soup = bs(html,'html.parser')

    mars_hemis = []

    # loop through the four tags and load the data to the dictionary

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        #partial = soup.find("img", class_="wide-image")["src"]
        try:
            partial = soup.find('a', text = 'Sample').get('href')
            img_title = soup.find("h2",class_="title").get_text()

        except AttributeError: 
            partial = None
            img_title = None
        img_url = partial
        #img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()
    return mars_hemis
        

def scrape_all():
    browser = init_browser()
    nasa_title, nasa_paragraph = nasa_all()
    mars_data = {
        'mars_hemis': mars_hemis(), 
        "clean_html_table": clean_html_table(),
        "featured_image_url": featured_image_url(),
        "nasa_title": nasa_title,
        "nasa_paragraph": nasa_paragraph

    }

    #print(mars_hemis)
    

    browser.quit()

    return mars_data

