# -*- coding: utf-8 -*-
import json

class Config:
    """
    读写配置文件
    快速
    
    """
    def __init__(self,file='config.json'):
        self.file=file
    def save(self,data):
        """
        数据保存为json文件
        """
        with open( self.file, 'w') as outfile:
            json.dump(data, outfile)

    def read(self):
        """
        读取json文件
        """
        with open( self.file) as json_file:
            return json.load(json_file)

    # def update(self,data):
    #     """
    #     读取json文件
    #     """
    #     with open( self.file) as json_file:
    #         return json.load(json_file)