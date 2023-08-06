import json

class Config:
    def save_config(data,file='config.json'):
        """
        数据保存为json文件
        """
        with open(file, 'w') as outfile:
            json.dump(data, outfile)

    def read_config(file='config.json'):
        """
        读取json文件
        """
        with open(file) as json_file:
            return json.load(json_file)

    def update_config(file='config.json'):
        """
        读取json文件
        """
        with open(file) as json_file:
            return json.load(json_file)