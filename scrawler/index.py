from bs4 import BeautifulSoup
import csv
import requests
import re
import websocket
from flask import Flask,request,render_template

import json

app = Flask(__name__)
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')



def scrape(next_page_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(next_page_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def getUrls(url):
    soup = scrape(url)
    links = soup.select('a')
    tempList = []
    for link in links:
        tempList.append(formatLink(link["href"]))
    return tempList

def formatLink(link):
    if(link[0] == "/" ):
        link=url+link
        return link
    return link


def scrawl(link,max):
    print link
    siteLink = link
    list= []
    count = 0
    while(len(list)<max):
        list.extend(getUrls(link))
        res = len(list)
        print len(list)
        link = list[count]
        if(link == siteLink):
            link = list[count+1]
            count+=1
    print len(list)
    return list[:max]

res = '0'

from flask import Flask
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def getFileCount():
    return res

@app.route('/scrawl/<version>/<link>',methods=['GET','POST'])
@crossdomain(origin='*')
def response(version,link):
    # return version+'://'+link
    list = scrawl(version+'://'+link,100)
    response = Flask.jsonify(list)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    # return json.dumps(list)
    # print "sd"
    # return "ssd"

if __name__ == '__main__':
    url = 'https://ikman.lk/'
    max = 500
    app.run()


# print scrawl(url)