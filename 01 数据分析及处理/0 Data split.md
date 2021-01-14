# Data split

数据拆分是评估推荐系统中最重要的任务之一。拆分策略极大地影响了评估协议，因此从业人员应始终认真考虑它。

## 0 Global settings

```
# set the environment path to find Recommenders
import sys
sys.path.append("../../")

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from reco_utils.common.spark_utils import start_or_get_spark
from reco_utils.dataset.download_utils import maybe_download
from reco_utils.dataset.python_splitters import (
    python_random_split, 
    python_chrono_split, 
    python_stratified_split
)
from reco_utils.dataset.spark_splitters import (
    spark_random_split, 
    spark_chrono_split, 
    spark_stratified_split,
    spark_timestamp_split
)

print("System version: {}".format(sys.version))
print("Pyspark version: {}".format(pyspark.__version__))
```

```
>>System version: 3.7.6 (default, Jan  8 2020, 13:42:34) 
[Clang 4.0.1 (tags/RELEASE_401/final)]
```





## 1 Data preparation

### 1.1 Data understanding

####获取课程内容

filepath_section = "/Users/apple/Recommenders/examples/02_model_collaborative_filtering/moodle/section课程内容与时间.csv"

```
data_sectionTime = pd.read_csv(filepath_section,encoding='utf-8')
```

A glimpse at the data<img src="../Library/Application Support/typora-user-images/image-20210111130952799.png" alt="image-20210111130952799" style="zoom:50%;" />



#### 获得学生行为数据

filepath_student ='/Users/apple/Recommenders/examples/02_model_collaborative_filtering/moodle/学生行为记录2.csv'

```
data_student = pd.read_csv(filepath_student,encoding='gbk')
data_student.head()
```

A glimpse at the data

<img src="../Library/Application Support/typora-user-images/image-20210111131230627.png" alt="image-20210111131230627" style="zoom:50%;" />



#### 数据统计

```
DATA_PATH = "/Users/apple/Recommenders/examples/02_model_collaborative_filtering/moodle"

COL_USER = "学号"
COL_ITEM = "课程id"
COL_RATING = "持续时间"
COL_PREDICTION = "Rating"
COL_TIMESTAMP = "行为发生时间"
```

```
data_student.describe()
```

总共有679078条行为记录。

```
print(
    #"Total number of ratings are\t{}".format(data_student[COL_RATING]),
    "Total number of users are\t{}".format(data_student[COL_USER].nunique()),
    "Total number of items are\t{}".format(data_student[COL_ITEM].nunique()),
    sep="\n"
)
```

![image-20210111132037529](../Library/Application Support/typora-user-images/image-20210111132037529.png)

### 1.2 Data transformation

data.info()

<img src="../Library/Application Support/typora-user-images/image-20210111134131580.png" alt="image-20210111134131580" style="zoom:50%;" />



##### 清洗日期数据

```
data = data_student[(data_student["行为编号"] == 7)]
data[COL_TIMESTAMP] = pd.to_datetime(data[COL_TIMESTAMP],format = '%Y/%m/%d %H:%M')
data[COL_TIMESTAMP].dtypes
data.info()
```

#####清洗文本
```python
i=0
for each in data["持续时间"].values:

​    if(type(each) != int):
​        ea = int(each.split(":")[0])
​        data[COL_RATING].values[i] =ea
​    i = i+1

#清洗非正常格式的数据
i=0
for each in data["持续时间"].values:
    if(type(each) != int):
        data[COL_RATING].values[i] = 0;
    i = i+1
```

<img src="../Library/Application Support/typora-user-images/image-20210111143246710.png" alt="image-20210111143246710" style="zoom:50%;" />

## Data split

```
data_uir = data[['学号','课程id','持续时间']]
```

```
train, test = python_random_split(data_uir, 0.75)
```

