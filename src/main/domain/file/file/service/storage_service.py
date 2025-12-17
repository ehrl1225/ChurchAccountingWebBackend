from abc import ABC, abstractmethod
from typing import BinaryIO

class StorageService(ABC):

    @abstractmethod
    async def upload_file(self, file: BinaryIO, file_name: str, content_type: str) -> str:
        """
        Uploads a file to the storage and returns its accessible URL.
        :param file: A file-like object (e.g., file.file from UploadFile
        :param file_name: The disired name for the file in storage.
        :param content_type: The content type of the file (e.g., "image/jpeg")
        :return: The URL of the uploaded file.
        """
        pass

    @abstractmethod
    async def get_file_url(self, file_name: str) -> str:
        """
        Returns the URL for a given file name.
        :param file_name: The name of the file in storage.
        :return: The URL of the file.
        """
        pass

    @abstractmethod
    async def delete_file(self, file_name:str):
        """
        Deletes a file from the storage.
        :param file_name: The name of the file to delete.
        :return:
        """
        pass
