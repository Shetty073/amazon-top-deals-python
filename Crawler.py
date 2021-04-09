from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep
from sys import exc_info, exit
import re


class Crawler:
    def __init__(self, product_name, store):
        self.product_name = product_name
        self.store = store
        option = webdriver.ChromeOptions()
        option.add_argument("--incognito")
        option.add_argument("headless")
        # create a new instance of chrome
        self.browser = webdriver.Chrome(executable_path="./driver/chromedriver.exe", options=option)
        # wait 10 seconds for page to load TODO: set this timeout according to the user's internet speed
        self.timeout = 10
        # a dictionary to store crawling results
        self.products = {}
        # last page initialized to 0
        self.last_page = 0

    def __crawl(self):
        url = ("https://www.amazon.%s/" %self.store)
        self.browser.get(url)
        try:
            WebDriverWait(self.browser, self.timeout).until(
                ec.visibility_of_element_located((By.ID, "twotabsearchtextbox")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            print("Url: '%s' Is this correct? Change store extension or try again later" %url)
            self.browser.quit()
            exit(0)

        # show only products with 4 stars and up
        searchbar_element = self.browser.find_element_by_id("twotabsearchtextbox")
        searchbar_element.click()
        searchbar_element.send_keys(self.product_name)
        searchbar_element.send_keys(Keys.ENTER)
        review_list = self.browser.find_elements_by_tag_name("li")

        # Select only products with 4 stars and up (doesn't work for not english stores)
        for x in review_list:
            if x.text == "& Up":
                x.click()
                break
        sleep(6)
        try:
            self.last_page = int(self.browser.find_elements_by_css_selector("li[class='a-disabled']")[1].text)
        except Exception as e:
            self.last_page = int(self.browser.find_elements_by_css_selector("li[class='a-normal']")[-1].text)

        i = 0
        try:
            for _ in range(1, self.last_page): 
                sleep(4)
                search_pg = self.browser.find_elements_by_css_selector(
                    "div[class='s-main-slot s-result-list s-search-results sg-row']")
                search_res = search_pg[0].find_elements_by_css_selector(
                    "div[class='s-expand-height s-include-content-margin s-border-bottom s-latency-cf-section']")
                if len(search_res) < 2:
                    search_res = search_pg[0].find_elements_by_css_selector(
                        "div[class='s-include-content-margin s-border-bottom s-latency-cf-section']")
                for d in search_res:
                    item_name = d.find_elements_by_css_selector("a[class='a-link-normal a-text-normal']")[0]
                    self.products[i] = {"name": item_name.text, "link": item_name.get_attribute("href")}
                    try:
                        og_price = d.find_elements_by_css_selector("span[class='a-price a-text-price']")[0].text
                    except IndexError as ie:
                        print("Warning: %s for original price (no price)" %ie)
                        og_price = "0.0"
                    try:
                        curr_price = d.find_elements_by_css_selector("span[class='a-price']")[0].find_elements_by_css_selector("span[class='a-offscreen']")[0].get_attribute('innerHTML') 
                    except IndexError as ie:
                        print("Warning: %s for current price (no price)" %ie)
                        curr_price = "0.0"
                    if og_price != "0.0":
                        og_price = re.search("(\d+[,]*[.]*\d*)", og_price).group()
                    if curr_price != "0.0":
                        curr_price = re.search("(\d+[,]*[.]*\d*)", curr_price).group()
                    
                    self.products[i]["og_price"] = float(str(og_price).replace(",", "."))
                    self.products[i]["curr_price"] = float(str(curr_price).replace(",", "."))
                    self.products[i]["price_diff"] = round(self.products[i]["og_price"] - self.products[i]["curr_price"],2)
                    
                    i += 1
                next_page = self.browser.find_elements_by_css_selector("li[class='a-last']")[0]
                next_page.click()
            
        except Exception as e:
            tb = exc_info()[2]
            print(e.with_traceback(tb))

        with open("results.txt", "w", encoding="utf-8") as f:
            for k in self.products.values():
                f.write(str(k))

    def get_best_deal(self):
        self.__crawl()
        temp = {}
        for k, v in self.products.items():
            if "price_diff" in v.keys():
                temp[k] = v["price_diff"]
        # sort the self.products keys in the descending order of "price_diff"
        temp = [k for k, v in sorted(temp.items(), key=lambda item: item[1], reverse=True)]
        
        # Debug: printing results
        with open("results_sorted.txt", "w", encoding="utf-8") as f:
            f.write(str([self.products[x] for x in temp if self.products[x]["price_diff"] > 0]))
    
        # Get the top 5 deals
        temp = temp[0: 5]

        # print the top 5 deals
        return [self.products[x] for x in temp]
