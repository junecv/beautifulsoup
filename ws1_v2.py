# ws1 turns products.json to prouduct_list per shop
# to be updated: breaks variants into list items

import requests
import csv
from sys import argv
from datetime import date

today = date.today()
d = today.strftime("%y%m%d")

class ShopifyScraper:

    def __init__(self, root_domain):
        self.domain_url = root_domain
        self.product_list_url = self.domain_url + "/products.json?limit=1000"
        self.product_list = [["idx", "title", "full_url", "desc", "created_date", "publish_date", "updated_date", "vendor", "product_type", "tags", "img"]]
        self.variant_list = [["shop_name","vari_idx", "vari_sku", "vari_avilable", "vari_price", "vari_product_id", "vari_created_date", "vari_updated_date"]]
        if str(self.domain_url).startswith("https://www."):
            self.start_position = 12
            # self.start_position = int(str(self.domain_url).find(".")) + 1
            # self.end_postition = int(str(self.domain_url).find(".", self.start_position))
            # self.name = str(self.domain_url)[self.start_position:self.end_postition]
        else:
            self.start_position = 8
        self.end_postition = int(str(self.domain_url).rfind(".", self.start_position))
        self.name = str(self.domain_url)[self.start_position:self.end_postition]

    def get_products(self):
        self.fetch_products = requests.get(self.product_list_url)
        products = self.fetch_products.json()["products"]
        for i in products:
            idx = i["id"]
            title = i["title"]
            slug = i["handle"]
            desc = i["body_html"]
            publish_date = i["published_at"]
            created_date = i["created_at"]
            updated_date = i["updated_at"]
            vendor = i["vendor"]
            product_type = i["product_type"]
            tags = i["tags"]
            variants = i["variants"]
            for j in variants:
                vari_idx = j["id"]
                vari_sku = j["sku"]
                vari_avilable = j["available"]
                vari_price = j["price"]
                vari_product_id = j["product_id"]
                vari_created_date = j["created_at"]
                vari_updated_date = j["updated_at"]
                vari_details = [self.name, vari_idx, vari_sku, vari_avilable, vari_price, vari_product_id, vari_created_date, vari_updated_date]
                self.variant_list.append(vari_details)
            img = i["images"]
            full_url = self.domain_url + "/products/" + slug
            details = [idx, title, full_url, desc, created_date, publish_date, updated_date, vendor, product_type, str(tags), str(img)]
            self.product_list.append(details)

    def create_products_file(self):
        with open("/Users/jc/code/ws/product_list/" + f"{self.name}_product_list.csv", "w", newline = '') as file:
            writer = csv.writer(file)
            writer.writerows(self.product_list)
        file.close()

    def create_variants_file(self):
        with open("/Users/jc/code/ws/product_list/" + f"{self.name}_variant_list.csv", "w", newline = '') as file:
            writer = csv.writer(file)
            writer.writerows(self.variant_list)
        file.close()
