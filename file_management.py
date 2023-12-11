# UploadPackageHandler.py

from base import BaseHandler
from urllib.parse import quote

class UploadPackageHandler(BaseHandler):
    def get(self):
        self.render("upload_file.html")

    def post(self):
        """
        检查文件类型
        生成 task  增加到任务队列中
        
        :return:
        """

        files = self.request.files.get('files', [])
        file_list = list()
        for file in files:
            filename = file['filename']
            content = file['body']
            # 处理文件上传逻辑，例如保存到特定路径、数据库等
            # 这里只简单打印文件名和内容
            file_list.append(filename)
            print(f'文件名: {filename}')
            # print(f'文件内容: {content}')
        print(file_list)
        self.write({"message": file_list, "error_code": 1000})


class DownloadFileHandler(BaseHandler):
    async def get(self):
        """
        下载 API

        This API is used to download a file. It accepts the following parameters:

        Parameters:
        - Authorization: Authorization token in the request header.
        - filename: Name of the file.

        Returns:
        - The file data for download.

        Errors:
        - 6000: File does not exist error.
        - 6005: File is not fully uploaded error.

        """

        filename = self.get_argument("filename", None)
        filename = "upload/upload_demo.txt"
        chunk_number = int(self.request.headers.get('X-Chunk-Number', default='0'))

        if not isinstance(chunk_number, int):
            chunk_number = int(chunk_number)

        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header("Content-Disposition", "attachment; filename=%s" % quote(filename))  # 中文支持
        self.set_header("File-Size", 344)

        chunk_size = 128  # Define the size of each chunk you want to read
        position = 0  # Starting position for reading
        position = chunk_number * chunk_size

        print("Chunk number:", chunk_number)

        with open(filename, 'r') as file:
            # Read the entire contents of the file
            file.seek(position)
            file_content = file.read(chunk_size)
            print(len(file_content), file_content)

            self.write(file_content)

        await self.finish()

