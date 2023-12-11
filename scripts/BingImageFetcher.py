"""
Author: Hang Yan
Date created: 2023/10/14
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
driver = webdriver.Chrome(executable_path=chrome_driver_path)

r = redis.Redis(host="127.0.0.1", port=6379)
img_list = 'IMG_URL_LIST'


def scrape_images_from_bing(query, page_num):
    base_url = "https://www.bing.com/images/search?q={query}&first={page_num}"

    # 循环处理多个页面
    for page in range(page_num):
        url = base_url.format(query=query, page_num=page)
        driver.get(url)

        driver.implicitly_wait(1)

        # 获取页面内容
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        imgpt_div = soup.find('div', class_='dg_b isvctrl')
        a_tags = imgpt_div.find_all('a')

        for a_tag in a_tags:
            href = a_tag['href']  # 获取href属性值

            current_url = f"https://www.bing.com{href}"
            print(current_url)
            position = r.lpos(img_list, current_url)
            if position is None:
                r.lpush(img_list, current_url)
            else:
                print(f"值 '{current_url}' 在Redis列表中，位置为 {position}")

            # current_soup = BeautifulSoup(current_html_content, 'html.parser')
            #
            # mainContainer_div = current_soup.find('div', class_='mainContainer')  # 查找class为mainContainer的div
            # img_tag = mainContainer_div.find('img')  # 查找img标签
            #
            # src = img_tag['src']  # 获取src属性值
            # print(src)

    # 返回图片URL列表


if __name__ == "__main__":
    query = "户口本"
    page_num = 40
    result = scrape_images_from_bing(query, page_num)
    print(result)

    # 关闭浏览器
    driver.quit()