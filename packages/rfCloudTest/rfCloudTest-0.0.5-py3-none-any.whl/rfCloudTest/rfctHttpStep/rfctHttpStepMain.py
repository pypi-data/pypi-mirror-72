'''
解析http请求步骤的.
解析类似下面的json
{
    "name": "测试步骤1",
    "type": "http",
    "wait":{
       "retry":"",
       "retryInterval"
    }
    "input": {
        "method": "get",
        "url": "${url}/aa/bb/cc",
        "params": {
            "aa": "123",
            "bb": "sak"
        },
        "data": "adsdsfgfadfsf",
        "req_json": null,
        "req_headers": {
            "www": "sdsad",
             "NN": "dsaad"
        },
        "timeout":null
    },
    "expect": {
        "expect_status_code": "${200}",
        "expect_resp_headers": {
            "aa": "213"
        },
        "expect_resp_body": null,
        "expect_resp_json": "${None}",
        "expect_resp_body_contains": "${empty}",
        "expect_resp_json_contains": "${empty}"
    }
}
'''

import json
from builtins import str, isinstance, dict, int

from rfCloudTest.utils import typeUtils, statusObj

_STEP_NAME='name'
_INPUT='input'
_EXPECT='expect'
_METHOD='method'
_URL='url'
_REQ_JSON='req_json'
_REQ_HEADER='req_headers'
_PARAMS='params'
_DATA='data'
_TIMEOUT='timeout'
_STATUS_CODE='expect_status_code'
_RESP_HEADER='expect_resp_headers_contains'
_RESP_BODY='expect_resp_body'
_RESP_JSON='expect_resp_json'
_RESP_BODY_CONTAINS='expect_resp_body_contains'
_RESP_JSON_CONTAINS='expect_resp_json_contains'
_RESP_JSON_REGULAR_EXPRESSION_CONTAINS="expect_resp_json_regular_expression_contains"
_RESP_BODY_REGULAR_EXPRESSION_CONTAINS="expect_resp_body_regular_expression_contains"
_RESP_JSON_SPECIAL_CONTAINS="expect_resp_json_special_contains"
_BLOCK=" " * 4
_SEPERATE=" " * 2
_KEY_WORD='At One Http Interface Test'
_STEP_TYPE='http'

_STEP_WAIT="wait"
_STEP_WAIT_RETRY="retry"
_STEP_WAIT_RETRY_INTERVAL="retryInterval"
_WAIT_KEYWORD="Wait until keyword succeeds"

_HTTP_METHOD=['GET','POST','PUT','DELETE','PATCH']

_HTTP_STATUS_CODE=[
    100,101,102,200,201,202,203,204,205,206,207,300,301,302,303,304,305,306,307,
    400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,
    421,422,423,424,425,426,449,451,500,501,502,503,504,505,506,507,508,509,510,
    600
]

