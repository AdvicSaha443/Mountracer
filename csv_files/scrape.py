""" This extracts the quotes submitted to typeracer.com from a third party website typeracerdata.com and quote's meta data from data.typeracer.com for the text_play.csv file """

from bs4 import BeautifulSoup
import requests
import time
import csv
import re

response = requests.get('https://www.typeracerdata.com/texts?texts=full&sort=relative_average')
soup = BeautifulSoup(response.content, 'html.parser')

print("all text data extracted")

with open('text_play.csv', "r", newline='', encoding="utf-8") as f: start = len(list(f)) + 1

content = soup.find_all('tr')
file_ = open('text_play.csv', "a", newline='', encoding="utf-8")
csv_writer = csv.writer(file_)

for i, con in enumerate(content[start:start+500]):
    try:
        val = con.find('a')
        textid = val['href'][9:]

        #obtaining author
        response2 = requests.get(f'https://data.typeracer.com/pit/text_info?id={textid}')
        soup2 = BeautifulSoup(response2.content, 'html.parser')
        # author = soup2.find('td').find('div', class_=False, id=False)
        meta_data = re.sub(r'\s+', ' ', (soup2.find('table', class_="textTable").find('div', class_=False, id=False).text.strip())).strip().split(" by ")

        csv_writer.writerow([i+start, str(val.text.strip()), meta_data[0], meta_data[1]])

        time.sleep(0.5)
        print(f"{start + i} Quotes Extracted!")
    except Exception as e:
        print(e)