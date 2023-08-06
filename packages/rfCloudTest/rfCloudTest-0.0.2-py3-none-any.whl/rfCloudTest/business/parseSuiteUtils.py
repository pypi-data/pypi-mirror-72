'''
解析suite
解析
aa={
    "name":"dasadada",
    "variableFiles": ["variable所在文件名字，不需要后缀名"],
    "pythonFiles":[],
	"variables": {
		"url": "http://localhost:45000"
	},
	"case": [{
			"name": "测试用例1",
			"steps": [{
				"name": "测试步骤1",
				"type": "http",
				"input": {
					"method": "get",
					"url": "${url}/aa/bb/cc",
					"params": {
						"aa": "123",
						"bb": "sak"
					},
					"data": None,
					"req_json": "321",
					"req_headers": {
						"www": "sdsad",
						"NN": "dsaad"
					},
					"timeout": 45
				},
				"expect": {
					"expect_status_code": "${200}",
					"expect_resp_headers": {
						"aa": "213"
					},
					"expect_resp_body": "123",
					"expect_resp_json": "${None}",
					"expect_resp_body_contains": "${empty}",
					"expect_resp_json_contains": "${empty}"
				}
			}, {
				"name": "测试步骤2",
				"type": "http",
				"input": {
					"method": "get",
					"url": "${url}/aa/bb/cc",
					"params": {
						"aa": "123",
						"bb": "sak"
					},
					"data": None,
					"req_json": "321",
					"req_headers": {
						"www": "sdsad",
						"NN": "dsaad"
					},
					"timeout": 45
				},
				"expect": {
					"expect_status_code": "${200}",
					"expect_resp_headers": {
						"aa": "213"
					},
					"expect_resp_body": "123",
					"expect_resp_json": "${None}",
					"expect_resp_body_contains": "${empty}",
					"expect_resp_json_contains": "${empty}"
				}
			}]
		}]

}
'''
import importlib
from builtins import isinstance, str, set, list, print, exit, dict

from rfCloudTest.business import parseSetupTeardownUtils, parseTagUtils, parseCaseUtils, parseVariableUtils, \
    parseKeywordUtils

from rfCloudTest.utils import statusObj, mappingUtils

_VARIABLES='variables'
_KEYWORD='keywords'
_CASE='case'
_NAME='name'
_VARIABLE_FILES='variableFiles'
_PYTHON_FILES='pythonFiles'

