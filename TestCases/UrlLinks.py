from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests

req = Request("https://shop.greatergoods.com/")
pages = urlopen(req)

soup = BeautifulSoup(pages, 'lxml')
links = []

for link in soup.findAll('a'):
    links.append(link.get("href"))

print(links)




