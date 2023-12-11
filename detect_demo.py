"""
For test
"""



import pdfplumber
import json


def extract_table_data(pdf_path):
    # 使用pdfplumber打开PDF文件
    with pdfplumber.open(pdf_path) as pdf:
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
    return table_data


def convert_table_to_json(table_data):
    # 将表格数据转换为JSON格式
    json_data = json.dumps(table_data, ensure_ascii=False)
    return json_data

# 指定PDF文件路径
pdf_path = "dataset/test_data/test.pdf"

# 提取表格数据
table_data = extract_table_data(pdf_path)

# 将表格数据转换为JSON
json_data = convert_table_to_json(table_data)

# 打印JSON数据
print(json_data)
print(" === 文件识别任务调试用方法 ===")