def parse(file_path,suite_json):
    if _NAME not in suite_json:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, None, None, None, None, _NAME + '不在suite里')
    suite_name=suite_json[_NAME]
    if not isinstance(suite_name,str):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, None, None, None, None, 'suite里'+_NAME + '不是string类型')
    variable_content=None
    keyword_content=None
    variable_setting_content=None
    python_setting_content=None
    keyword_type=None
    suite_setup=None
    suite_teardown=None
    test_setup=None
    test_teardown=None
    tag=None
    case_content=''
    if not isinstance(suite_json,dict):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, suite_name + '不是字典类型')
    if _VARIABLES in suite_json:
        variable_result=parseVariableUtils.parse(file_path, suite_name,suite_json[_VARIABLES])
        if variable_result[statusObj.STATUS]==statusObj.STATUS_NOK:
            return variable_result
        variable_content=variable_result[statusObj.CONTENT]+'\n'
    if _VARIABLE_FILES in suite_json:
        variable_file_list=suite_json[_VARIABLE_FILES]
        if not isinstance(variable_file_list,list):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, _VARIABLE_FILES + '不是list类型')
        variable_setting_content=""
        for variable_file in variable_file_list:
            variable_setting_content+="Resource  ./"+variable_file +".robot\n"
    if _PYTHON_FILES in suite_json:
        python_file_list=suite_json[_PYTHON_FILES]
        if not isinstance(python_file_list,list):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, _PYTHON_FILES + '不是list类型')
        python_setting_content=""
        for python_file in python_file_list:
            python_setting_content+="Library  "+python_file +"\n"

    if _KEYWORD in suite_json:
        keyword_json_list=suite_json[_KEYWORD]
        keyword_result=parseKeywordUtils.parse(file_path, suite_name,keyword_json_list )
        if keyword_result[statusObj.STATUS]==statusObj.STATUS_NOK:
            return keyword_result
        keyword_type=keyword_result[statusObj.STEP_TYPE]
        keyword_content=keyword_result[statusObj.CONTENT]
    if parseSetupTeardownUtils.SUITE_SETUP in suite_json and suite_json[parseSetupTeardownUtils.SUITE_SETUP] is not None:
        suite_setup_result=parseSetupTeardownUtils.parse_suite_setup(file_path, suite_name, suite_json[parseSetupTeardownUtils.SUITE_SETUP])
        if suite_setup_result[statusObj.STATUS]==statusObj.STATUS_NOK:
            return suite_setup_result
        suite_setup=suite_setup_result[statusObj.CONTENT]
    if parseSetupTeardownUtils.SUITE_TEARDOWN in suite_json and suite_json[parseSetupTeardownUtils.SUITE_TEARDOWN] is not None:
        suite_teardown_result=parseSetupTeardownUtils.parse_suite_teardown(file_path, suite_name, suite_json[parseSetupTeardownUtils.SUITE_TEARDOWN])
        if suite_teardown_result[statusObj.STATUS]==statusObj.STATUS_NOK:
            return suite_teardown_result
        suite_teardown=suite_teardown_result[statusObj.CONTENT]
    if parseSetupTeardownUtils.TEST_SETUP in suite_json and suite_json[parseSetupTeardownUtils.TEST_SETUP] is not None:
        test_setup_result=parseSetupTeardownUtils.parse_test_setup(file_path, suite_name, suite_json[parseSetupTeardownUtils.TEST_SETUP])
        if test_setup_result[statusObj.STATUS]==statusObj.STATUS_NOK:
            return test_setup_result
        test_setup=test_setup_result[statusObj.CONTENT]
    if parseSetupTeardownUtils.TEST_TEARDOWN in suite_json and suite_json[parseSetupTeardownUtils.TEST_TEARDOWN] is not None:
        test_teardown_result=parseSetupTeardownUtils.parse_test_teardown(file_path, suite_name, suite_json[parseSetupTeardownUtils.TEST_TEARDOWN])
        if test_teardown_result[statusObj.STATUS]==statusObj.STATUS_NOK:
            return test_teardown_result
        test_teardown=test_teardown_result[statusObj.CONTENT]
    if parseTagUtils.TAG in suite_json and suite_json[parseTagUtils.TAG] is not None:
        tag_result=parseTagUtils.parse_suite_tag(file_path, suite_name, suite_json[parseTagUtils.TAG])
        if tag_result[statusObj.STATUS]==statusObj.STATUS_NOK:
            return tag_result
        tag=tag_result[statusObj.CONTENT]
    content = ''
    if _CASE in suite_json:
        if not isinstance(suite_json[_CASE],list):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None,  _CASE+'不是数组')
        cases=suite_json[_CASE]
        case_content+='*** Test Cases ***\n'
        suite_type=set([])
        for case in cases:
            case_result=parseCaseUtils.parse(file_path, suite_name,case)
            if case_result[statusObj.STATUS]==statusObj.STATUS_OK:
                case_content+=case_result[statusObj.CONTENT]+'\n'
                suite_type= suite_type | case_result[statusObj.STEP_TYPE]
            else:
                return case_result
        if keyword_type is not None:
            suite_type=suite_type.union(keyword_type)
        setting_content=get_setting_content_by_type(suite_type)
        if suite_setup is not None:
            setting_content+=suite_setup
        if suite_teardown is not None:
            setting_content+=suite_teardown
        if test_setup is not None:
            setting_content+=test_setup
        if test_teardown is not None:
            setting_content+=test_teardown
        if tag is not None:
            setting_content += tag
        if setting_content is not None:
            content+=setting_content
            if variable_setting_content is not None:
                content+=variable_setting_content
            if python_setting_content is not None:
                content += python_setting_content
        if variable_content is not None:
            content+=variable_content
        if keyword_content is not None:
            content+=keyword_content
        if case_content is not None:
            content += case_content
        return statusObj.get_step_content(file_path, statusObj.STATUS_OK, suite_name, None, None, suite_type, 'OK', content=content)
    else:
        if keyword_type is not None:
            content+=get_setting_content_by_type(keyword_type)
        else:
            content += '*** Settings ***\n'
        if variable_setting_content is not None:
            content += variable_setting_content
        if python_setting_content is not None:
            content += python_setting_content
        if suite_setup is not None:
            content +=suite_setup
        if suite_teardown is not None:
            content +=suite_teardown
        if test_setup is not None:
            content +=test_setup
        if test_teardown is not None:
            content +=test_teardown
        if tag is not None:
            content += tag
        if variable_content is not None:
            content+=variable_content
        if keyword_content is not None:
            content+=keyword_content
        if content=='':
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, 'NOK', content=content)
        return {statusObj.STATUS: statusObj.STATUS_OK,
                    statusObj.PATH: file_path,
                    statusObj.SUITE: suite_name,
                    statusObj.CASE: None,
                    statusObj.STEP: None,
                    statusObj.STEP_TYPE: None,
                    statusObj.ERROR_MSG: None,
                    statusObj.CONTENT: content
        }



def get_setting_content_by_type(case_type_set):
    '''
    :param case_type_set:
    :return:
    '''
    content = '*** Settings ***\n'
    content_list=[]
    for step_type in case_type_set:
        if step_type.lower() in mappingUtils._STEP_TYPE_MAPPING:
            module = importlib.import_module(mappingUtils.get_module_by_package_name(mappingUtils._STEP_TYPE_MAPPING[step_type.lower()]))
        else:
            module = importlib.import_module(mappingUtils.get_module_by_package_name(step_type))
        module_content=module.get_settings_content()
        if module_content is None or module_content.strip()=='' or module_content.strip() in content_list:
            continue
        content_list.append(module_content.strip())
        content+=module_content.strip()+'\n'
    return content

def get_suite_name_dict(file_path,suite_json,suite_name_dict):
    if _NAME not in suite_json:
        print(_NAME + '不在suite里')
        exit(-1)
    suite_name=suite_json[_NAME].strip()
    lst = []
    if suite_name in suite_name_dict:
        lst = suite_name_dict[suite_name]
    lst.append(file_path)
    suite_name_dict.update({suite_name:lst})
    return suite_name_dict