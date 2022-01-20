# get_shop_list gets shop list from shopishop

import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

today = date.today()
d = today.strftime("%y%m%d")

class ShopiScraper():

    def __init__(self, keyword, root_domain, max_page):
        self.keyword = keyword
        self.domain_url = root_domain
        self.page_limit = int(max_page) + 1
        self.pages = range(1, self.page_limit)
        self.shop_list = [["rank", "store_url", "title", "alexa"]]
        self.store_url_list = []
        self.page_url = []
        self.rank = []
        self.store_url = []
        self.title = []
        self.alexa = []

    def get_shops(self):
        for i in self.pages:
            self.page_url = self.domain_url + str(i)
            self.page = requests.get(self.page_url)
            self.soup = BeautifulSoup(self.page.content, "html.parser")
            self.results = self.soup.find(id = "content-container-tbl")
            self.shop_elems = self.results.find_all("tr")
            for shop_elem in self.shop_elems:
                shop_details = shop_elem.find_all("td")
                for shop_detail in shop_details:
                    tag = "<td data-title=\"Rank\">"
                    if str(shop_detail).startswith(tag):
                        start_position = len(tag)
                        end_postion = int(str(shop_detail).find("<", start_position))
                        self.rank = str(shop_detail)[start_position:end_postion]
                    else:
                        tag = "<td data-title=\"Store Address\">"
                        if str(shop_detail).startswith(tag):
                            start_position = len(tag) + 10
                            end_postion = int(str(shop_detail).find("\"", start_position))
                            self.store_url = str(shop_detail)[start_position:end_postion]
                        else:
                            tag = "<td data-title=\"Title\">"
                            if str(shop_detail).startswith(tag):
                                start_position = len(tag) + 19
                                end_postion = int(str(shop_detail).find("<", start_position))
                                self.title_str = str(shop_detail)[start_position:end_postion]
                                self.title = self.title_str.strip()
                            else:
                                tag = "<td class=\"numeric\" data-title=\"Alexa Rank\">"
                                if str(shop_detail).startswith(tag):
                                    start_position = len(tag)
                                    end_postion = int(str(shop_detail).find("<", start_position))
                                    self.alexa_str = str(shop_detail)[start_position:end_postion]
                                    self.alexa = self.alexa_str.strip()
                                else: continue
                                details = [self.rank, self.store_url, self.title, self.alexa]
                                url = [self.store_url]
                                self.shop_list.append(details)
                                self.store_url_list.append(url)
                                print(details)

    def create_shop_file(self):
        with open(f"{self.keyword}_best_shops_{d}.csv", "a", newline = '') as file:
            writer = csv.writer(file)
            writer.writerows(self.shop_list)
        file.close()

    def create_store_url_list(self):
        with open(f"{self.keyword}_store_url_list_{d}.csv", "a", newline = '') as file:
            writer = csv.writer(file)
            writer.writerows(self.store_url_list)
        file.close()

shopi = ShopiScraper("jewelry", "https://www.shopistores.com/shopify-jewelry-stores/", "167")
shopi.get_shops()
shopi.create_shop_file()
shopi.create_store_url_list()
