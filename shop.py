# from ws1 import ShopifyScraper
from ws1_v2 import ShopifyScraper

list = []

file = open("jewelry_store_url_list_210510.csv", "r")
txt = file.read()
list = txt.split("\n")
file.close()

for (i) in list[378:]:
    try:
        x = ShopifyScraper(i)
        x.get_products()
        x.create_products_file()
        x.create_variants_file()
        print(x.name)
    except Exception:
        print(f"{x.name} ---------- ERROR, File not produced.")
        pass
