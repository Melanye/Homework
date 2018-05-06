
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import re
import pandas as pd
import time


# In[2]:


def startBrowser():
    global browser
    executable_path = {'executable_path': 'c:\chromedriver\chromedriver.exe'}
    browser = Browser('chrome', **executable_path)


# In[3]:


def getNews():
    startBrowser()
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    result = soup.find(attrs={"class": "list_text"})

    with browser:
        try:
            # Identify and return title of news
            news_title = result.a.text
            # Identify and return news paragraph
            news_p = result.find(attrs={"class": "article_teaser_body"}).text

            # Run only if news title, and paragraph are available
            if (news_title and news_p):

                # Dictionary to be inserted as a MongoDB document
                post = {
                    'title': news_title,
                    'news_p': news_p,
                }
        except Exception as e:
            print(e)  
    return post


# In[4]:


def getFeaturedImage():
    startBrowser()
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    img_url_base= img_url[:24]
    featured_image_url =[]

    browser.visit(img_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(4)
    with browser:
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        featured_image_url = soup.find('img', attrs={"class": "fancybox-image"})['src']
        featured_image_url = img_url_base + featured_image_url
    return featured_image_url


# In[5]:


def getWeather():
    startBrowser()
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    with browser:
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        mars_weather = soup.find(text=re.compile('Sol'))
    return mars_weather


# In[6]:


def getFacts():
    startBrowser()
    mars_facts_url = 'https://space-facts.com/mars/'
    results = pd.read_html(mars_facts_url, attrs={'id': 'tablepress-mars'}, flavor=['bs4'])
    keys=[]
    values =[]
    for key, value in results[0]._values:
        keys.append(key.strip(':'))
        values.append(value)
    mars_facts = dict(zip(keys, values))
    return mars_facts


# In[7]:


def getHemisphereImages():
    startBrowser()
    img_hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    img_hemis_url_base = img_hemis_url[:29]
    hemisphere_image_urls = []
    browser.visit(img_hemis_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    links_found = soup.find_all(attrs={"class": 'description'})

    with browser:
        for link in links_found:
            try:
                title = link.a.text
                browser.click_link_by_partial_text(title)
                curr_html = browser.html
                soup = BeautifulSoup(curr_html, 'html.parser')
                result = [x['src'] for x in soup.findAll('img', attrs={"class": "wide-image"})]
                img_url = img_hemis_url_base + result[0]
                img_dict = {'title': title, 'img_url': img_url}
                hemisphere_image_urls.append(img_dict)
            except Exception as e:
                print(e)
            finally:
                browser.back()
    return hemisphere_image_urls


# latest_news = getNews()

# In[ ]:


print('Mars Lastest New\n {} \n {}' .format(latest_news['title'], latest_news['news_p']))


# In[ ]:


FeaturedImageURL = getFeaturedImage()
print('URL to Featured Image \n{}' .format(FeaturedImageURL))


# In[ ]:


mars_facts = getFacts()
pd.DataFrame(mars_facts, index=['Facts'])


# In[ ]:


weather = getWeather()
print('Lastest Weather\n{}' .format(weather))


# In[ ]:


hemisphereImages = getHemisphereImages()


# for value in hemisphereImages:
#     print('Title: {}\n URL:\n {}' .format(value['title'], value['img_url']))
