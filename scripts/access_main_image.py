"""
Author: Hang Yan
Date created: 2023/10/15
Email: topaz1668@gmail.com

This code is licensed under the GNU General Public License v3.0.
"""
from time import sleep, time

import requests
import asyncio


from pyppeteer import launch
from requests_html import HTMLSession


from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# options = Options()
# options.add_argument("--headless")  # 启用无界面模式
#
# prefs = {"profile.managed_default_content_settings.images": 2}
# options.add_experimental_option("prefs", prefs)
#
# chrome_driver_path = '/opt/homebrew/bin/chromedriver'
# driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
#
# url = "https://www.bing.com/images/search?view=detailV2&ccid=OGRK1joe&id=14668FF502B336A070CACE665B8C031790DC865E&thid=OIP.OGRK1joe0ly3bJIAEr-TGgHaFj&mediaurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.38644ad63a1ed25cb76c920012bf931a%3frik%3dXobckBcDjFtmzg%26riu%3dhttp%253a%252f%252fphotocdn.sohu.com%252f20130701%252fImg380308454.jpg%26ehk%3diz0RZCkFsGwFhZd082dAP3dSivmpx8IcjzFtc9%252fSdKk%253d%26risl%3d%26pid%3dImgRaw%26r%3d0%26sres%3d1%26sresct%3d1%26srh%3d799%26srw%3d1066&exph=375&expw=500&q=%e6%88%b7%e5%8f%a3%e6%9c%ac&simid=608046651028878337&FORM=IRPRST&ck=5C73C7C2170AD8A5721A698368CAEAA3&selectedIndex=72"
#
# t0 = time()
# driver.get(url)
#
# html = driver.page_source
# with open('page.html', 'w', encoding='utf-8') as file:
#     file.write(html)


# 关闭浏览器驱动
# driver.quit()
# print(f"Cost time: {time() - t0}")# from selenium import webdriver
# # from selenium.webdriver.chrome.options import Options
# #
# # options = Options()
# # options.add_argument("--headless")  # 启用无界面模式
# #
# # prefs = {"profile.managed_default_content_settings.images": 2}
# # options.add_experimental_option("prefs", prefs)
# #
# # chrome_driver_path = '/opt/homebrew/bin/chromedriver'
# # driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
# #
# # url = "https://www.bing.com/images/search?view=detailV2&ccid=OGRK1joe&id=14668FF502B336A070CACE665B8C031790DC865E&thid=OIP.OGRK1joe0ly3bJIAEr-TGgHaFj&mediaurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.38644ad63a1ed25cb76c920012bf931a%3frik%3dXobckBcDjFtmzg%26riu%3dhttp%253a%252f%252fphotocdn.sohu.com%252f20130701%252fImg380308454.jpg%26ehk%3diz0RZCkFsGwFhZd082dAP3dSivmpx8IcjzFtc9%252fSdKk%253d%26risl%3d%26pid%3dImgRaw%26r%3d0%26sres%3d1%26sresct%3d1%26srh%3d799%26srw%3d1066&exph=375&expw=500&q=%e6%88%b7%e5%8f%a3%e6%9c%ac&simid=608046651028878337&FORM=IRPRST&ck=5C73C7C2170AD8A5721A698368CAEAA3&selectedIndex=72"
# #
# # t0 = time()
# # driver.get(url)
# #
# # html = driver.page_source
# # with open('page.html', 'w', encoding='utf-8') as file:
# #     file.write(html)
#
#
# # 关闭浏览器驱动
# # driver.quit()
# # print(f"Cost time: {time() - t0}")
#
#
# with open('page.html', 'r', encoding='utf-8') as file:
#     html = file.read()
# # # 处理网页内容，例如使用BeautifulSoup进行解析
# soup = BeautifulSoup(html, 'html.parser')
# a_tags = soup.find_all('div')
# print(a_tags)


with open('page.html', 'r', encoding='utf-8') as file:
    html = file.read()
# # 处理网页内容，例如使用BeautifulSoup进行解析
soup = BeautifulSoup(html, 'html.parser')
a_tags = soup.find_all('div')
print(a_tags)

# idx = 0
# for a_tag in a_tags:
#     print(idx, a_tag)
#     idx += 1


# 解析网页内容
# soup = BeautifulSoup(response.text, 'html.parser')
#
# 找到所有链接
# t = soup.find_all('div')
# print(t)

# a_tags = divs.find_all('a')

# # 输出链接
# for link in a_tags:
#     href = link.get('href')
#     print(href)

