# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
#import pandas
import pandas as pd
import datetime as dt


# Set the executable path and initialize the chrome browser in splinter
#executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

def scrape_all():
    #initiate headless driver
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    #browser = Browser("chrome", **executable_path, headless=True)

    # set news title and paragrapp equal to mars_news() function
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# function to get mars update
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### JPL Space Images Featured Image

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        #img_url_rel

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    # using an f-string for this print statement because it's a cleaner way
    # to create print statements; they're also evaluated at run-time.
    img_url = f"https://www.jpl.nasa.gov{img_url_rel}"
    #img_url

    return img_url


# ## Mars Facts

def mars_facts():
    try:
        # print(pd.read_html('http://space-facts.com/mars/')[0])
        # use Pandas '.read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
        #df = pd.read_html('http://space-facts.com/mars/')

    except BaseException:
        #print("Error!")
        #raise
        return None

    # Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # use to_html method to convert DataFrame back into HTML format, add bootstrap.
    return df.to_html(classes="table table-striped")


test_output = mars_facts()
# tells Flask that our script is complete and ready for action.
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
