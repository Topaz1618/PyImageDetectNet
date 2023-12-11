"""
Author: Hang Yan
Date created: 2023/10/15
Email: topaz1668@gmail.com

This code is licensed under the GNU General Public License v3.0.
"""

import requests
import redis
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # 启用无界面模式

chrome_driver_path = '/opt/homebrew/bin/chromedriver'
# driver = webdriver.Chrome(executable_path=chrome_driver_path)

r = redis.Redis(host="127.0.0.1", port=6379)
img_list = 'IMG_URL_LIST'


def save_image():
    elements = r.lrange(img_list, 0, -1)

    idx = 0
    for element in elements:
        print(element)
        idx += 1

    print("所有 URL", idx)


def main_url_looper():
    elements = r.lrange(img_list, 0, -1)

    idx = 0
    for element in elements:
        print(element)
        idx += 1

        respone = requests.get(element)
        html_content = respone.text
        soup = BeautifulSoup(html_content, "html.parser")


        mainContainer_div = soup.find('div', class_='mainContainer')
        print(mainContainer_div)


def main():

    main_url_looper()
    # save_image()


if __name__ == "__main__":
    main()

    # 关闭浏览器
    # driver.quit()