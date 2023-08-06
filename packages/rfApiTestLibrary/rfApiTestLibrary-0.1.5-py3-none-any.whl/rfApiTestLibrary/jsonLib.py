'''
Documentation: 处理json包含关系的方法
'''
from builtins import AssertionError

import json_tools
import rfApiTestLibrary.log as log
import re
import copy
import json
import re
from collections import Counter
# def json_contain_sub_json(son_json, father_json):
#     '''
#     父亲json包含儿子json。父亲一般来说就是实际结果，儿子一般是期待的结果
#     :param father_json: json类型
#     :param son_json: json类型
#     '''
#     result = json_tools.diff(son_json, father_json)
#     if not isinstance(result,list):
#         raise AssertionError("json_tools的返回结果不是list,有可能是输入数据有误！")
#     msg="两个json对比结果: "+str(result)
#     log.info(msg, html=True, also_console=True)
#     if result==[]:
#         log.info("两个json完全相同",html=True, also_console=True)
#         return
#     for item in result:
#         if not isinstance(item,dict):
#             raise AssertionError("json_tools的返回结果具体内容不是字典,有可能是输入数据有误！")
#         #不处理'add'，只处理'remove'，'replace'
#         if 'remove' in item:
#             raise AssertionError(msg)
#         if 'replace' in item:
#             raise AssertionError(msg)

def json_contains_not_orderd_sub_json(son,father):
    '''
    父亲json包含儿子json。父亲一般来说就是实际结果，儿子一般是期待的结果。此方法
    支持list无序包含。但是不支持list内部包含嵌套。
    :param son:
    :param father:
    :return:
    '''
    result = json_tools.diff(son, father)
    lst = []
    if not isinstance(result,list):
        raise AssertionError("json_tools的返回结果不是list,有可能是输入数据有误！")
    msg="两个json对比结果: "+str(result)
    if result==[]:
        return
    for item in result:
        if not isinstance(item,dict):
            raise AssertionError("json_tools的返回结果具体内容不是字典,有可能是输入数据有误！")
        #不处理'add'，只处理'remove'，'replace'
        if 'remove' in item:
            raise AssertionError(msg)
        if 'replace' in item:
            pattern_str = '/\d+'
            pattern = re.compile(pattern_str)
            value_list = pattern.findall(item['replace'])
            if value_list==[]:
                raise AssertionError(msg)

            temp_start = 0
            temp_str = ''
            for value_item in value_list:
                index = item['replace'].index(value_item, temp_start)
                temp_str = temp_str + item['replace'][temp_start:index]
                if not temp_str in lst:
                    for lst_item in lst:
                        if lst_item.index(temp_str)==0 or temp_str.index(lst_item)==0:
                            raise AssertionError("不支持超过1层的list比较")
                    lst.append(temp_str)
                temp_start = index + len(value_item)
    for lst_item in lst:
        son_data=parse_json_by_path(son,lst_item)
        father_data=parse_json_by_path(father,lst_item)
        son_data_length=len(son_data)
        father_data_length = len(father_data)
        if son_data_length>father_data_length:
            raise AssertionError(msg)
        for son_data_item in son_data:
            match1=set()
            for father_data_item in father_data:
                match2=set()
                for son_key,son_value in son_data_item.items():
                    if son_key not in father_data_item:
                        match2.add(False)
                        break
                    father_value = father_data_item[son_key]
                    if type(father_value) != type(son_value):
                        match2.add(False)
                        break
                    if isinstance(son_value,list):
                        match2.add(False)
                        raise AssertionError("不支持超过1层的list比较")
                    if isinstance(son_value, str) or isinstance(son_value, bool) or isinstance(son_value,int) or isinstance(son_value, float):
                        if son_value != father_value:
                            match2.add(False)
                            break
                        match2.add(True)
                if len(match2)==0 or False in match2:
                    continue
                if True in match2:
                    match1.add(True)
                    break
            if len(match1)==0:
                raise AssertionError(msg)
                break



