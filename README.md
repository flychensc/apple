# apple
获取彩票历史数据，做简单数据分析

## 示例
```python
Python 3.6.4 |Anaconda, Inc.| (default, Jan 16 2018, 10:22:32) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from lottery import get_history as get_his
>>> his_data = get_his("七星彩", count=1)
>>> print(his_data)
[{'date': datetime.date(2018, 7, 15), 'result': [5, 4, 1, 8, 8, 6, 4], 'total': 5104935, 'grades': [{'num': 0, 'money': 0}, {'num': 6, 'money': 43284}, {'num': 109, 'money': 1800}, {'num': 1725, 'money': 300}, {'num': 21651, 'money': 20}, {'num': 251811, 'money': 5}]}]
>>> his_data = get_his("双色球", count=1)
>>> print(his_data)
[{'date': datetime.date(2018, 7, 15), 'result': {'red': [1, 2, 12, 16, 20, 26], 'blue': 3}, 'total': 174849270, 'grades': [{'num': 5, 'money': 9113851}, {'num': 154, 'money': 166958}, {'num': 1488, 'money': 3000}, {'num': 66828, 'money': 200}, {'num': 1261360, 'money': 10}, {'num': 7612560, 'money': 5}, {'num': 0, 'money': 0}]}]
>>>
```

## 输出格式
```js
[
    {
        'date': datetime.date(2018,7,15),
        'result': {
            'red': [1,2,12,16,20,26],
            'blue': 3
        },
        'total': 174849270,
        'grades': [
            {'num': 5, 'money': 9113851
            },
            {'num': 154, 'money': 166958
            },
            {'num': 1488, 'money': 3000
            },
            {'num': 66828, 'money': 200
            },
            {'num': 1261360, 'money': 10
            },
            {'num': 7612560, 'money': 5
            },
            {'num': 0, 'money': 0
            }
        ]
    }
]
```
