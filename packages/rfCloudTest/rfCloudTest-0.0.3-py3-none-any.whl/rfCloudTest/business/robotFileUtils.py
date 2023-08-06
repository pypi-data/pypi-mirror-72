from builtins import print, isinstance, list, len

import sys

from rfCloudTest.business import parseSuiteUtils
from rfCloudTest.utils import fileUtils, jsonAndYamlUtils, statusObj
from robot import run_cli
import os

CLOUD_TEST_OUTPUT='cloudtest-output'

def generate_robot_file_by_file_path(file_paths):
    fileUtils.create_directory(CLOUD_TEST_OUTPUT)
    fileUtils.remove_all_files(CLOUD_TEST_OUTPUT)
    for file_path in file_paths.split("::"):
        if not os.path.exists(file_path):
            print(file_path+' : 文件不存在')
            sys.exit(-1)
        if os.path.isfile(file_path):
            generate_robot_file(file_path)
            continue
        file_path_list=fileUtils.get_all_files(file_path)
        for item in file_path_list:
            generate_robot_file(item)

def generate_robot_file(file_path):
    json_data=jsonAndYamlUtils.open_json_or_yaml_file(file_path)
    if isinstance(json_data,list):
        for suite_item in json_data:
            suite_result=parseSuiteUtils.parse(file_path,suite_item)
            if suite_result[statusObj.STATUS]==statusObj.STATUS_NOK:
                print(file_path+': '+suite_result[statusObj.ERROR_MSG])
                sys.exit(-1)
            content=suite_result[statusObj.CONTENT]
            fileUtils.create_file( CLOUD_TEST_OUTPUT + '/' + suite_result[statusObj.SUITE]+'.robot',content)
    else:
        suite_result = parseSuiteUtils.parse(file_path,json_data)
        if suite_result[statusObj.STATUS] == statusObj.STATUS_NOK:
            print(file_path + ': ' + suite_result[statusObj.ERROR_MSG])
            sys.exit(-1)
        content = suite_result[statusObj.CONTENT]
        fileUtils.create_file(CLOUD_TEST_OUTPUT + '/' + suite_result[statusObj.SUITE] + '.robot', content)

def run_case(args):
    args.append(CLOUD_TEST_OUTPUT)
    run_cli(args)

def check_files_suite_name(file_paths):
    suite_name_dict={}
    for file_path in file_paths.split("::"):
        if not os.path.exists(file_path):
            print(file_path+' : 文件不存在')
            sys.exit(-1)
        if os.path.isfile(file_path):
            suite_name_dict=check_file_suite_name(file_path,suite_name_dict)
            continue
        file_path_list=fileUtils.get_all_files(file_path)
        for item in file_path_list:
            suite_name_dict=check_file_suite_name(item,suite_name_dict)
    flag=False
    print('=================================')
    for item_key in suite_name_dict:
        lst=suite_name_dict[item_key]
        if len(lst)>=2:
            flag=True
            print("\nsuite name: ["+ item_key+"]重复:")
            print('----------')
            for item in lst:
                print(os.path.abspath(item))
            print('----------\n')
    if not flag:
        print("没有重复的suite name")
    print('=================================')


def check_file_suite_name(file_path,suite_name_dict):
    print("读取文件: "+file_path)
    json_data = jsonAndYamlUtils.open_json_or_yaml_file(file_path)
    if isinstance(json_data, list):
        for suite_item in json_data:
            suite_name_dict = parseSuiteUtils.get_suite_name_dict(file_path, suite_item,suite_name_dict)
    else:
        suite_name_dict = parseSuiteUtils.get_suite_name_dict(file_path, json_data,suite_name_dict)
    print("读取文件: " + file_path+" 成功")
    return suite_name_dict
