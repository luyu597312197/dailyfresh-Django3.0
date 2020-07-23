from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import *


class FDFSStorage(Storage):
    """fast dfs文件存储类"""
    def __init__(self, client_conf=None, base_url=None):
        """初始化"""
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        """打开文件时使用"""
        pass

    def _save(self, name, content):
        """保存文件时使用"""
        # name:你选择上传文件的名字
        # content:包含你上传文件内容的对象

        # 创建一个Fsfs_client对象
        tracker_path = get_tracker_conf(self.client_conf)
        client = Fdfs_client(tracker_path)

        # 上传文件到fdfs_dfs系统中
        res = client.upload_by_buffer(content.read())

        """
        dict {
            'Group name'      : group_name,
            'Remote file_id'  : remote_file_id,
            'Status'          : 'Upload successed.',
            'Local file name' : local_file_name,
            'Uploaded size'   : upload_size,
            'Storage IP'      : storage_ip
        } if success else None
        """
        if res.get("Status") != "Upload successed.":
            # 上传失败
            raise Exception("上传文件到fdfs dfs失败")

        # 获取返回文件的id
        filename = res.get("Remote file_id")

        return filename.decode()

    def exists(self, name):
        """Django判断文件名是否可用"""
        return False

    def url(self, name):
        """返回访问文件的url路径"""
        return self.base_url + name
        # return name