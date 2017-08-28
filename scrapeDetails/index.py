from bs4 import BeautifulSoup
import csv
import requests
import re

def scrape(next_page_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(next_page_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def getDetailsInPage(url):
    soup = scrape(url)
    total = int(soup.find('div',{'class':'listings-title'}).find('h1').text.split(" ")[0][0:-1])+1
    print total
    if(total>100):
        total =100
    for i in range(1,101):
        j = str(i)
        link = url+'&page='+j
        soup = scrape(link)
        divs = soup.findAll('div',{'class':'local-listing'})
        for div in divs:
            name = div.find('h2').find('a').text
            number = div.find('a', {'class': 'number'})
            if(number != None):
                number = number.text
            else:
                number=''
            address = div.find('span',{'class':'address'}).text
            print '"'+name+'"'+","+'"'+number+'"'+","+'"'+address+'"'
url = "https://tel.local.ch/en/q?what=y&where="
url1 = "https://tel.local.ch/en/q?what=z&where="

getDetailsInPage(url)
getDetailsInPage(url1)

