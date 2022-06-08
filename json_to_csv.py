import json
import csv
from bs4 import BeautifulSoup

JSON = json.load(open("./posts.json", "r+", encoding="utf-8"))

data_dict = []

for item in JSON:
    content = []
    content_soup = BeautifulSoup(item["content"]["rendered"], features="html.parser")
    for i in content_soup.find_all("p", attrs={"class": "more"}):
        i.decompose()

    content.append(str(content_soup))

    item_dict = {}
    item_dict["title"] = BeautifulSoup(
        item["title"]["rendered"], features="html5lib"
    ).get_text()
    item_dict["content"] = "".join(content)
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
