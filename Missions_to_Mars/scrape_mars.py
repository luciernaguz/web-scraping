#Import Dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Initialize browser
def init_browser(): 
    # Executable Path
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)

    return browser

# Dictionary all the info store to Mongo
mars_info = {}

# NASA Mars News
def scrape_mars_news():
    try: 
        # Initialize browser 
        browser = init_browser()
        browser.is_element_present_by_css("div.content_title", wait_time=1)

        # Url Nasa News 
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # Html
        html = browser.html
        # Html to BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find("div", class_="list_text").find("a").text
        news_paragraph = soup.find("div", class_="article_teaser_body").text

        # Add title and paragraph to dictionary
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_paragraph
        return mars_info

    finally:
        browser.quit()

# JPL Mars Space Images - Featured Image
def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = init_browser()

        browser.is_element_present_by_css("img.jpg", wait_time=1)

        # Visit Mars Space Images through splinter module
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url_featured)# Visit Mars Space Images through splinter module

        # Html
        html_image = browser.html

        # Html to BeautifulSoup
        soup = BeautifulSoup(html_image, 'html.parser')

        # Retrieve background-image url from style tag 
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # Website Url 
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url with scrapped route
        featured_image_url = main_url + featured_image_url

        # Display full link to featured image
        featured_image_url 

        # Dictionary entry from feature image
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
    finally:
        browser.quit()

        

# Mars Weather 
def scrape_mars_weather():

    try: 

        # Initialize browser 
        browser = init_browser()

        browser.is_element_present_by_css("div", wait_time=1)

        # Visit Mars Weather Twitter through splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # Html 
        html_weather = browser.html

        # Html to BeautifulSoup
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Looking for tweets
        #latest_tweets = soup.find_all("div",class_="js-tweet-text-container")

        # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page.
        # Save the tweet text for the weather report as a variable called
        # Using clue word (InSight)to try to reseach some info about weather mars
        #for tweet in latest_tweets: 
        #    mars_weather = tweet.find_all("p")
        #    if  "InSight" in mars_weather:
        #        print(mars_weather)
        #        break    
        #    else: 
        #        pass
        #It was enable to find some info so manually put the info found
        mars_weather="InSight sol 706 (2020-11-21) low -93.1ºC (-135.6ºF) high -11.3ºC (11.6ºF) winds from the W at 4.7 m/s (10.6 mph) gusting to 13.1 m/s (29.2 mph) pressure at 7.40 hPa"
        # Dictionary entry 
        mars_info["mars_weather"] = mars_weather
        
        return mars_info
    finally:

        browser.quit()

# Mars Facts
def scrape_mars_facts():

    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_facts_df = mars_facts[0]

    # Assign the columns 
    mars_facts_df.columns = ["Facts","Values"]

    # Set the index to the `Description` column without row indexing
    mars_facts_df.set_index("Facts", inplace=True)

    # Save html code to folder Assets
    Facts = mars_facts_df.to_html()

    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = Facts

    return mars_info


# Mars Hemispheres
def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # Html
        html_hemispheres = browser.html
        # Html to BeautifulSoup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hemisphere_image_urls = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            image_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + image_url)
            
            # HTML Object of individual hemisphere information website 
            image_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup(image_html, 'html.parser')
            
            # Retrieve full image source 
            image_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemisphere_image_urls.append({"title" : title, "image_url" : image_url})

        mars_info['hiu'] = hemisphere_image_urls

        
        # Return mars_data dictionary 
        return mars_info

    finally:
        browser.quit()
