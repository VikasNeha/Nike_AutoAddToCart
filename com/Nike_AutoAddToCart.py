import config
from ConfigParser import ConfigParser
from PageEvents.nikeEvents import NikeEvents
import time
from bs4 import BeautifulSoup
import urllib2
import re
from Utilities.myLogger import logger
import sys


def readProperties():
    Config = ConfigParser()
    fileName = 'Resources\properties.ini'
    Config.read(config.get_main_dir() + "\\" + fileName)
    config.Email = Config.get('Information', 'Email').strip()
    config.Password = Config.get('Information', 'Password').strip()
    config.Keyword = Config.get('Information', 'Keyword').strip()
    config.Size = Config.get('Information', 'Size').strip()

    config.ProxyIP = Config.get('Information', 'ProxyIP').strip()
    # config.ProxyUsername = Config.get('Information', 'ProxyUsername').strip()
    # config.ProxyPassword = Config.get('Information', 'ProxyPassword').strip()


def make_soup(url):
    opener = urllib2.build_opener(
        urllib2.HTTPHandler(),
        urllib2.HTTPSHandler(),
        urllib2.ProxyHandler({'https': config.ProxyIP}))
    urllib2.install_opener(opener)
    html = urllib2.urlopen(url).read()
    return BeautifulSoup(html, "html.parser")


def get_desired_url():
    BASE_URL = "https://twitter.com/nikestore"
    while True:
        soup = make_soup(BASE_URL)
        contents = soup.find_all("div", class_="content")
        for content in contents:
            tweetText = content.p.text
            if config.Keyword in tweetText and ('available' in tweetText or 'arrived' in tweetText):
                urls = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                                  tweetText)
                return urls[0]
        time.sleep(4)

readProperties()

try:

    nike = NikeEvents(config.ProxyIP)

    logger.info("Opening Nike Site...")
    nike.navigate("http://store.nike.com/us/en_us/?l=shop%2Clogin")
    logger.info("...Opened Nike Site")
    logger.info(nike.driver.title)
    logger.info(nike.driver.current_url)

    logger.info("Logging in to Nike...")
    nike.loginToNike(config.Email, config.Password)

    time.sleep(10)
    logger.info("...Logged in to Nike")
    logger.info(nike.driver.title)
    logger.info(nike.driver.current_url)

    logger.info("Waiting for tweet...")
    shoeURL = get_desired_url()
    # shoeURL = "http://store.nike.com/us/en_us/pd/air-jordan-11-retro-three-quarter-shoe/pid-782484/pgid-720807?cp=usns_twit_122113_jordan_retro11"
    logger.info("...Got the tweet")
    logger.info(nike.driver.title)
    logger.info(nike.driver.current_url)

    logger.info("Opening shoe page...")
    nike.navigate(shoeURL)
    logger.info("...Opened shoe page")
    logger.info(nike.driver.title)
    logger.info(nike.driver.current_url)

    logger.info("Selecting Size and Adding To Cart...")
    if nike.select_size_and_add_to_cart(config.Size):
        logger.info("...Size selected and added to cart")
    time.sleep(5)
    logger.info(nike.driver.title)
    logger.info(nike.driver.current_url)

    logger.info("Quitting")
    nike.destroy()

except:
    logger.exception(sys.exc_info())