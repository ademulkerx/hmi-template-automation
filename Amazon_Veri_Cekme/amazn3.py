from asyncio.windows_events import NULL
from itertools import count
from pickle import NONE, TRUE
from random import betavariate
from bs4 import BeautifulSoup
from email import header
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOption
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import re
from selenium.webdriver.common.keys import Keys
from soupsieve import select_one
import requests
"""ip = requests.get('https://api.ipify.org').content.decode('utf8')
if (str(ip) == "188.132.202.235"):
    None
else:
    exit()"""
chrome_options = chromeOption()
py = input("Proxy Giriniz : ")
# "45.199.132.32:3128"
#192.177.142.16:3128
#alivelionyedixx@gmail.com:253932
chrome_options.add_argument('--proxy-server=%s' % py)
driver_path ='chromedriver.exe'
uruns = []
uruns1 = []

ara = input("Arama Değeri Giriniz : ")

ara = ara.replace(" ","+")
driver = webdriver.Chrome( driver_path,options=chrome_options)

driver.delete_all_cookies()
driver.get(f"https://www.amazon.com.tr/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com.tr%2Fref%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=trflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&")
input("Lüten Giriş yapıp birşeyler yazın : ")
time.sleep(3)
driver.get(f"https://www.amazon.com.tr/s?k={ara}")
time.sleep(3)
driver.get(f"https://www.amazon.com.tr/s?k={ara}")
me = "sa"
link = f"https://www.amazon.com.tr/s?k={ara}"
while (me == "sa"):
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        if(soup.select_one("body > center > p > table > tbody > tr > td > h2").text == "Üzgünüz"):
            me = "sa"
    except:
            me="sa1"
soup = BeautifulSoup(driver.page_source, 'html.parser')

a=1
while(TRUE):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if not soup.find('a',class_="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"):
        break
    else:
        nextpge = soup.find('a',class_="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator")
    driver.get("https://www.amazon.com.tr"+str(nextpge.get("href")))
    a=a+1
print(str(a) + " TANE SAYFA BULUNDU")
b=1
while(b <= a):
    driver.get(f"https://www.amazon.com.tr/s?k={ara}&page={b}&crid=23C9S6Q3GU4PE&sprefix=role%2Caps%2C195&ref=nb_sb_noss_2")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    sear = soup.find_all('a',class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
    z = 1
    for i in sear:
        links = i.get("href")
        uruns.append(links)
        z = z + 1 
    print(str(z)+" TANE ÜRÜN BULUNDU")
    b = b+1
for i in uruns:
    driver.get(f"https://www.amazon.com.tr{i}")
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        te1 = re.findall('(/dp/?\S+/)', i)
        te1 = te1[0].replace("/dp/","")
        te1= te1.replace("/","")
        asin = te1
    except:
        asin = NULL
    try:
        te = soup.select_one('#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span > span.a-offscreen').text
        te.replace(' ',"")
        amznfyt= te
    except:
        try:
            te = soup.select_one('#sns-base-price').text
            te.replace(' ',"")
            amznfyt= te
        except:
            amznfyt = NULL
    
    link = f"https://www.amazon.com.tr{i}"
    if(link != NULL and asin != NULL and amznfyt != NULL  ):
        b = []
        b.append(link)
        b.append(asin)
        b.append(amznfyt)
        uruns1.append(b)

student_header = ['amazntr_link', 'asin', 'amzntrfyt']
with open('urunlers.csv', 'w') as file:
    writer = csv.writer(file,delimiter=";")
    writer.writerow(student_header)
    # Use writerows() not writerow()
    writer.writerows(uruns1)
