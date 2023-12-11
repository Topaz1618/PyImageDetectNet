import os
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

from pymongo import MongoClient
import asyncio
from gridfs import GridFS
import motor.motor_asyncio

secret_key = b'YourSecretKey123'

HOST = '82.157.31.231'


MONGODB_SERVERS = [
    f'{HOST}:30001',
    f'{HOST}:30002',
    f'{HOST}:30003',
]

replicaSet = 'rs0'


def async_conn_db():
    """
    Establishes an asynchronous connection to the MongoDB server and returns the async client and database objects
    :return:
        async_client: The asynchronous connection to the MongoDB server
        async_db: The database object for the specified file system
    """
    mongo_cluster_uri = f"mongodb://{','.join(MONGODB_SERVERS)}/?replicaSet={replicaSet}"
    async_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_cluster_uri)
    async_db = async_client['filesystem']
    return async_client, async_db


def encrypt_data(data):
    cipher = AES.new(secret_key, AES.MODE_CBC)
    iv = cipher.iv  # Get the IV generated by PyCryptodome
    if not isinstance(data, bytes):
        data = data.encode('utf-8')

    padded_data = pad(data, AES.block_size)
    ct_bytes = cipher.encrypt(padded_data)

    # Combine IV and ciphertext and encode as Base64
    iv_and_ciphertext = iv + ct_bytes
    return base64.b64encode(iv_and_ciphertext).decode('utf-8')


def decrypt_data(encrypted_text):
    encrypted_text = base64.b64decode(encrypted_text)

    cipher = AES.new(secret_key, AES.MODE_CBC, encrypted_text[:AES.block_size])
    decrypted = cipher.decrypt(encrypted_text[AES.block_size:])
    # Strip PKCS7 padding manually

    padding_length = decrypted[-1]
    decrypted = decrypted[:-padding_length]
    return decrypted


class MongoDBManager:
    def __init__(self):
        self.async_client, self.async_db = async_conn_db()
        self.fs = motor.motor_asyncio.AsyncIOMotorGridFSBucket(self.async_db)


class AsyncGridFSManager(MongoDBManager):
    """
    A manager class for handling asynchronous operations with GridFS in MongoDB.
    """

    def __init__(self):
        super().__init__()
        self.chunk_size = 1024 * 1024

    async def download_chunk(self, chunk_id):
        download_stream = await self.fs.open_download_stream(chunk_id)
        return download_stream

    async def upload_chunk(self, data, filename):
        upload_stream = self.fs.open_upload_stream(filename=filename)
        try:
            await upload_stream.write(data)

        finally:
            await upload_stream.close()
        print(f'Uploaded file {filename} to GridFS')

    async def count_file_clips(self, filename):
        clip_count = await self.fs.find({'filename': filename}).to_list(length=None)
        return clip_count

    async def upload_file(self, filename):
        with open(filename, 'rb') as file:

            while True:
                chunk_data = file.read(self.chunk_size)
                if not chunk_data:
                    break
                print(f"Chunk data: {chunk_data}")
                encrypted_data = encrypt_data(chunk_data)
                if isinstance(encrypted_data, str):
                    # Encode the string data to bytes (using UTF-8 encoding in this example)
                    encrypted_data = encrypted_data.encode('utf-8')
                print(f"Encrypted data: {encrypted_data}")
                await self.upload_chunk(encrypted_data, filename)

            print(f'Uploaded file {filename} to GridFS')

    async def download_file(self, filename, output_path):
        versions = await self.count_file_clips(filename)

        print(versions)
        with open(output_path, 'wb') as file:
            for chunk_number in range(len(versions)):
                version = versions[chunk_number]  # 指定切片
                chunk_id = version['_id']
                print(version, chunk_id)
                download_stream = await self.download_chunk(chunk_id)
                data = await download_stream.read()

                print(f"Encrypted data: {data}")
                if not data:
                    break

                chunk_data = decrypt_data(data)
                print(f"Chunk data: {chunk_data}")

                file.write(chunk_data)

        print(f'Downloaded file {filename} from GridFS to {output_path}')

    async def delete_files_async(self, filename):
        versions = await self.fs.find({'filename': filename}).to_list(length=None)

        for version in versions:
            chunk_id = version['_id']
            await self.fs.delete(chunk_id)


# 示例用法
async def main():
    gridfs_manager = AsyncGridFSManager()

    # versions = await gridfs_manager.count_file_clips(os.path.join("data", "FileSystemDocker_v9.zip"))
    # print(len(versions))

    # 上传本地文件到MongoDB
    # await gridfs_manager.upload_file(os.path.join("data", "FileSystemDocker_v9.zip"))

    # 从MongoDB下载文件到本地
    await gridfs_manager.download_file('3e48b924-3fae-4225-ab3f-8dd7721b82a8_detect_demo1.zip', os.path.join("data", "output1.zip"))
    #
    # await gridfs_manager.delete_files_async('Test_1.1_Topaz')


# 运行示例用法
if __name__ == "__main__":
    asyncio.run(main())