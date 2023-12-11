
"""
This script reads annotation information from an XML file and visualizes the annotations on an image. The XML file contains structured data that represents annotations for objects in an image.
The XML file typically includes the following information:
    - Image filename: The name or path of the annotated image file.
    - Image size: The width, height, and depth (number of color channels) of the image.
    - Object annotations: Each object in the image is represented by an XML element. The object element contains the following information:
        - Object name: The name or label of the object.
        - Bounding box coordinates: The coordinates of the bounding box that encloses the object in the image. The coordinates typically include xmin, ymin, xmax, and ymax values.

This script utilizes the parse_annotation function to extract the annotation data from the XML file. The function parses the XML file, extracts the relevant information, and returns a dictionary containing the parsed label data.
The extracted label data is then used to visualize the annotations on the input image. The script draws bounding boxes around the objects and displays the image with the annotations.

该脚本从 XML 文件中读取注释信息，并将注释可视化显示在图像上。XML 文件包含了结构化数据，用于表示图像中物体的注释信息。 XML 文件通常包含以下信息：
    - 图像文件名：被注释的图像文件的名称或路径。
    - 图像尺寸：图像的宽度、高度和深度（颜色通道数）。
    - 物体注释：图像中的每个物体都由一个 XML 元素表示。物体元素包含以下信息：
        - 物体名称：物体的名称或标签。
        - 边界框坐标：包围物体的边界框在图像中的坐标。通常包括 xmin、ymin、xmax 和 ymax 值。

该脚本利用 parse_annotation 函数从 XML 文件中提取注释数据。该函数解析 XML 文件，提取相关信息，并返回包含解析后标签数据的字典。
提取的标签数据随后用于将注释可视化显示在输入图像上。脚本绘制物体的边界框，并显示带有注释的图像。

"""

import xml.etree.ElementTree as ET

import cv2

# 解析注释信息
def parse_annotation(annotation):
    tree = ET.ElementTree(file=annotation)
    root = tree.getroot()

    # 提取文件名
    filename = root.find('filename').text

    # 提取图像尺寸
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    depth = int(size.find('depth').text)


    # 构建通用的图像信息
    common_data = {
        'filename': filename,
        'width': width,
        'height': height,
        'depth': depth,
        "objects": list(),
    }

    # 提取所有物体信息
    objects = root.findall('object')

    # 构建标签数据列表
    object_data_list = []

    # 构建每个物体的标签数据
    for object_elem in objects:
        name = object_elem.find('name').text

        # 提取边界框坐标
        bndbox = object_elem.find('bndbox')
        xmin = float(bndbox.find('xmin').text)
        ymin = float(bndbox.find('ymin').text)
        xmax = float(bndbox.find('xmax').text)
        ymax = float(bndbox.find('ymax').text)

        # 构建单个物体的标签数据
        object_data = {
            'name': name,
            'bbox': {
                'xmin': xmin,
                'ymin': ymin,
                'xmax': xmax,
                'ymax': ymax
            }
        }

        object_data_list.append(object_data)

    label_data = {
        'filename': filename,
        'width': width,
        'height': height,
        'depth': depth,
        'objects': object_data_list
    }

    return label_data


if __name__ == "__main__":
    xml_file = 'data/table.xml'
    # 解析注释
    label_data = parse_annotation(xml_file)

    # 打印标签数据
    print(label_data)
    image_path = 'data/table.jpg'
    image = cv2.imread(image_path)



    for idx, obj in enumerate(label_data['objects']):
        name = obj['name']
        bbox = obj['bbox']
        xmin, ymin, xmax, ymax = bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']

        print("IDX:", idx, xmin, ymin, xmax, ymax)

        # 绘制边界框
        cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)

        # 标注坐标信息
        label = f'{xmin}, {ymin}, {xmax}, {ymax}'
        cv2.putText(image, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # 显示绘制结果
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()