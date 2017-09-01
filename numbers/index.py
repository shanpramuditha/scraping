from bs4 import BeautifulSoup
import csv
import requests
import re

def scrape(next_page_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(next_page_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def scrapeList(soup):
    list = soup.select('li.cntanr')
    for item in list:
        getDetails(item["data-href"])

def getDetails(link):
    soup = scrape(link)
    name = soup.find('span',{'class':'fn'}).text
    address = soup.select('span.adrstxtr > span > span')[0].text
    numbers = soup.select('div.telCntct > a.tel')
    numberList = []
    # print name
    for num in numbers:
        numberList.append(num.text)
    # numberList = set(numberList)
    # print numberList
    print "'"+name+"','"+address+"','"+numberList[0]+"','"+numberList[1]+"'"
scrapeList(scrape("https://www.justdial.com/Delhi-NCR/AC-Repair-Services/nct-10890481/page-4"))
# getDetails("https://www.justdial.com/Delhi/Vipin-Raj-Enterprises--Ganga-Vihar/011PX124-X124-110501164632-Y8U6_BZDET?xid=RGVsaGkgQUMgUmVwYWlyIFNlcnZpY2Vz&tab=gallery")