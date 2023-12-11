import paddle
from paddleocr import PaddleOCR, draw_ocr

# 加载模型
ocr = PaddleOCR(use_gpu=False)

# 输入图片
img_path = 'data/0004.jpg'
title = ["姓名", "性别", "民族", "出生", "住址", "公民身份号码"]
result = ocr.ocr(img_path)

# print(result)

# result = [[[[[47.0, 56.0], [136.0, 59.0], [136.0, 79.0], [46.0, 76.0]], ('姓名郝颁', 0.9940928816795349)], [[[48.0, 90.0], [114.0, 90.0], [114.0, 108.0], [48.0, 108.0]], ('性别男', 0.9997153282165527)], [[[145.0, 90.0], [207.0, 90.0], [207.0, 108.0], [145.0, 108.0]], ('民族汉', 0.9995177388191223)], [[[46.0, 122.0], [126.0, 116.0], [128.0, 135.0], [47.0, 141.0]], ('出生1984', 0.998253583908081)], [[[139.0, 117.0], [239.0, 119.0], [239.0, 140.0], [139.0, 138.0]], ('年9月19日', 0.9984073638916016)], [[[46.0, 155.0], [175.0, 153.0], [175.0, 172.0], [46.0, 174.0]], ('住址浙江省杭州', 0.991706371307373)], [[[93.0, 174.0], [279.0, 174.0], [279.0, 193.0], [93.0, 193.0]], ('某某666号--自制数据集', 0.9584340453147888)], [[[43.0, 243.0], [311.0, 236.0], [312.0, 258.0], [43.0, 265.0]], ('公民身份号码803226740643271224', 0.9978017807006836)]]]

res_dict = {}
current_title = None
for line in result[0]:
    # 提取信息
    # print(f"{line} \n")

    location = line[0]
    text, confidence = line[1]

    for t in title:
        if t in text:
            current_title = t
            text = text.replace(t, '').strip()  # 移除标题，留下内容
            break
    if current_title:
        if current_title not in res_dict:
            res_dict[current_title] = text
        else:
            res_dict[current_title] += ' ' + text


    # 打印信息
    # print(f"位置：{location}")
    print(f"文本：{text} 置信度：{confidence}")

print(res_dict)