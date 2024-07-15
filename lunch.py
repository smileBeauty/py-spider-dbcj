import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import csv
import mysql.connector
import uuid
import datetime
import os

domain = 'https://www.dufe.edu.cn/'
pattern = r'(\d{0,4}年?\d{1,2}月\d{1,2}日)'
pattern2 = r'联系人：(.*?)(?:，|$)'
csvHead = ['项目名称', '项目类型', '发布日期', '截止日期', '联系人', '网页链接']
folderName = 'csv'

if not os.path.exists(f"./{folderName}"):
    os.makedirs(f"./{folderName}")
    print(f"文件夹 '{folderName}' 不存在，已创建")
else:
    print(f"文件夹 '{folderName}' 已存在")

conn = mysql.connector.connect(host='', user='', password='', database='duang')
cursor = conn.cursor()
sql = "INSERT INTO spider (id, title, type, publishDate, endDate, contact, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"

class MyObj:
    def __init__(self, title, type, publishDate, endDate, contact, url):
        self.title = title
        self.type = type
        self.publishDate = publishDate
        self.endDate = endDate
        self.contact = contact
        self.url = url

def spider(url, xPath):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    root = etree.HTML(str(soup))
    elements = root.xpath(xPath)
    my_dict = {}
    for element in elements:
        a = element.find('a')
        href = a.get("href")
        detailUrl = f"{domain}{href}"
        detailResponse = requests.get(detailUrl)
        detailSoup = BeautifulSoup(detailResponse.text, 'lxml')
        detailRoot = etree.HTML(str(detailSoup))
        title = detailRoot.xpath('/html/body/div[5]/div/div[2]/div[1]')
        if (len(title)):
            title = title[0].text.strip().replace("关于组织", "").replace("关于", "").replace("工作的通知", "").replace("的通知", "")
        else:
            title = ''
        if '研讨会' in title or '实践' in title:
            continue
        type = detailRoot.xpath('/html/body/div[5]/div/div[1]/a[2]')
        if (len(type)):
            type = type[0].text.strip()
        else:
            type = ''
        publishDate = detailRoot.xpath('/html/body/div[5]/div/div[2]/div[2]')
        year = ''
        if (len(publishDate)):
            publishDate = publishDate[0].text.strip()
            year = publishDate.split('年')[0]
        else:
            publishDate = ''
        endDate = detailSoup.find_all(text=lambda text: text and '截止时间：' in text)
        if (len(endDate)):
            endDate = endDate[0].text.strip()
            endDate = re.findall(pattern, endDate)
            if (len(endDate)):
                if ("年" in endDate[0]):
                    endDate = endDate[0]
                else:
                    endDate = f"{year}年{endDate[0]}"
            else:
                endDate = ''
        else:
            endDate = ''
        contact = detailSoup.find_all(text=lambda text: text and '联系人：' in text)
        if (len(contact)):
            contact = contact[0].text.strip()
            contact = re.search(pattern2, contact)
            if contact:
                contact = contact.group(1)
            else:
                contact = ''
        else:
            contact = ''

        sotPublishDate = publishDate.replace("年", "").replace("月", "").replace("日", "")
        
        if not sotPublishDate in my_dict:
            my_dict[sotPublishDate] = []
        my_dict[sotPublishDate].append(MyObj(title, type, publishDate, endDate, contact, detailUrl))
    return my_dict



def writeFile(currentDict, filePath):
    for fileName in currentDict.keys():
        currentList = currentDict[fileName]
        csvData = [
            csvHead,
        ]
        for item in currentList:
            csvData.append([item.title, item.type, item.publishDate, item.endDate, item.contact, item.url])
            cursor.execute(sql, (str(uuid.uuid4()), item.title, item.type, datetime.datetime.strptime(item.publishDate, '%Y年%m月%d日'), datetime.datetime.strptime(item.endDate, '%Y年%m月%d日') if item.endDate else None, item.contact, item.url))
        
        with open(f"{filePath}/{fileName}.csv", 'w', encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csvData)

    conn.commit()

result = spider(f"{domain}/r_6.html", '/html/body/div[5]/div/div[2]/ul/*')
writeFile(result, f"./{folderName}")

cursor.close()

conn.close()

print('数据库数据插入成功')
