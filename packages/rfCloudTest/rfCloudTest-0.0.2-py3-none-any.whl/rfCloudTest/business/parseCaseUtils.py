'''
解析测试用例.
处理类似下面的东西
{
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
				"expect_resp_headers_contains": {
					"aa": "213"
				},
				"expect_resp_body": "123",
				"expect_resp_json": "${None}",
				"expect_resp_body_contains": "${empty}",
				"expect_resp_json_contains": "${empty}"
			}
		},{
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
		}
	]
}
'''
from builtins import isinstance, dict, str, list, range, len, tuple, set

import itertools

from rfCloudTest.business import parseSetupTeardownUtils
from rfCloudTest.business import parseTagUtils
from rfCloudTest.utils import statusObj, mappingUtils

_CASE_NAME='name'
_STEPS='steps'
_STEP_NAME='name'
_STEP_TYPE='type'


def parse(file_path, suite_name, case_json):
    '''

    :param suite_name:
    :param template:
    :return:
    '''
    if not isinstance(case_json,dict):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, '测试用例不是字典类型')
    if _CASE_NAME not in case_json:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, '测试用例不包含' + _CASE_NAME)

    if not isinstance(case_json[_CASE_NAME],str):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, '测试用例' + _CASE_NAME + '必须是string类型')
    case_name=case_json[_CASE_NAME]
    if _STEPS not in case_json:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, '不包含' + _STEPS)
    if not isinstance(case_json[_STEPS],list):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, _STEPS + "必须是数组")
    if len(case_json[_STEPS])==0:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, _STEPS + "必须是有数据的数组")
    steps=case_json[_STEPS]

    step_type_list=[]
    content = case_name + '\n'
    if parseSetupTeardownUtils.CASE_TEST_SETUP in case_json and case_json[parseSetupTeardownUtils.CASE_TEST_SETUP] is not None:
        setup_result= parseSetupTeardownUtils.parse_case_setup(file_path, suite_name, case_name, case_json[
            parseSetupTeardownUtils.CASE_TEST_SETUP])
        if setup_result[statusObj.STATUS]== statusObj.STATUS_NOK:
            return setup_result
        content+=setup_result[statusObj.CONTENT]
    if parseSetupTeardownUtils.CASE_TEST_TEARDOWN in case_json and case_json[parseSetupTeardownUtils.CASE_TEST_TEARDOWN] is not None:
        teardown_result= parseSetupTeardownUtils.parse_case_teardown(file_path, suite_name, case_name, case_json[
            parseSetupTeardownUtils.CASE_TEST_TEARDOWN])
        if teardown_result[statusObj.STATUS]== statusObj.STATUS_NOK:
            return teardown_result
        content+=teardown_result[statusObj.CONTENT]
    if parseTagUtils.TAG in case_json and case_json[parseTagUtils.TAG] is not None:
        tag_result= parseTagUtils.parse_test_tag(file_path, suite_name, case_name, case_json[parseTagUtils.TAG])
        if tag_result[statusObj.STATUS]== statusObj.STATUS_NOK:
            return tag_result
        content+=tag_result[statusObj.CONTENT]
    pair_step_content_list_flag=False
    pair_step_content_list=[]
    for step_index in range(len(steps)):
        if not isinstance(steps[step_index],dict):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, '第' + str(step_index + 1) + '步测试步骤不是字典')
        step_detail_dict=steps[step_index]
        if _STEP_NAME not in step_detail_dict:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, '第' + str(step_index + 1) + '步测试步骤不存在' + _STEP_NAME)
        if not isinstance(step_detail_dict[_STEP_NAME],str):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, '第' + str(step_index + 1) + '步测试步骤' + _STEP_NAME + '不是string类型')
        step_name=step_detail_dict[_STEP_NAME]
        if _STEP_TYPE not in step_detail_dict:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, None, '第' + str(step_index + 1) + '步测试步骤不存在' + _STEP_TYPE)
        if not isinstance(step_detail_dict[_STEP_TYPE],str):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, None, '第' + str(step_index + 1) + '步测试步骤' + _STEP_TYPE + '不是string类型')
        if not mappingUtils.check_step_type(step_detail_dict[_STEP_TYPE]):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, None, '第' + str(step_index + 1) + '步测试步骤不支持测试类型' + step_detail_dict[_STEP_TYPE]) + ',或者没有引入该类型测试包'
        step_result= mappingUtils.parse_step(file_path, suite_name, case_name, step_detail_dict[_STEP_TYPE], step_detail_dict)
        if step_result[statusObj.STATUS]== statusObj.STATUS_NOK:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, step_detail_dict[_STEP_TYPE], '第' + str(step_index + 1) + '步测试步骤: ' + step_result[
                statusObj.ERROR_MSG])
        step_result_content=step_result[statusObj.CONTENT]
        if isinstance(step_result_content,str):
            content+= step_result[statusObj.CONTENT] + '\n'
        if isinstance(step_result_content, list):
            pair_step_content_list_flag=True
            content+='%s\n'
            pair_step_content_list.append(step_result_content)
        if isinstance(step_detail_dict[_STEP_TYPE],str):
            step_type_list.append(step_detail_dict[_STEP_TYPE].lower())
        elif isinstance(step_detail_dict[_STEP_TYPE],list):
            for step_detail_dict_step_type_item in step_detail_dict[_STEP_TYPE]:
                step_type_list.append(step_detail_dict_step_type_item[_STEP_TYPE].lower())
        else:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                              step_detail_dict[_STEP_TYPE], '第' + str(step_index + 1) + '步测试步骤: type类型异常')
    if pair_step_content_list_flag:
        content_list=[]
        case_index=1
        if len(pair_step_content_list)==1:
            tmp_pair_step_list=pair_step_content_list[0]
            for tmp_pair_step_list_item in tmp_pair_step_list:
                tmp_content=content.replace(case_name, case_name + str(case_index))
                case_index+=1
                content_list.append(tmp_content % tmp_pair_step_list_item)
        else:
            lst = []
            length = len(pair_step_content_list)
            for x in itertools.product(*pair_step_content_list):
                tmp_list = []
                for i in range(length):
                    tmp_list.append(x[i])
                lst.append(tmp_list)
            for item in lst:
                tmp_content=content.replace(case_name, case_name+str(case_index))
                case_index += 1
                content_list.append(tmp_content % tuple(item))
        all_content=''
        for content_list_item in content_list:
            all_content+=content_list_item
        return statusObj.get_step_content(file_path, statusObj.STATUS_OK, suite_name, case_name, step_name, set(step_type_list), 'OK', content=all_content)
    else:
        return statusObj.get_step_content(file_path, statusObj.STATUS_OK, suite_name, case_name, step_name, set(step_type_list), 'OK', content=content)
