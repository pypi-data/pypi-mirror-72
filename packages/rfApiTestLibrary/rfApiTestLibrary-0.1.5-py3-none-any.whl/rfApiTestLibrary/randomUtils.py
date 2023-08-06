'''
Documentation: 用于随机字符串的生成，包括随机字母和数字.
引用包名是rfApiTestLibrary，引用本python文件，请使用Library  rfApiTestLibrary/randomUtils.py.
如果您觉得引用代码不方便，也可以使用框架提供的关键字Resource   rfApiTestLibrary/keywords/random.robot ]
'''
import random
import string
from builtins import BaseException, int, AssertionError, str, round
import time


def at_create_random_str(len=None):
    '''
    创建随机字符串：包含字母和数字
   【len】: 整型变量

    目前使用该方法的关键字是:
    [../keywords/random.Create Random Str],

    Examples:
        | 关键字             |  参数    |
        | Create Random Str |  ${len} |
    '''
    try:
        length = int(len)
    except BaseException:
        raise AssertionError(str(len) + ' is not type of int')
    if len==None:
        randomStr= "".join(random.sample(string.ascii_letters + string.digits, 5))
        return randomStr
    else:
        randomStr= "".join(random.sample(string.ascii_letters + string.digits, length))
        return randomStr

def at_create_random_int(len=None):
    '''
    创建随机整数：包含字母和数字
   【len】: 整型变量，为创建的随机数的长度，如果为空，默认长度为5

    目前使用该方法的关键字是:
    [../keywords/random.Create Random Int],

    Examples:
        | 关键字             |  参数    |
        | Create Random Int |  ${len} |
    '''
    try:
        length = int(len)
    except BaseException:
        raise AssertionError(str(len) + ' is not type of int')
    if len==None:
        randomStr= "".join(random.sample(string.digits, 5))
        return int(randomStr)
    else:
        randomStr= "".join(random.sample(string.digits, length))
        return int(randomStr)

def at_get_timestamp():
    '''
     获取当前时间戳：毫秒级
    目前使用该方法的关键字是:
    [../keywords/random.Get Timestamp],

    Examples:
        | 关键字             |  参数    |
        | Get Timestamp |         |
    '''
    timestamp = time.time()
    return int(round(timestamp*1000))