def parse_json_by_path(json,path):
    '''

    :param json:
    :param path:
    :return:
    '''
    arr=path.split('/')
    new_json=json
    for item in arr:
        if item=='':
            continue
        pattern_str = '\d+'
        pattern = re.compile(pattern_str)
        value_list = pattern.findall(item)
        if len(value_list)!=0:
            new_json=new_json[int(value_list[0])]
            continue
        new_json=new_json[item]
    return new_json

def json_contain_sub_json(dictobj2,dictobj1):
    """
    【功能】比较两个字典类型是否是包含关系
    【参数】dictobj1:字典类型
            dictobj2:字典类型
    【结果】如果dictobj2中的键值对在dictobj1中都存在，且路径一致，则认为存在包含关系，否则不存在包含关系
    """
    # 如果dictobj2为{}则直接返回True
    if dictobj2 is {}:
        return True

    # 将dictobj1、dictobj2转换为字典类型
    if not isinstance(dictobj1, dict):
        dictobj1 = json.loads(dictobj1)
    if not isinstance(dictobj2, dict):
        dictobj2 = json.loads(dictobj2)

    # 获取dictobj1、dictobj2的所有value
    # values_dictobj1 = list(all_list(getvalues(dictobj1, result=[])).keys())
    values_dictobj2 = list(all_list(getvalues(dictobj2, result=[])).keys())

    fp_dictobj1 = find_path(dictobj1)
    fp_dictobj2 = find_path(dictobj2)

    # 存放比较结果
    result = True

    for value in values_dictobj2:
        the_value_path_dictobj1 = list(set(fp_dictobj1.the_value_path(value)))
        the_value_path_dictobj2 = list(set(fp_dictobj2.the_value_path(value)))
        the_value_path_dictobj1 = resetpathindex(the_value_path_dictobj1)
        the_value_path_dictobj2 = resetpathindex(the_value_path_dictobj2)
        print('the_value_path_dictobj1=%s' % the_value_path_dictobj1)
        print('the_value_path_dictobj2=%s' % the_value_path_dictobj2)
        if set(the_value_path_dictobj2) <= set(the_value_path_dictobj1):
            pass
        else:
            result = False
    if result == False:
        raise AssertionError('期望结果和实际结果之间不是包含关系')
    # return result

