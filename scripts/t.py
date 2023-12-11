"""
Author: Hang Yan
Date created: 2023/10/14
Email: topaz1668@gmail.com

This code is licensed under the GNU General Public License v3.0.
"""
import requests
from bs4 import BeautifulSoup
import re

# 发送HTTP请求获取页面内容
url = "https://www.bing.com/images/search?q=户口本&width=300&height=300"
response = requests.get(url)
html_content = response.text

# 使用BeautifulSoup解析页面内容
soup = BeautifulSoup(html_content, "html.parser")

# 找到所有图片元素
image_elements = soup.find_all("img")

# 筛选出宽度和高度大于300的图片
filtered_images = []
for img in image_elements:
    print(img)
    width = img.get("width")
    height = img.get("height")
    print(width, height)

# 打印筛选结果
for img_url in filtered_images:
    print(img_url)