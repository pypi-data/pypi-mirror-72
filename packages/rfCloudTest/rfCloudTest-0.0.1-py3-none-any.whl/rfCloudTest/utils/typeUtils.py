import json
import re

def is_rft_list_variable(str_data):
    if isinstance(str_data,str) and re.search('^@{.*}$', str_data) is not None:
        return True
    return False

def is_rft_dict_variable(str_data):
    if isinstance(str_data,str) and re.search('^&{.*}$', str_data) is not None:
        return True
    return False

def is_rft_variable(str_data):
    if isinstance(str_data,str) and re.search('^\${.*}$', str_data) is not None:
        return True
    return False


def is_str(str_data):
    '''
    验证是否是string
    :param str_data: 由于${}
    :return:
    '''
    if not isinstance(str_data,str):
        return False
    #验证不是robot framework的变量@{balabala}
    if re.search('^@{.*}$',str_data) is not None:
        return False
    if re.search('^&{.*}$',str_data) is not None:
        return False
    return True

def is_json_or_json_str(json_data):
    '''
    验证json_data是否是json或者可以转成json的string，再或者是rft变量。
    :param json_data:
    :return:
    '''
    if isinstance(json_data,dict) or isinstance(json_data,list):
        return True
    if isinstance(json_data,str):
        try:
            json.loads(json_data)
            return True
        except Exception:
            if is_rft_variable(json_data) or is_rft_dict_variable(json_data) or is_rft_list_variable(json_data):
                return True
    return False

def is_list_or_list_str(list_data):
    '''
    验证list_data是否是列表或者可以转成列表的string,再或者是rft变量
    :param list_data:
    :return:
    '''
    if isinstance(list_data,list):
        return True
    if isinstance(list_data,str):
        try:
            json.loads(list_data)
            return True
        except Exception:
            if is_rft_variable(dict) or is_rft_list_variable(list_data):
                return True
    return False

def is_dict_or_dict_str(dict_data):
    '''
    验证dict_data是否是字典或者可以转成字典的string,再或者是rft变量
    :param dict_data:
    :return:
    '''
    if isinstance(dict_data,dict):
        return True
    if isinstance(dict_data,str):
        try:
            data=json.loads(dict_data)
            if isinstance(data, dict):
                return True
            return False
        except Exception:
            if is_rft_variable(dict) or is_rft_dict_variable(dict_data):
                return True
    return False


def covert_json_or_json_str_to_json_formate_str(json_data):
    '''
    转成json string.
    :param json_data:
    :return:
    '''
    if isinstance(json_data, dict) or isinstance(json_data, list):
        return json.dumps(json_data,ensure_ascii=False)
    if isinstance(json_data, str):
        try:
            result=json.loads(json_data)
            return json.dumps(result,ensure_ascii=False)
        except Exception:
            if is_rft_variable(json_data) or is_rft_dict_variable(json_data) or is_rft_list_variable(json_data):
                return json_data
    return None

def is_int_or_int_str(int_data):
    '''
    验证数据是否是int或者可以转成int的string，支持robot framework的${<int>}的使用。
    :param int_data:
    :return:
    '''
    try:
        int(int_data)
        return True
    except Exception:
        if is_rft_variable(int_data):
            flag = re.search('^\${\s*\d+\s*}$', int_data)
            if flag is not None:
                return True
        return False

def get_int_value(int_data):
    '''
    int_data是int类型或者${<int>}的string类型
    :param int_data:
    :return:
    '''
    flag=is_int_or_int_str(int_data)
    if flag:
        try:
            int(int_data)
            return int(int_data)
        except Exception:
            pattern_str = '''^\${\s*(\d+)\s*}$'''
            pattern = re.compile(pattern_str, re.IGNORECASE)
            value_list = pattern.findall(int_data)
            if value_list==[]:
                return None
            return int(value_list[0])
    return None

def is_bool_or_bool_str(bool_data):
    '''
    验证bool_data是否是bool类型
    :param bool_data:
    :return:
    '''
    try:
        bool(bool_data)
        return True
    except Exception:
        return False

def get_bool_value(bool_data):
    '''
    :param bool_data:
    :return:
    '''
    return bool(bool_data)

def is_number_or_number_str(num_data):
    """
    验证非负数字或者能转成非负数字的String
    :param num_data:
    :return:
    """
    if isinstance(num_data, float):
        return True
    if isinstance(num_data, int):
        return True
    if not isinstance(num_data, str):
        return False
    flag = re.search('^\${\s*\d+\.\d+\s*}$', num_data)
    if flag is not None:
        return True
    flag = re.search('^\${\s*\d+\s*}$', num_data)
    if flag is not None:
        return True
    flag = re.search("^\d+\.\d+$", num_data)
    if flag is not None:
        return True
    flag = re.search("^\d+$", num_data)
    if flag is not None:
        return True
    return False


def get_num_value(num_data):
    """
    获取非负数字或者能转成非负数字的String
    :param num_data:
    :return:
    """
    flag = is_number_or_number_str(num_data)
    if flag:
        if isinstance(num_data, float) or isinstance(num_data, int):
            return num_data
        pattern_str = "^\${\s*(\d+\.\d+)\s*}$"
        flag = re.search(pattern_str, num_data)
        if flag is not None:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            value_list = pattern.findall(num_data)
            if value_list == []:
                return None
            return float(value_list[0])
        pattern_str = "^\${\s*(\d+)\s*}$"
        flag = re.search(pattern_str, num_data)
        if flag is not None:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            value_list = pattern.findall(num_data)
            if value_list == []:
                return None
            return int(value_list[0])
        pattern_str = "^(\d+\.\d+)$"
        flag = re.search(pattern_str, num_data)
        if flag is not None:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            value_list = pattern.findall(num_data)
            if value_list == []:
                return None
            return float(value_list[0])
        pattern_str = "^(\d+)$"
        flag = re.search("^\d+$", num_data)
        if flag is not None:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            value_list = pattern.findall(num_data)
            if value_list == []:
                return None
            return int(value_list[0])
    return None
