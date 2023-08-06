# **PyUnit-phone** [![](https://gitee.com/tyoui/logo/raw/master/logo/photolog.png)][1]

## 实体提取电话号码，包括电话号码的有效消息：电话类型、电话区号、运营商等
[![](https://img.shields.io/badge/Python-3.7-green.svg)](https://pypi.org/project/pyunit-address/)

## 安装
    pip install pyunit-phone


## 使用
```python
from pyunit_phone import Phone

phone = Phone()


def check_up():
    data = """
    我的电话是15180865874,
    他的电话是0851-12456789,
    骚扰电话：075523675665,
    01051369070 18716521010 
    """
    assert phone.extract(data) == \
           [{
               'city': '贵阳',
               'operators': '移动',
               'province': '贵州',
               'type': '移动手机卡',
               'value': '15180865874'
           },
               {
                   'city': '万州',
                   'operators': '移动',
                   'province': '重庆',
                   'type': '移动手机卡',
                   'value': '18716521010'
               },
               {
                   'city': '贵阳',
                   'operators': '电信',
                   'province': '贵州',
                   'type': '固定电话',
                   'value': '0851-12456789'
               },
               {
                   'city': '深圳',
                   'operators': '电信',
                   'province': '广东',
                   'type': '固定电话',
                   'value': '075523675665'
               },
               {
                   'city': '北京',
                   'operators': '电信',
                   'province': '北京',
                   'type': '固定电话',
                   'value': '01051369070'
               }
           ]


if __name__ == '__main__':
    check_up()
```

## Docker部署
    docker pull jtyoui/pyunit-phone
    docker run -d -P jtyoui/pyunit-phone

### 车牌号规则提取
|**参数名**|**类型**|**是否可以为空**|**说明**|
|------|------|-------|--------|
|data|string|YES|输入话带有电话的句子|

### 请求示例
> #### Python3 Requests测试
```python
import requests

url = "http://IP:端口/pyunit/phone"
data = {
    'data': '我的电话是15180865874',
}
headers = {'Content-Type': "application/x-www-form-urlencoded"}
response = requests.post(url, data=data, headers=headers).json()
print(response)
``` 

> #### 返回结果
```json
{
    "code":200,
    "result":[
        {
            "city":"贵阳",
            "operators":"移动",
            "province":"贵州",
            "type":"移动手机卡",
            "value":"15180864978"
        }
    ]
}
```

***
[1]: https://blog.jtyoui.com