import os
import requests
import cv2
import numpy as np
from bs4 import BeautifulSoup

bing_images = list()


def download_image(url, directory, filename):
    response = requests.get(url)
    if response.status_code == 200:
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        file_path = os.path.join(directory, filename)
        cv2.imwrite(file_path, image)
        print(f"Saved: {file_path}")
    else:
        print(f"Failed to download image: {url}")

# def download_image(url, directory, filename):
#     response = requests.get(url)
#     if response.status_code == 200:
#         file_path = os.path.join(directory, filename)
#         with open(file_path, "wb") as file:
#             file.write(response.content)
#         print(f"Downloaded: {file_path}")
#     else:
#         print(f"Failed to download image: {url}")


def scrape_images_from_bing(query, page_num):
    url = f"https://www.bing.com/images/search?q={query}&qft=+filterui:imagesize-custom_320_320&form=IRFLTR&first=page_num"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_elements = soup.find_all('img')

    for img in image_elements:
        # print(type(img), img)
        img_dict = dict(img.attrs)

        width = img.get("width")
        height = img.get("height")
        if width < 500 or height < 380:
            continue

        if "src2" in img_dict:
            bing_images.append(img_dict["src2"])

        if "data-src" in img_dict:
            bing_images.append(img_dict["data-src"])

        print(width, height)
    print(len(bing_images), bing_images)
    return bing_images


def scrape_images_from_google(query):
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    image_elements = soup.find_all('img', class_='t0fcAb')

    image_urls = [img['data-src'] for img in image_elements]
    # print(image_urls, len(image_elements))
    # return image_urls

output_directory = "data/户口本"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


# Scrape images from Bing
for page_num in range(1):
    print(f"Page Num: {page_num}")
    scrape_images_from_bing("户口本", page_num)


# for i, url in enumerate(bing_images):
#     if url.startswith("http"):
#         filename = f"image_{i}.jpg"
#         download_image(url, output_directory, filename)
#
#     print(f"Image {i+1}: {url}")

# # Scrape images from Google
# google_images = scrape_images_from_google("cat")
# print("\nGoogle Images:")
# for i, url in enumerate(google_images):
#     print(f"Image {i+1}: {url}")