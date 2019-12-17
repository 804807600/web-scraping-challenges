from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
def scrape():
    executable_path={"executable_path":"chromedriver"}
    browser=Browser("chrome",**executable_path, headless=False)
    mars_data={}
    #NASA Mars News
    newsurl="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(newsurl)
    html=browser.html
    soup=bs(html,"html.parser")
    news_title=soup.find('div', class_="content_title").get_text()
    news_p=soup.find('div',class_="article_teaser_body").get_text()
    mars_data["news_title"]=news_title
    mars_data["news_p"]=news_p
    #JPL Mars Space Images
    img_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    html=browser.html
    soup=bs(html,"html.parser")
    img=soup.find_all('a',class_='fancybox')
    src = []
    for image in img:
        pic = image['data-fancybox-href']
        src.append(pic)

    featured_image_url = 'https://www.jpl.nasa.gov' + pic[6]
    mars_data["featured_image_url"]=featured_image_url
    #Mars Weather
    weather_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    html=browser.html
    soup=bs(html,"html.parser")
    mars_weather=soup.find('p',class_="tweet-text").get_text()
    mars_data["mars_weather"]=mars_weather
    #Mars facts
    facts_ucl="https://space-facts.com/mars/"
    facts_df=pd.read_html(facts_ucl)[0]
    facts_table=facts_df.to_html(header=False,index=False)
    mars_data["facts_table"]=facts_table
    #Mars Hemispher
    hemispher_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispher_url)
    html=browser.html
    soup=bs(html,'html.parser')
    hemisphere_image_urls=[]
    for i in range(4):
        image=browser.find_by_tag('h3')
        image[i].click()
        html=browser.html
        soup=bs(html, 'html.parser')
        img_url=soup.find('img',class_="wide-image")["src"]
        title=soup.find('h2',class_="title").text
        dictionary={"title":title, "img_url":img_url}
        hemisphere_image_urls.append(dictionary)
        browser.back()
    mars_data["hemisphere_image_urls"]=hemisphere_image_urls
    return mars_data
    