import json
import shutil

class Json:
  """
  处理json信息函数
  """
  def __init__(self,file_path="data.json"):
    self.file_path=file_path
  def save(self,data):
    """
    保存数据函数
    逐行写入
    >>> data=[{'a':'ess'}]
    """
    with open(self.file_path, 'a+', encoding='utf-8') as f:
      for item in data:
        line = json.dumps(item, ensure_ascii=False)
        f.write(line+'\n')
  def load(self):
    """
    加载数据
    """
    lines=[]
    for line in self.auto_load():
      lines.append(line)
    return lines
  def json_remove_duplicates(self,json_file):
        print("尝试移除重复数据")
        origin_json=tkitFile.Json(json_file)
        temp=tkitFile.Json(json_file+".tmp.json")
        tt=tkitText.Text()
        temp_keys=[]
        data=[]
        num_duplicates=0
        for i, item in enumerate(origin_json.auto_load()):
            data.append(json.dumps(item))
        new=list(set(data))
        print("原始长度",len(data))
        new_json=[]
        for item in new:
            new_json.append(json.loads(item))
        print("新长度",len(new_json))
        temp.save(new_json)
        print("移除重复内容",num_duplicates)
        #覆盖之前文件
        shutil.move(json_file+".tmp.json",json_file)

  def auto_load(self):
    """
    加载数据

    """
    # with open(self.file_path, "r") as json_file:
    #   data = json.load(json_file)
    #   return data
    f = open(self.file_path,"r")  
    # lines = f.readlines()#读取全部内容  
    # lines=[]
    for line in f.readlines():
      data=json.loads(line[:-1])
      yield data
"""
#使用
data=[{'a':'ess'}]
Json().save(data)
print(Json().load())


"""


