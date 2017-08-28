from bs4 import BeautifulSoup
import csv
import requests
import re

productsArray = []

def extractProductDetails(url,category):
    soup = scrape(url)
    name = soup.find('h1',{'class':'entry-title'}).text.encode('utf8')
    descriptionDiv = soup.find('div',{'class':'product-excerpt'})
    brand = soup.find('div',{'class':'summary'}).text.split(':')[-1].encode('utf8').strip()
    # print brand
    price = soup.find('a',{'class':'tcf-price-rating'})
    if(price != None):
        price = str(len(price.text)).encode('utf8')
    else:
        price = ""
    description = ""
    images = ""
    imagesList = soup.find('div',{'class':'caroufredsel-wrap'}).findAll('img')
    # print len(imagesList)
    for image in imagesList:
        images+=image['src'].encode('utf8') +' | '
    # print images
    if(descriptionDiv != None):
        for p in descriptionDiv.findAll('p'):
            description+= p.text.encode('utf8')
    description = unicode(description,'utf-8')
    resultList = [name,description,category,brand,price,images]
    # response = "%s" for x in resultList
    print '"' + name + '"' + "," + '"' + description + '"' + "," + '"' + category + '"'+"," + '"' + brand + '"'+"," + '"' + price + '"'+"," + '"' + images + '"'
    # return response

def getProductListFromPage(url):
    soup = scrape(url)
    products = soup.findAll('div',{'class':'product-images'})
    links = []
    for product in products:
        links.append(product.find('a')['href'])
    return links




def scrape(next_page_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(next_page_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


soup = scrape("http://www.topcarpetsandfloors.co.za/")
productList = soup.find('li',{'id' : 'menu-item-8136'})
productMenu = productList.find('ul')
productCategories = productMenu.findAll('li')
totalProducts = 0
links = []
for category in productCategories:
    links = []
    link =  category.find('a')['href']
    # print link
    soup = scrape(link)
    lastIndex = soup.findAll('a',{'class':'page-numbers'})
    # print link

    if(len(lastIndex)>0):
        lastIndex =int(lastIndex[-2].text)
        for i in xrange(1,lastIndex+1):
            currentLink = link+'page/'+str(i)+'/'
            links.extend(getProductListFromPage(currentLink))
            print currentLink
            print len(getProductListFromPage(currentLink))

    else:
        links.extend(getProductListFromPage(link))
        print link
        print len(getProductListFromPage(link))
        # print "no"
    print lastIndex
    print(len(links))
    category = link.split('/')[-2]
    for link in links:
        # print (link)
        data = extractProductDetails(link.strip(),category)
        # file = open("myfile.csv", "wb")
        # out = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
        # out.write(data)
        # print data
        # exit(0)
    # exit(0)
# print totalProducts
# print extractProductDetails("http://www.topcarpetsandfloors.co.za/product/avant-garde/","category")
print len(getProductListFromPage("http://www.topcarpetsandfloors.co.za/products/laminates/page/5/"))