class find_path():
    def __init__(self,target):
        self.target=target

    def find_the_value(self,target,value,path='',path_list=None):
        '''完全匹配，每经过一层(list、dict)都会记录path，到了最后一层且当前target就是要找的目标，才把对应的path记录下来
        :param target: 被搜索的目标
        :param value: 要搜索的关键字
        :param path: 当前所在的路径
        :param path_list: 存放所有path的列表
        判断当前target类型：···是字典，循环内容，每个键值都记录下路径path，然后以当前值v为判断target，调用自身传入添加了的path判断
                             ···是列表，循环内容，每个元素都记录下路径path，然后以当前元素为判断target，调用自身传入添加了的path判断
                             ···是str或者int，那么就判断当前target是否就是要搜索的value，如果是，那就把路径path放进list里面'''
        if isinstance(target, dict):
            for k, v in target.items():
                path1 = copy.deepcopy(path)
                path1=path1+str([k])
                self.find_the_value(v, value, path1, path_list)

        elif isinstance(target, (list, tuple)):  # 判断了它是列表
            for i in target:
                path1 = copy.deepcopy(path)
                posi = target.index(i)
                path1 = path1+'[%s]' % posi
                self.find_the_value(i, value, path1, path_list)

        elif isinstance(target, (str, int)) :
            if  str(value) ==str(target):   #必须完全相同
                path_list.append(path)


    def find_in_value(self,target,value,path='',path_list=None):
        '''包含匹配，内容跟上面一样，只是最后判断时不同'''
        if isinstance(target, dict):
            for k, v in target.items():
                path1 = copy.deepcopy(path)
                path1=path1+str([k])
                self.find_in_value(v, value, path1, path_list)

        elif isinstance(target, (list, tuple)):  # 判断了它是列表
            for i in target:
                path1 = copy.deepcopy(path)
                posi = target.index(i)
                path1 = path1+'[%s]' % posi
                self.find_in_value(i, value, path1, path_list)

        elif isinstance(target, (str, int)) :
            if  str(value) in str(target):   #
                path_list.append(path)

    def find_the_key(self,target,key,path='',path_list=None):
        '''查找key，每经过一层(list、dict)都会记录path，在字典时，若当前的k就是要找的key，那就把对应的path记录下来
                :param target: 被搜索的目标
                :param key: 要搜的键
                :param path: 当前所在的路径
                :param path_list: 存放所有path的列表
                判断当前target类型：···是字典，循环内容，每个键值都记录下路径path，判断当前k是否要查找的：~~~是，那就把路径path放进list里面
                                                                                                 ~~~不是，以当前值v为判断target，调用自身传入添加了的path判断
                                  ···是列表，循环内容，每个元素都记录下路径path，然后以当前元素为判断target，调用自身传入添加了的path判断
                                     '''
        if isinstance(target, dict):
            for k, v in target.items():
                path1 = copy.deepcopy(path)
                path1=path1+str([k])
                if str(key) == str(k):
                    path_list.append(path1)
                else:
                    self.find_the_key(v, key, path1, path_list)

        elif isinstance(target, (list, tuple)):  # 判断了它是列表
            for i in target:
                path1 = copy.deepcopy(path)
                posi = target.index(i)
                path1 = path1+'[%s]' % posi
                self.find_the_key(i, key, path1, path_list)

    def in_value_path(self,value):
        '''包含匹配value'''
        path_list=[]
        self.find_in_value(self.target, value,path_list=path_list)
        return path_list

    def the_value_path(self,value):
        '''完全匹配value'''
        path_list=[]
        self.find_the_value(self.target, value,path_list=path_list)
        return path_list

    def the_key_path(self,value):
        '''只查找key'''
        path_list = []
        self.find_the_key( self.target, value,path_list=path_list)
        return path_list

def getvalues(dic,result):
    '''
    【功能】根据传入的字典类型参数，获取其每个键值对的值
    【参数】dic:传入的字典类型参数
            result:列表类型，存在dic中的每个键值对的值
    '''
    count=0
    keys=dic.keys()
    for key in keys:
        value=dic.get(key)
        if isinstance(value,dict):
            getvalues(value,result)
        elif isinstance(value,list):
            for ls in value:
                if isinstance(ls,dict):
                    getvalues(ls,result)
                else:
                    result.append(value)
        else:
            result.append(value)
    return result

def all_list(arr):
    '''
    【功能】去除列表中的重复值
    【参数】arr:列表类型
    【结果】返回不含重复值的列表
    '''
    result = {}
    for i in set(arr):
        result[i] = arr.count(i)
    return result

def resetpathindex(lst):
    '''
    【功能】将一个字典路径中包含的数组下标进行重置
    【参数】lst:期望被重置的字典路径数组
    【结果】被重置后的字典路径  例如：["['result'][2]['orgCodeList'][3]", "['result'][2]['orgCodeList'][3]","['result']['companies'][3]['orgCode']", "['result']['ownOrgCode']"]
            重置后为：["['result'][0]['orgCodeList'][0]", "['result'][1]['orgCodeList'][1]", "['result']['companies'][0]['orgCode']", "['result']['ownOrgCode']"]
    '''
    for i in range(len(lst)):
        ls = re.findall(r'\[+\d+\]+',str(lst[i]))
        for j in range(len(ls)):
            lst[i] = lst[i].replace(ls[j],'['+']')
    list_count = Counter(lst)
    for key in list_count:
        index = 0
        if list_count[key] >1:
            for k in range(len(lst)):
                if lst[k] == key:
                    lst[k] = lst[k].replace('[]', '[' +str(index)+ ']')
                    index+=1
            index =0
        elif list_count[key] == 1:
            for k in range(len(lst)):
                lst[k] = lst[k].replace('[]', '[' +str(index)+ ']')
            index =0
    return lst