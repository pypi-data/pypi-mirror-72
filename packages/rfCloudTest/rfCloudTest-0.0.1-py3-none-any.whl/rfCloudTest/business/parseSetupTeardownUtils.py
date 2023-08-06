'''
{
   "keyword":"",
   "params":[]
}
'''

from xforceCloudTestBasic import statusObj as statusObj
import json

_KEY_WORD="keyword"
_PARAMS="params"
_SEPERATE=" " * 2
_BLOCK=" "*4
SUITE_SETUP='suiteSetup'
SUITE_TEARDOWN='suiteTeardown'
TEST_SETUP='testSetup'
TEST_TEARDOWN='testTeardown'
CASE_TEST_SETUP="setup"
CASE_TEST_TEARDOWN="teardown"

def parse(file_path, suite_name, json_data, json_type, rft_str):
    if not isinstance(json_data, dict):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, json_type + ': 不是字典类型')

    if _KEY_WORD not in json_data:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, json_type + ': 不包含' + _KEY_WORD)
    keyword=json_data[_KEY_WORD]
    if not isinstance(keyword,str):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, json_type + '的' + _KEY_WORD+'必须是string类型')
    content= rft_str + _SEPERATE + keyword
    if _PARAMS in json_data and json_data[_PARAMS] is not None:
        params=json_data[_PARAMS]
        if not isinstance(params,list):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, json_type + '的' + _PARAMS+'必须是list类型')
        for param in params:
            if isinstance(param,str):
                content+=_SEPERATE + param
            elif isinstance(param,list) or isinstance(param,dict):
                try:
                    content+=_SEPERATE + json.dumps(param,ensure_ascii=False)
                except:
                    return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, json_type + '的' + _PARAMS+'里有无法解析的json数据')
            else:
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, json_type + '的' + _PARAMS+'里的bool,null,int,double类型，请使用RFT转义')
    content+='\n'
    return statusObj.get_step_content(file_path, statusObj.STATUS_OK, suite_name, None, None, None, 'OK', content=content)

def parse_suite_setup(file_path, suite_name, suite_setup_json):
    return parse(file_path, suite_name, suite_setup_json, SUITE_SETUP, 'Suite Setup')

def parse_suite_teardown(file_path, suite_name, suite_teardown_json):
    return parse(file_path, suite_name, suite_teardown_json, SUITE_TEARDOWN, 'Suite Teardown')

def parse_test_setup(file_path, suite_name, test_setup_json):
    return parse(file_path, suite_name, test_setup_json, TEST_SETUP, 'Test Setup')

def parse_test_teardown(file_path, suite_name, test_teardown_json):
    return parse(file_path, suite_name, test_teardown_json, TEST_TEARDOWN, 'Test Teardown')

def parse_case(file_path, suite_name, case_name,json_data, json_type, rft_str):
    if not isinstance(json_data, dict):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, json_type + ': 不是字典类型')

    if _KEY_WORD not in json_data:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, json_type + ': 不包含' + _KEY_WORD)
    keyword=json_data[_KEY_WORD]
    if not isinstance(keyword,str):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, json_type + '的' + _KEY_WORD+'必须是string类型')
    content= _BLOCK + rft_str + _SEPERATE + keyword
    if _PARAMS in json_data and json_data[_PARAMS] is not None:
        params=json_data[_PARAMS]
        if not isinstance(params,list):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, json_type + '的' + _PARAMS+'必须是list类型')
        for param in params:
            if isinstance(param,str):
                content+=_SEPERATE + param
            elif isinstance(param,list) or isinstance(param,dict):
                try:
                    content+=_SEPERATE + json.dumps(param,ensure_ascii=False)
                except:
                    return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, json_type + '的' + _PARAMS+'里有无法解析的json数据')
            else:
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, json_type + '的' + _PARAMS+'里的bool,null,int,double类型，请使用RFT转义')
    content+='\n'
    return statusObj.get_step_content(file_path, statusObj.STATUS_OK, suite_name, case_name, None, None, 'OK', content=content)

def parse_case_setup(file_path, suite_name, case_name,json_data):
    return parse_case(file_path, suite_name, case_name,json_data,CASE_TEST_SETUP,'[Setup]')

def parse_case_teardown(file_path, suite_name, case_name,json_data):
    return parse_case(file_path, suite_name, case_name,json_data,CASE_TEST_TEARDOWN,'[Teardown]')