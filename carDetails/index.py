from bs4 import BeautifulSoup
import csv
import requests
import re
import MySQLdb
import httplib2
import os
import time
from apiclient import discovery
# from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
from gdrive import get_service,uploadFileToFolder,getIDfromName,shareFileWithEmail
from sqlite import setup,insertImage,isImageAvailable
import cssutils
import urllib



baseLink = 'https://www.goauto.com.au'
baseFolder = ''
def scrape(next_page_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(next_page_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def scrapeCarReviews():
    url = 'https://www.goauto.com.au/car-reviews.html'
    first = False
    end = False
    results = []
    temp = scrapeCarLinks(scrape(url))

    results.extend(temp[0])
    nextLink = temp[1]
    while(end == False):
        if not first and not end:
            first = True
            url = baseLink+nextLink[0].find('a')['href']

        elif (first) and (not end) :
            if len(nextLink) ==1:
                end = True
                break
            else:
                url = baseLink+nextLink[0].find('a')['href']

        temp = scrapeCarLinks(scrape(url))
        results.extend(temp[0])
        nextLink = temp[1]
    for result in results:
        print extractImage(baseLink+result['href'])

def scrapeCarNew():
    url = 'https://www.goauto.com.au/new-models.html'
    first = False
    end = False
    results = []
    temp = scrapeCarLinks(scrape(url))

    results.extend(temp[0])
    nextLink = temp[1]
    while(end == False):
        if not first and not end:
            first = True
            url = baseLink+nextLink[0].find('a')['href']

        elif (first) and (not end) :
            if len(nextLink) ==1:
                # print end
                end = True
                # print end
                break
            else:
                url = baseLink+nextLink[0].find('a')['href']
        # print end
        # print url
        temp = scrapeCarLinks(scrape(url))
        results.extend(temp[0])
        nextLink = temp[1]
    # print len(results)

def scrapeCarFuture():
    url = 'https://www.goauto.com.au/future-models.html'
    first = False
    end = False
    results = []
    temp = scrapeCarLinks(scrape(url))

    results.extend(temp[0])
    nextLink = temp[1]
    while(end == False):
        if not first and not end:
            first = True
            url = baseLink+nextLink[0].find('a')['href']

        elif (first) and (not end) :
            if len(nextLink) ==1:
                # print end
                end = True
                # print end
                break
            else:
                url = baseLink+nextLink[0].find('a')['href']
        # print end
        # print url
        temp = scrapeCarLinks(scrape(url))
        results.extend(temp[0])
        nextLink = temp[1]
    # print len(results)

def scrapeCarNews():
    url = 'https://www.goauto.com.au/news.html'
    first = False
    end = False
    results = []
    temp = scrapeCarLinks(scrape(url))

    results.extend(temp[0])
    nextLink = temp[1]
    while(end == False):
        if not first and not end:
            first = True
            url = baseLink+nextLink[0].find('a')['href']

        elif (first) and (not end) :
            if len(nextLink) ==1:
                # print end
                end = True
                # print end
                break
            else:
                url = baseLink+nextLink[0].find('a')['href']
        # print end
        # print url
        temp = scrapeCarLinks(scrape(url))
        results.extend(temp[0])
        nextLink = temp[1]
    # print len(results)

def scrapeCarLinks(soup):
    mainDiv = soup.find('div',{'id':'article_most_recent'})
    # print mainDiv
    # exit(0)
    subDiv = mainDiv.select('div > div > a[alt=""]')
    images = subDiv[0:-1]
    nextLink = mainDiv.select('div > div.abutton')
    return [subDiv,nextLink]

def scrapeNewModelLinks(soup):
    mainDiv = soup.find('div', {'id': 'more_future_models'})
    # print mainDiv
    # exit(0)
    subDiv = mainDiv.select('div > div > a[href^="/new-models/"]')
    images = subDiv[0:-1]
    nextLink = mainDiv.select('div > div.abutton')
    return [subDiv, nextLink]

def scrapeFutureModelLinks(soup):
    mainDiv = soup.find('div', {'id': 'more_future_models'})
    # print mainDiv
    # exit(0)
    subDiv = mainDiv.select('div > div > a[href^="/future-models/"]')
    images = subDiv[0:-1]
    nextLink = mainDiv.select('div > div.abutton')
    return [subDiv, nextLink]

def scrapeNewsModelLinks(soup):
    mainDiv = soup.find('div', {'id': 'more_future_models'})
    # print mainDiv
    # exit(0)
    subDiv = mainDiv.select('div > div > a[href^="/news/"]')
    images = subDiv[0:-1]
    nextLink = mainDiv.select('div > div.abutton')
    return [subDiv, nextLink]

def extractImage(link):
    soup = scrape(link)
    image = soup.find('img',{"id":"article_bottom_image"})
    if(image == None):
        image = soup.select('div#article_t')[0]['style']
        style = cssutils.parseStyle(image)
        url = style['background-image']
        image = url.replace('url(', '').replace(')', '')
        # print image
        # exit(0)
    else:
        image=image["src"]
    # print image
    # exit(0)
    # print baseLink+image
    return [baseLink+image,link.split('/')[3:5]]

def saveImage(result):
    folder = ""
    image = result[0]
    category = result[1][0]
    type = result[1][2]
    fileName = result[1][3]+'-'+result[1][4]+'-'+result[1][5]+'.jpg'
    if(isImageAvailable(image)):
        return 0
    else:
        insertImage(image,fileName)


    # uploadFileToFolder(service=service, folderID=folder, fileName=fileName)

def setBaseFolder():
    name = 'images'

def downloadImage(imageLink,imageName):
    urllib.urlretrieve(imageLink,'images/'+imageName)

# test = scrapeNewsModelLinks(scrape('https://www.goauto.com.au/news.html'))

# image = extractImage("https://www.goauto.com.au/car-reviews/mercedes-benz/glc-coupe/250d/2017-03-23/27146.html")
service = get_service()
# uploadFileToFolder(service=service, folderID='0B7Kfv7Ef2210SDZaR3lDZWFLRkE', fileName='image.jpg')
# scrapeCarReviews()
# print extractImage('https://www.goauto.com.au/car-reviews/mercedes-benz/glc-coupe/250d/2017-03-23/27146.html')
image = 'testing.jpg'
downloadImage('https://www.goauto.com.au/assets/contents/925b256b5dea3626ae7f0471dade0a166c54e33f.jpg',image)
uploadFileToFolder(service,'0B_0E4HVtROqicmV5bWVXektQcDg',image)