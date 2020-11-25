# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup

import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

#set up the HTML parser:
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# ### Featured Images

# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Use the base URL to create an absolute URL
#using an f-string for this print statement because it's a cleaner way 
#to create print statements; they're also evaluated at run-time. 
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

#to scrape the entire table with Pandas' .read_html() function.
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df

# convert our DataFrame back into HTML-ready code using the .to_html() function. 
df.to_html()

#browser.quit() and execute that cell to end the session.
browser.quit()

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Path to chromedriver
get_ipython().system('which chromedriver')

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)


# <h3>Visit the NASA Mars News Site</h3>

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# <h3>JPL Space Images Featured Image</h3>

# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# <h3>Mars Facts</h3>

df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()

df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df

df.to_html()

# <h3>Mars Weather</h3>

# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)

# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')

# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

# <h1>D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles</h1>

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Use the parent element to find where image url located
results = img_soup.findAll("a", class_='itemLink')
print(results)

#create list to hold the result
new_result = []
#loop the result to get title in h3 tag
for result in range(0, len(results)):
    if(result % 2 != 0):
        new_result.append(results[result])
        
print(new_result)

#img_url = results.find("div", class_='item').get_text()
img_url_rel = collapsible_results.select_one('div.item a img').get("src")
img_url_rel

img_title_url = collapsible_results.select_one('div.description a h3').get_text()
img_title_url

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
#loop through collapsible_results to retrieve image urls and titles
for result in new_result:
    #print(result)
    try: 
        #find image title
        img_title_url = result.find('h3').text
        img_title_click = browser.find_by_tag('h3').click()

        #parse new page
        html = browser.html
        new_soup = soup(html, 'html.parser')
        
        #find downloads class to get a href
        img_url_rel = new_soup.find("div",class_="downloads").find("a")['href']
        #print(img_url_rel)
        
        #create empty dictionary to hold image and title
        url_dict = {}
        url_dict["title"] = img_title_url
        url_dict["img_url"] = img_url_rel
        
        #append the dictionary to the list
        hemisphere_image_urls.append(url_dict)
        
        browser.back()
        
    except AttributeError:
       #img_url_rel = " "
       #img_title_url = " "
       print("No Title Found")

# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)

browser.quit()


