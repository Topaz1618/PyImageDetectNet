"""
Note: The following code can extract text from an ID card image, but the results may not be highly accurate.

注意: 以下代码可以从身份证图像中提取文本，但效果可能较差。
"""

import cv2
import pytesseract

# 读取身份证图像
image = cv2.imread('0004.jpg')

text = pytesseract.image_to_string(image, lang='chi_sim')
print(text)