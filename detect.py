"""
For test
"""

import os
import argparse
from time import sleep, time
from task_utils import get_task_info, update_task_info
from compression_utils import decompress_zip



# 创建参数解析器
parser = argparse.ArgumentParser(description='Description of your script')

# 添加需要的参数
parser.add_argument('--task_id', type=str, help='Id of detect task')
parser.add_argument('--model', type=str, help='Id of detect task')

# 解析命令行参数
args = parser.parse_args()

import tabula
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


def count_file_num(task_id, file_path):
    file_count = 0
    for root, dirs, files in os.walk(file_path):
        for file in files:
            file_count += 1
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file_path)[1]
            if file_extension == ".pdf":
                print(f"File {file_count}: {file_path} - PDF file")
                update_task_info(task_id, "log", f"Task ID: {task_id} File {file_count}: {file_path} - PDF file")

            elif file_extension == ".docx":
                print(f"File {file_count}: {file_path} - DOCX file")
                update_task_info(task_id, "log", f"Task ID: {task_id} File {file_count}: {file_path} - DOCX file")

            else:
                print(f"File {file_count}: {file_path} - Other file type")
                update_task_info(task_id, "log", f" Task ID: [{task_id}] File {file_count}: {file_path} - Other file type")

    return file_count

def main():
    # if not args.task_id:
    #     raise ValueError("no task id")

    task_id = "edbee8f6-981f-4359-9f60-4ee32e2fad52"

    if args.model:
        model = args.model
    else:
        model = "opencv"

    task_info = get_task_info(task_id)
    print(task_info)
    # Todo: 1. Redis 获取文件名称
    # Todo: 2. mongoDB 获取文件，测试先使用本文件
    # Todo: 3. 解压文件，获取总文件数，逐个处理，并生成格式为 {"文件名": "", "类型": "", "数据": ""} 的字符

    # 测试流程
    update_task_info(task_id, "log", "开始解压 (Unzipping)...")
    zip_name = task_info.get("detect_file")
    uncompress_file_path = decompress_zip(task_id, os.path.join("upload", zip_name))

    # update_task_info(task_id, "log", "开始计算文件数量")
    # file_count = count_file_num(task_id, uncompress_file_path)
    # update_task_info(task_id, "total_file_count", file_count)
    # update_task_info(task_id, "current_completed_file_count", 0)
    #
    # file_list = os.listdir(uncompress_file_path)
    # print(file_list)


    # # 提取表格数据
    # table_data = extract_table_data(pdf_path)
    #
    # # 将表格数据转换为JSON
    # json_data = convert_table_to_json(table_data)
    #
    # # 打印JSON数据
    # print(json_data)


if __name__ == "__main__":
    # 指定PDF文件路径
    print(" === 文件识别任务调试用方法测试开始 ===")
    main()

    print(" === 文件识别任务调试用方法测试结束 ===")
