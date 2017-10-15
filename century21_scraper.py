"""
Scraper for Century21.com.
"""
import time
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Century21Scraper(object):
    def __init__(self):
        self.url = "http://www.century21.com"
        self.driver = webdriver.Chrome()

    def scrape(self, city):
        self.driver.get(self.url)
        el = self.driver.find_element(By.ID, 'searchText')
        el.send_keys(city)
        el.send_keys(Keys.RETURN)
        l = []
        wait = WebDriverWait(self.driver, 10)
        while True:
            time.sleep(10)
            elem = wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))
            button = self.driver.find_element(By.ID, 'filter-sort-order')
            button.click()
            elem.send_keys(Keys.PAGE_DOWN)
            no_of_pagedowns = 34
            while no_of_pagedowns:
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(1.3)
                no_of_pagedowns -= 1
            soup = BeautifulSoup(self.driver.page_source, "html5lib")
            elements = soup.find_all("div", {"class": "property-card-primary-info"})
            for item in elements:
                d = {}
                try:
                    d["Price"] = item.find("a", {"class": "listing-price"}).text.replace("\n", "").replace(" ", "")
                except:
                    d["Price"] = None
                try:
                    d["Beds"] = item.find("div", {"class": "property-beds"}).text.replace("\n", "").replace(" ", "")
                except:
                    d["Beds"] = None
                try:
                    d["Baths"] = item.find("div", {"class": "property-baths"}).text.replace("\n", "").replace(" ", "")
                except:
                    d["Baths"] = None
                try:
                    d["Sqft"] = item.find("div", {"class": "property-sqft"}).text.replace("\n", "").replace(" ", "")
                except:
                    d["Sqft"] = None
                try:
                    d["Address"] = item.find("div", {"class": "property-address"}).text.replace("\n", "").replace(" ",
                                                                                                                  "")
                except:
                    d["Address"] = None
                try:
                    d["City"] = item.find("div", {"class": "property-city"}).text.replace("\n", "").replace(" ", "")
                except:
                    d["City"] = None
                l.append(d)

                df = pd.DataFrame(l)
                df.to_csv("Output.csv")
            try:
                element = self.driver.find_element_by_id('pagination-next')
                element.click()
            except NoSuchElementException:
                break
        self.driver.close()

if __name__ == '__main__':
    scraper = Century21Scraper()
    # enter the city, comma, abbreviation of the state
    scraper.scrape('San Diego, CA')
