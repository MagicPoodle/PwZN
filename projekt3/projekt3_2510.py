import json
import argparse
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Description")
parser.add_argument('-filename', help='name of file with data ', type=str, default='web_data')
args = parser.parse_args()

web = requests.get('http://www.psianiol.org.pl/adopcje?species=d')
data = []

soup = BeautifulSoup(web.text, 'html.parser')
print(soup.title.text)
first_class = soup.find('div', id='Content')
second_class = first_class.find_all('div', class_='Animal')

with open(f"{args.filename}.json", "w", encoding="utf-8") as file:
    for attributes in second_class:
        animal_name1 = attributes.find('td', class_="Name")
        animal_name2 = animal_name1.find('a').text
        page = animal_name1.find('a')['href']
        features1 = attributes.find('td', class_="Status").text.strip()
        data.append(json.dumps([animal_name2, page, features1], ensure_ascii=False, indent=4))
    json.dump(data, file, ensure_ascii=False, indent=4)

with open(f"{args.filename}.json", "r", encoding="utf-8") as data:
    print(json.dumps(json.loads(data.read()),ensure_ascii=False, indent=4))