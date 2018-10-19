from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from pprint import pprint

def scrape():
    return {
        'news': news(),
        'space_images': space_images(),
        'mars_weather': space_twitter(),
        'mars_facts': mars_facts(),
        'mars_hemispheres': mars_hemispheres()
    }

def news():
    url = 'https://mars.nasa.gov/news/'

    content = urlopen(url)
    c=content.read()
    soup = BeautifulSoup(c, 'html.parser')
    slides = soup.find_all(class_='slide')
    news = []
    for slide in slides:
        link = slide.a.get('href')
        description = slide.find(class_='rollover_description_inner').text
        title = slide.find(class_='content_title').text
        news.append({'link': link,
                    'description': description,
                    'title': title})
        
    return news

def space_images():
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    jpl_base_url = 'https://www.jpl.nasa.gov'
    from splinter import Browser

    with Browser('chrome') as browser:
        # Visit URL
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'lxml')
        footer = soup.body.find(class_="carousel_item").attrs['style'].split("\'")[1]
        featured_image_url = jpl_base_url + footer
    print(featured_image_url)
    return featured_image_url


def space_twitter():
    #TWITTER
    url = 'https://twitter.com/marswxreport?lang=en'

    content = urlopen(url)
    c=content.read()
    soup = BeautifulSoup(c, 'html.parser')
    slides = soup.find(class_='js-tweet-text-container')
    mars_weather = slides.text
    return mars_weather

def mars_facts():
    #MARS FACCTS
    import pandas as pd
    url = 'https://space-facts.com/mars/'
    dfs = pd.read_html(url) 
    mars_facts = dfs[0]
    mars_facts.columns = ['Description','Value']
    mars_facts.set_index('Description', inplace=True)
    mars_facts_html = mars_facts.to_html()
    mars_facts_html = mars_facts_html.replace('\n', '')
    return mars_facts_html

def mars_hemispheres():
    #MARS HEMISPHERES
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    content = urlopen(url)
    c=content.read()
    soup = BeautifulSoup(c, 'html.parser')
    items = soup.find_all(class_='item')
    hemisphere_image_urls = []
    for item in items:
        link = ''.join(url.split('search')[0])+ item.a.get('href')
        content = urlopen(link)
        c=content.read()
        soup = BeautifulSoup(c, 'html.parser')
        title = soup.find(class_='title').text
        hemisphere_image_urls.append({'title': title, 'url': link})

    return hemisphere_image_urls
        