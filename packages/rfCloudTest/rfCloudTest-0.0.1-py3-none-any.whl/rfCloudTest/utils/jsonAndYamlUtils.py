import yaml
import sys
import json

def open_json_or_yaml_file(json_or_yaml_file_path):
    '''
    读取json或者yaml文件
    :param yaml_file_path:
    :return:
    '''
    try:
        with open(json_or_yaml_file_path, encoding='UTF-8') as file:
            data=json.load(file)
    except Exception as e1:
        try:
            with open(json_or_yaml_file_path, encoding='UTF-8') as file:
                data = yaml.load(file,Loader=yaml.FullLoader)
        except Exception as e:
            print(e)
            print(json_or_yaml_file_path+' : 无法解析')
            sys.exit(-1)
    return data
