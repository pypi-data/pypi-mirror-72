# -*- coding: utf-8 -*-
import json

class Config:
    """
    读写配置文件
    快速
    
    """
    def __init__(self,file='config.json'):
        self.file=file
    def save_config(data):
        """
        数据保存为json文件
        """
        with open( self.file, 'w') as outfile:
            json.dump(data, outfile)

    def read_config():
        """
        读取json文件
        """
        with open( self.file) as json_file:
            return json.load(json_file)

    def update_config():
        """
        读取json文件
        """
        with open( self.file) as json_file:
            return json.load(json_file)