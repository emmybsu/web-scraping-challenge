#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Dependencies

import os
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time


# In[2]:


from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[3]:


#create chrome webpage that allows manipulation from jupyter notebook coding
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# # NASA Mars News

# In[4]:


#url of news page to be scraped
news_url = 'https://mars.nasa.gov/news'


# In[5]:


#retrieve page with the requests module
response = requests.get(news_url)


# In[6]:


#Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, 'html.parser')


# In[7]:


title = soup.title.text
print(title)


# In[8]:


paragraphs = soup.find_all('a')


# In[9]:


title = soup.find_all('div', class_='content_title')
nasa_title = title[0].text.strip()
nasa_title


# In[10]:


para = soup.find_all('div', class_='rollover_description_inner')
nasa_paragraph = para[0].text.strip()
nasa_paragraph


# # JPL Mars Space Images - Featured Image

# In[11]:


#url of JPL Featured Space Image
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[12]:


html = browser.html
soup = bs(html,'html.parser')


# In[13]:


images = soup.find_all('div', class_='floating_text_area')


# In[14]:


for img in images:
    
    link = img.find('a')
    href = link['href']
    
    
    print( 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + href )

featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + href
    


# In[15]:


browser.quit()


# # Mars Facts

# In[16]:


facts_url = 'https://space-facts.com/mars/'


# In[17]:


tables = pd.read_html(facts_url)


# In[18]:


df = tables[0]
df


# In[19]:


html_table = df.to_html()
html_table


# In[20]:


clean_html_table = html_table.replace('\n', ' ')
clean_html_table


# # Mars Hemispheres

# In[21]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[22]:


hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemi_url)


# In[23]:


html = browser.html
soup = bs(html,'html.parser')

mars_hemis = []


# In[24]:


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


# In[25]:


print(mars_hemis)


# In[26]:


browser.quit()

