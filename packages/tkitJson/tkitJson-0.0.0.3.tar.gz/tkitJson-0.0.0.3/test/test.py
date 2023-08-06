
#encoding=utf-8
from __future__ import unicode_literals
import sys
sys.path.append("../")
# from harvesttext import HarvestText

import tkitJson
# data=[{"item":111},{"item":111},{"item":111},{"item":111}]
# Tjson=tkitJson.Json("data.json")
# #添加数据
# Tjson.save(data)

# new_data=Tjson.load()
# print(new_data)

data={"no":111,
'bb':22
}
Config=tkitJson.Config("config.json")
Config.save(data)
#读取
data=Config.read()
print(data)

