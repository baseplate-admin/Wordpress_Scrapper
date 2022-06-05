import json
import csv
from bs4 import BeautifulSoup

JSON = json.load(open("./posts.json", "r+", encoding="utf-8"))

data_dict = []

for item in JSON:
    item_dict = {}
    item_dict["title"] = BeautifulSoup(
        item["title"]["rendered"], features="html5lib"
    ).get_text()
    item_dict["content"] = BeautifulSoup(
        item["content"]["rendered"], features="html5lib"
    ).get_text()
    data_dict.append(item_dict)

csv_file = open("test.csv", "w+")
csv_writer = csv.writer(csv_file)

count = 0
for item in data_dict:
    if count == 0:
        header = item.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(item.values())

csv_file.close()
