import requests
import pdfplumber
import cv2
import numpy as np


with pdfplumber.open('test.pdf') as pdf:
    ocr_text = ""
    img_ori = None
    for page_num, page in enumerate(pdf.pages):
        default_text = page.extract_text()
        ocr_text += default_text.replace(" ", "")

        img = page.to_image()
        if page_num == 0:
            img_ori = img
            pdf_image = img_ori.original
            img_cv = cv2.cvtColor(np.array(pdf_image), cv2.COLOR_RGB2BGR)
            resized_img = cv2.resize(img_cv, (int(img_cv.shape[1] / 4), int(img_cv.shape[0] / 4)))
            cv2.imwrite('tmp.jpg', resized_img)


remote_url = 'http://127.0.0.1:8011/detect/sync'
remote_path = 'id_card_num'

files = {'file': open('tmp.jpg', 'rb')}
data = {'path': remote_path, "material_type": "身份证"}

response = requests.post(remote_url, files=files, data=data)

if response.status_code == 200:
    print("文件传输成功！")
else:
    print("文件传输失败:", response.text)