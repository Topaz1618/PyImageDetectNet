import os
import shutil
import pdfplumber
import pytesseract
import re
import docx
from enum import Enum


class MaterialType(Enum):
    ID_CARD = "身份证"
    LAND_MAP = "宗地图"
    HOUSEHOLD_REGISTER = "户口本"
    REAL_ESTATE_APPLICATION = "不动产申请表"
    UNKNOWN = "Unknown"

    def get_text_format(self):
        return self.name


class FileFormatType(Enum):
    DOCX = ".docx"
    PDF = ".pdf"
    JPG = ".jpg"
    PNG = ".png"
    XLSX = ".xlsx"
    CSV = ".csv"
    UNKNOWN = "Unknown"

    def get_text_format(self):
        return self.name


class MaterialTitleType(Enum):
    LAND_MAP = "土地权利人"
    REAL_ESTATE_APPLICATION = "不动产单元号"
    UNKNOWN = "Unknown"

    def get_text_format(self):
        return self.name

file_title_keywords = {
    MaterialType.LAND_MAP: ['宗地代码', '土地权利人', '所在图幅号', '宗地面积', 'J1', 'J2', 'J3', 'J4'],
    MaterialType.REAL_ESTATE_APPLICATION:  ['不动产调查登记申请表', '预编号', '宗地代码', '不动产单元号', '权利人', '权利人类型', '证件种类', '证件号', '联系电话', '权利人身份', '法定代表人或负责人姓名', '电话', '代理人姓名', '户口簿', '权利类型', '权属来源证明材料', '土地来源证明材料', '权属证件号', '权属证件发证时间', '权利性质', '共有/共用权利人情况', '批准用途', '实际用途', '地类编码', '批准面积', '宗地面积', '房屋竣工时间', '房屋性质', '房屋状况', '幢号', '总层数', '所在层', '房屋结构', '占地面积', '建筑面积', '专有建筑面积', '分摊建筑面积', '权属来源', '墙体归属', '东', '南', '西', '北']
}


def match_file_format(file_extension):
    matching_format = None
    for format_type in FileFormatType:
        if format_type.value == file_extension:
            matching_format = format_type
            text_format = matching_format.get_text_format()
            return text_format

    if not matching_format:
        return FileFormatType.UNKNOWN.get_text_format()


def extract_table_data(pdf_path):
    # 使用pdfplumber打开PDF文件
    with pdfplumber.open(pdf_path) as pdf:
        page_num = len(pdf.pages)

        table_data = []
        for page in pdf.pages:
            # 提取页面中的表格
            tables = page.extract_tables()
            for table in tables:
                # 将表格数据转换为JSON格式
                table_json = []
                for row in table:
                    table_json.append(row)
                table_data.append(table_json)
    return table_data, page_num


def extract_text(pdf_path):
    # 使用pdfplumber打开PDF文件
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 将pdfplumber的Page对象转换为图像
            img = page.to_image()

            # 使用OCR来提取图像中的文本
            ocr_text = pytesseract.image_to_string(img.original, lang='chi_sim')

            # 使用正则表达式匹配身份证号码
            id_card_pattern = re.compile(r'\d{17}[\dXx]|\d{15}|\d{18}')
            matches = re.findall(id_card_pattern, ocr_text)

            # 打印匹配到的身份证号码
            if matches:
                for match in matches:
                    print("身份证号码:", match)
                    return match


def loop_files(detect_folder_path):
    file_dic = {}
    # Todo: 获取总文件数量:

    for file_name in os.listdir(detect_folder_path):
        # Todo: 更新当前处理文件
        file_path = os.path.join(detect_folder_path, file_name)

        file_extension = os.path.splitext(file_path)[1]
        file_type = match_file_format(file_extension)
        file_dic[file_name] = {
            "file_type": file_type,
        }

        if file_extension == FileFormatType.PDF.value:
            table_data, page_num = extract_table_data(file_path)

            file_dic[file_name]["page_num"] = page_num

            if not table_data:
                id_number = extract_text(file_path)
                if id_number:
                    file_dic[file_name]["material_type"] = MaterialType.ID_CARD.value
                    table_data = {"id": id_number}

            else:
                table_data = [[item.replace('\n', '') for item in sublist if item is not None and item != ''] for sublist in table_data[0]]

            file_dic[file_name]["json_data"] = table_data

            if not table_data:
                continue

            if any(MaterialTitleType.LAND_MAP.value in item for item in table_data):
                file_dic[file_name]["material_type"] = MaterialType.LAND_MAP.value

            elif any(MaterialTitleType.REAL_ESTATE_APPLICATION.value in item for item in table_data):
                file_dic[file_name]["material_type"] = MaterialType.REAL_ESTATE_APPLICATION.value

            else:
                file_dic[file_name]["material_type"] = MaterialType.UNKNOWN.value

            # Todo: 更新已处理完成文件数量

    print(file_dic)


if __name__ == "__main__":
    detect_folder_path = "data/detect_demo1"
    loop_files(detect_folder_path)