def parse(file_path, suite_name,case_name,step_detail_json):
    '''
    检查http步骤是否有效。
    :param step_detail_json:
    :return:
    '''
    if not isinstance(step_detail_json,dict):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None,
                                    _STEP_TYPE,'测试步骤不是字典')
    if _STEP_NAME not in step_detail_json:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None,
                                          _STEP_TYPE, '测试步骤不存在'+_STEP_NAME)
    if not isinstance(step_detail_json[_STEP_NAME],str):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None,
                                          _STEP_TYPE, '测试步骤' + _STEP_NAME+'不是string类型')
    step_name=step_detail_json[_STEP_NAME]

    content = _BLOCK + '${' + step_name + '}='
    if _STEP_WAIT in step_detail_json and step_detail_json[_STEP_WAIT] is not None:
        wait=step_detail_json[_STEP_WAIT]
        if not isinstance(wait,dict):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                              _STEP_TYPE, '测试步骤' + _STEP_WAIT + "不是dict类型")
        if _STEP_WAIT_RETRY not in wait:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                              _STEP_TYPE, '测试步骤' + _STEP_WAIT + "里"+ _STEP_WAIT_RETRY +"不存在")
        if _STEP_WAIT_RETRY_INTERVAL not in wait:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                              _STEP_TYPE, '测试步骤' + _STEP_WAIT + "里"+ _STEP_WAIT_RETRY_INTERVAL +"不存在")
        wait_retry=wait[_STEP_WAIT_RETRY]
        wait_retry_interval=wait[_STEP_WAIT_RETRY_INTERVAL]
        if not isinstance(wait_retry,str):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                              _STEP_TYPE, '测试步骤' + _STEP_WAIT + "里" + _STEP_WAIT_RETRY + "不是str类型")
        if not isinstance(wait_retry_interval,str):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                              _STEP_TYPE, '测试步骤' + _STEP_WAIT + "里" + _STEP_WAIT_RETRY_INTERVAL + "不是str类型")
        content+=_SEPERATE + _WAIT_KEYWORD + _SEPERATE + wait_retry + _SEPERATE + wait_retry_interval


    content+= _SEPERATE + _KEY_WORD
    if _INPUT not in step_detail_json:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                    _STEP_TYPE,_INPUT+'是必填字段')
    input_json=step_detail_json[_INPUT]
    if not isinstance(input_json,dict):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                    _STEP_TYPE,_INPUT + '字段' + str(input_json) +'不是字典')

    ##########################
    # method和url是必填字段
    #########################
    if _METHOD not in input_json:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                    _STEP_TYPE, '[' + _INPUT + '.' + _METHOD + ']是必填字段')
    if not typeUtils.is_str(input_json[_METHOD]):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                    _STEP_TYPE, '['+_INPUT+'.'+_METHOD + ']字段' +str(input_json[_METHOD]) +'不是string类型')
    if not _is_support_http_method(input_json[_METHOD]):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                    _STEP_TYPE, '['+_INPUT+'.'+_METHOD + ']字段'+input_json[_METHOD]+'不支持')

    content+= _SEPERATE + input_json[_METHOD]
    if _URL not in input_json:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                    _STEP_TYPE, '['+_INPUT+'.'+_URL + ']是必填字段')

    if not typeUtils.is_str(input_json[_URL]):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                    _STEP_TYPE, '['+_INPUT+'.'+_URL + ']字段不是string类型')
    content += _SEPERATE + input_json[_URL]

    #########################################
    # 如果存在，检测req_json,req_headers,params,data
    #########################################
    if _REQ_JSON in input_json and input_json[_REQ_JSON] is not None:
        if not typeUtils.is_json_or_json_str(input_json[_REQ_JSON]):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                _STEP_TYPE,'[' + _INPUT + '.' + _REQ_JSON + ']字段' + str(input_json[_REQ_JSON]) + '不是json类型或者能转成json的string类型')
        content += _SEPERATE + _REQ_JSON + '=' + typeUtils.covert_json_or_json_str_to_json_formate_str(input_json[_REQ_JSON])
    if _REQ_HEADER in input_json and input_json[_REQ_HEADER] is not None:
        if not typeUtils.is_json_or_json_str(input_json[_REQ_HEADER]):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                _STEP_TYPE,'[' + _INPUT + '.' + _REQ_HEADER + ']字段' + input_json[_REQ_HEADER] +'不是json类型或者能转成json的string类型')
        content += _SEPERATE + _REQ_HEADER + '=' + typeUtils.covert_json_or_json_str_to_json_formate_str(input_json[_REQ_HEADER])
    if _PARAMS in input_json and input_json[_PARAMS] is not None:
        if not typeUtils.is_json_or_json_str(input_json[_PARAMS]):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                _STEP_TYPE,'[' + _INPUT + '.' + _PARAMS + ']字段' + input_json[_PARAMS] +'不是json类型或者能转成json的string类型')
        content += _SEPERATE + _PARAMS + '=' + typeUtils.covert_json_or_json_str_to_json_formate_str(input_json[_PARAMS])
    if _DATA in input_json and input_json[_DATA] is not None:
        if not isinstance(input_json[_DATA],str):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                _STEP_TYPE,'[' + _INPUT + '.' + _DATA + ']字段' + input_json[_DATA] + '不是string类型')
        content += _SEPERATE + _DATA + '=' + input_json[_DATA]
    #如果data和req_json同时存在，提示错误
    if _DATA in input_json and _REQ_JSON in input_json and input_json[_DATA] is not None and input_json[_REQ_JSON] is not None:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
            _STEP_TYPE,'[' + _INPUT + '.' + _DATA + ']和['+ _INPUT + '.' + _REQ_JSON + ']字段不能同时存在')

    if _TIMEOUT in input_json and input_json[_TIMEOUT] is not None:
        timeout=input_json[_TIMEOUT]
        # 验证timeout
        if not typeUtils.is_int_or_int_str(timeout):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                _STEP_TYPE, '[' + _INPUT + '.' + _TIMEOUT + ']字段' + str(_TIMEOUT) + '不能转成数字')
        # 检查status code是合理的数据
        if not typeUtils.is_int_or_int_str(timeout):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                        _STEP_TYPE, '[' + _INPUT + '.' + _TIMEOUT + ']字段' + str(timeout) + '是不支持的')
        timeout_int = typeUtils.get_int_value(timeout)
        if timeout<=0:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                    _STEP_TYPE, '[' + _INPUT + '.' + _TIMEOUT + ']字段' + str(timeout) + '不是有效的时间')
        content += _SEPERATE + _TIMEOUT + '=${' + str(timeout_int) + '}'

    #########################################
    # 如果存在，检测status_code, resp_header,resp_body, resp_json, resp_body_contains, resp_json_contains
    #########################################
    if _EXPECT in step_detail_json and step_detail_json[_EXPECT] is not None:
        expect_json=step_detail_json[_EXPECT]
        if not isinstance(expect_json,dict):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                _STEP_TYPE,_EXPECT + '字段' + str(expect_json) + '不是字典')
        #验证status_code
        if _STATUS_CODE in expect_json and expect_json[_STATUS_CODE] is not None:
            status_code=expect_json[_STATUS_CODE]
            if not typeUtils.is_str(status_code) and not isinstance(status_code,int):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                _STEP_TYPE,'[' + _EXPECT + '.' + _STATUS_CODE + ']字段' + str(status_code) + '不是string类型或者int类型')
            #检查status code是合理的数据
            if not typeUtils.is_int_or_int_str(status_code):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                _STEP_TYPE,'[' + _EXPECT + '.' + _STATUS_CODE + ']字段' + str(status_code) + '是不支持的')
            status_code_int=typeUtils.get_int_value(status_code)
            if not _is_valid_http_status_code(status_code_int):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                        _STEP_TYPE,'[' + _EXPECT + '.' + _STATUS_CODE + ']字段' + str(status_code) + '不是标准的返回码')
            content+=_SEPERATE+ _STATUS_CODE+'=${'+ str(status_code_int) +'}'
        #验证resp_header
        if _RESP_HEADER in expect_json and expect_json[_RESP_HEADER] is not None:
            if not typeUtils.is_json_or_json_str(expect_json[_RESP_HEADER]):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                         _STEP_TYPE,'[' + _EXPECT + '.' + _RESP_HEADER + ']字段' + str(expect_json[_RESP_HEADER]) + '不是json类型或者能转成json的string类型')
            content += _SEPERATE + _RESP_HEADER + '=' + typeUtils.covert_json_or_json_str_to_json_formate_str(expect_json[_RESP_HEADER])
        #验证resp_body
        if _RESP_BODY in expect_json and expect_json[_RESP_BODY] is not None:
            if not typeUtils.is_str(expect_json[_RESP_BODY]):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                        _STEP_TYPE,'[' + _EXPECT + '.' + _RESP_BODY + ']字段' + str(expect_json[_RESP_BODY]) + '不是string类型')
            content += _SEPERATE + _RESP_BODY + '=' + expect_json[_RESP_BODY]
        #验证resp_json
        if _RESP_JSON in expect_json and expect_json[_RESP_JSON] is not None:
            if not typeUtils.is_json_or_json_str(expect_json[_RESP_JSON]):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                         _STEP_TYPE,'[' + _EXPECT + '.' + _RESP_JSON + ']字段' + str(expect_json[_RESP_JSON]) + '不是json类型或者能转成json的string类型')
            content += _SEPERATE + _RESP_JSON + '=' + typeUtils.covert_json_or_json_str_to_json_formate_str(expect_json[_RESP_JSON])
        # 验证resp_body_contains
        if _RESP_BODY_CONTAINS in expect_json and expect_json[_RESP_BODY_CONTAINS] is not None:
            if not typeUtils.is_str(expect_json[_RESP_BODY_CONTAINS]):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                    _STEP_TYPE,'[' + _EXPECT + '.' + _RESP_BODY_CONTAINS + ']字段' + str(expect_json[_RESP_BODY_CONTAINS]) + '不是string类型')
            content += _SEPERATE + _RESP_BODY_CONTAINS + '=' + expect_json[_RESP_BODY_CONTAINS]
        #验证resp_json_contains
        if _RESP_JSON_CONTAINS in expect_json and expect_json[_RESP_JSON_CONTAINS] is not None:
            if not typeUtils.is_json_or_json_str(expect_json[_RESP_JSON_CONTAINS]):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                        _STEP_TYPE,'[' + _EXPECT + '.' + _RESP_JSON_CONTAINS + ']字段' + str(expect_json[_RESP_JSON_CONTAINS]) + '不是json类型或者能转成json的string类型')
            content += _SEPERATE + _RESP_JSON_CONTAINS + '=' + typeUtils.covert_json_or_json_str_to_json_formate_str(expect_json[_RESP_JSON_CONTAINS])
        #验证expect_resp_body_regular_expression_contains
        if _RESP_BODY_REGULAR_EXPRESSION_CONTAINS in expect_json and expect_json[_RESP_BODY_REGULAR_EXPRESSION_CONTAINS] is not None:
            if not typeUtils.is_str(expect_json[_RESP_BODY_REGULAR_EXPRESSION_CONTAINS]):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                    _STEP_TYPE,'[' + _EXPECT + '.' + _RESP_BODY_REGULAR_EXPRESSION_CONTAINS + ']字段' + str(expect_json[_RESP_BODY_REGULAR_EXPRESSION_CONTAINS]) + '不是string类型')

            content += _SEPERATE + _RESP_BODY_REGULAR_EXPRESSION_CONTAINS + '=' + expect_json[_RESP_BODY_REGULAR_EXPRESSION_CONTAINS].replace('\\','\\\\\\\\')

        # 验证expect_resp_json_regular_expression_contains
        if _RESP_JSON_REGULAR_EXPRESSION_CONTAINS in expect_json and expect_json[_RESP_JSON_REGULAR_EXPRESSION_CONTAINS] is not None:
            expect_resp_json_regular_expression_contains=expect_json[_RESP_JSON_REGULAR_EXPRESSION_CONTAINS]
            if not typeUtils.is_dict_or_dict_str(expect_resp_json_regular_expression_contains):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,_STEP_TYPE,'[' + _EXPECT + '.' +
                    _RESP_JSON_REGULAR_EXPRESSION_CONTAINS + ']字段' + str(expect_resp_json_regular_expression_contains) + '不是字典类型')
            if isinstance(expect_resp_json_regular_expression_contains,dict):
                for item_key,item_value in expect_resp_json_regular_expression_contains.items():
                    item_value=str(item_value)
                    expect_resp_json_regular_expression_contains.update({item_key: item_value.replace('\\', '\\\\')})
                content += _SEPERATE + _RESP_JSON_REGULAR_EXPRESSION_CONTAINS + '=' + json.dumps(expect_resp_json_regular_expression_contains)
            if isinstance(expect_resp_json_regular_expression_contains,str):
                content += _SEPERATE + _RESP_JSON_REGULAR_EXPRESSION_CONTAINS + '=' + expect_resp_json_regular_expression_contains.replace('\\','\\\\\\\\')
        if _RESP_BODY_CONTAINS in expect_json and expect_json[_RESP_BODY_CONTAINS] is not None:
            expect_resp_body_contains=expect_json[_RESP_BODY_CONTAINS]
            if not typeUtils.is_str(expect_resp_body_contains):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                        _STEP_TYPE, '[' + _EXPECT + '.' + _RESP_BODY_CONTAINS + ']字段' + str(expect_resp_body_contains) + '不是string类型')
            content += _SEPERATE + _RESP_BODY_CONTAINS + '=' + expect_resp_body_contains.replace('\\','\\\\\\\\')
        if _RESP_JSON_SPECIAL_CONTAINS in expect_json and expect_json[_RESP_JSON_SPECIAL_CONTAINS] is not None:
            expect_resp_json_special_contains=expect_json[_RESP_JSON_SPECIAL_CONTAINS]
            if not typeUtils.is_json_or_json_str(expect_resp_json_special_contains):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                        _STEP_TYPE, '[' + _EXPECT + '.' + _RESP_JSON_SPECIAL_CONTAINS + ']字段' + str(expect_resp_json_special_contains) + '不是json类型或者能转成json的string类型')
            content += _SEPERATE + _RESP_JSON_SPECIAL_CONTAINS + '=' + typeUtils.covert_json_or_json_str_to_json_formate_str(expect_resp_json_special_contains)
    return statusObj.get_step_content(file_path, statusObj.STATUS_OK, suite_name, case_name, step_name,_STEP_TYPE, 'OK',content=content)

def _is_valid_http_status_code(code_data):
    if code_data in _HTTP_STATUS_CODE:
        return True
    return False

def _is_support_http_method(method):
    if method.upper() in _HTTP_METHOD:
        return True
    return False

def get_settings_content():
    '''
    获取robot文件依赖。
    :return: content
    '''
    content = 'Library  atApiBasicLibrary/supper.py\n'
    return content
