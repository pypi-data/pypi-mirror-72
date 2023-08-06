'''
{
   "keyword":[{
        "name": "keyword名字",
        "args":["",""]
        "steps":[
            {
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
			}
        ]
   },
   {
        "name": "keyword名字",
        "steps":[
            {

            },
            {
            }
        ]
   }、
   ]
}
'''
from builtins import str, isinstance, range, dict, len, set, list
from rfCloudTest.utils import statusObj, mappingUtils

_KEYWORD_NAME='name'
_STEPS='steps'
_STEP_NAME='name'
_STEP_TYPE='type'
_KEYWORD_ARGUMENTS="args"


def parse(file_path, suite_name, keyword_json_list):
    content='\n*** Keywords ***\n'
    if not isinstance(keyword_json_list,list ):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, "keyword不是数组类型")
    keyword_step_list=[]

    for keyword_json in keyword_json_list:
        if _KEYWORD_NAME not in keyword_json:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, "keyword里'"+_KEYWORD_NAME+"'不存在")
        keyword_name=keyword_json[_KEYWORD_NAME]
        if _STEPS not in keyword_json:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, keyword_name, None, None,
                                              'keyword:'+keyword_name+'不包含' + _STEPS)
        if not isinstance(keyword_json[_STEPS], list):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, keyword_name, None, None,
                                              'keyword:'+keyword_name+'的'+_STEPS + "必须是数组")
        if len(keyword_json[_STEPS]) == 0:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, keyword_name, None, None,
                                              'keyword:'+keyword_name+'的'+_STEPS + "必须是有数据的数组")
        steps = keyword_json[_STEPS]
        step_name_list = []
        content += keyword_name + '\n'
        if _KEYWORD_ARGUMENTS in keyword_json:
            if not isinstance(keyword_json[_KEYWORD_ARGUMENTS],list):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, keyword_name, None, None,
                                                  'keyword:' + keyword_name + '的' + _KEYWORD_ARGUMENTS + "必须是数组")
            content+="    [Arguments]"
            for argument_item in keyword_json[_KEYWORD_ARGUMENTS]:
                content+="  " + argument_item
            content+="\n"
        for step_index in range(len(steps)):
            if not isinstance(steps[step_index], dict):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, keyword_name, None, None,
                                                  '第' + str(step_index + 1) + '步测试步骤不是字典')
            step_detail_dict = steps[step_index]
            if _STEP_NAME not in step_detail_dict:
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, keyword_name, None, None,
                                                  'keyword:'+keyword_name+'的第' + str(step_index + 1) + '步测试步骤不存在' + _STEP_NAME)
            if not isinstance(step_detail_dict[_STEP_NAME], str):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, keyword_name, None, None,
                                                  'keyword:'+keyword_name+'的第' + str(step_index + 1) + '步测试步骤' + _STEP_NAME + '不是string类型')
            step_name = step_detail_dict[_STEP_NAME]
            if step_name in step_name_list:
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, keyword_name, step_name,
                            None, '第' + str(step_index + 1) + '步测试步骤' + step_name + '重复了')
            if _STEP_TYPE not in step_detail_dict:
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, keyword_name, step_name,
                        None, 'keyword:'+keyword_name+'的第' + str(step_index + 1) + '步测试步骤不存在' + _STEP_TYPE)
            if not isinstance(step_detail_dict[_STEP_TYPE], str):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, keyword_name, step_name,
                        None, 'keyword:'+keyword_name+'的第' + str(step_index + 1) + '步测试步骤' + _STEP_TYPE + '不是string类型')
            if not mappingUtils.check_step_type(step_detail_dict[_STEP_TYPE]):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, keyword_name, step_name,
                        None, 'keyword:'+keyword_name+'的第' + str(step_index + 1) + '步测试步骤不支持测试类型' + step_detail_dict[_STEP_TYPE]) + ',或者没有引入该类型测试包'
            step_result = mappingUtils.parse_step(file_path, suite_name, keyword_name, step_detail_dict[_STEP_TYPE],step_detail_dict)
            if step_result[statusObj.STATUS] == statusObj.STATUS_NOK:
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, keyword_name, step_name,
                                    step_detail_dict[_STEP_TYPE],'keyword:'+keyword_name+'的第' + str(step_index + 1) + '步测试步骤: ' + step_result[statusObj.ERROR_MSG])
            content += step_result[statusObj.CONTENT] + '\n'
            keyword_step_list.append(step_detail_dict[_STEP_TYPE].lower())
            if step_index==len(steps)-1:
                content+="    [Return]  ${" + step_name +"}\n"

    return statusObj.get_step_content(file_path, statusObj.STATUS_OK, suite_name, None, None, set(keyword_step_list),'OK', content=content)

# aa=[{
#         "name": "keyword11",
#         "steps":[
#             {
# 				"name": "测试步骤1",
# 				"type": "http",
# 				"input": {
# 					"method": "get",
# 					"url": "${url}/aa/bb/cc",
# 					"params": {
# 						"aa": "123",
# 						"bb": "sak"
# 					},
# 					"data": None,
# 					"req_json": "321",
# 					"req_headers": {
# 						"www": "sdsad",
# 						"NN": "dsaad"
# 					},
# 					"timeout": 45
# 				},
# 				"expect": {
# 					"expect_status_code": "${200}",
# 					"expect_resp_headers": {
# 						"aa": "213"
# 					},
# 					"expect_resp_body": "123",
# 					"expect_resp_json": "${None}",
# 					"expect_resp_body_contains": "${empty}",
# 					"expect_resp_json_contains": "${empty}"
# 				}
# 			}, {
# 				"name": "测试步骤2",
# 				"type": "http",
# 				"input": {
# 					"method": "get",
# 					"url": "${url}/aa/bb/cc",
# 					"params": {
# 						"aa": "123",
# 						"bb": "sak"
# 					},
# 					"data": None,
# 					"req_json": "321",
# 					"req_headers": {
# 						"www": "sdsad",
# 						"NN": "dsaad"
# 					},
# 					"timeout": 45
# 				},
# 				"expect": {
# 					"expect_status_code": "${200}",
# 					"expect_resp_headers": {
# 						"aa": "213"
# 					},
# 					"expect_resp_body": "123",
# 					"expect_resp_json": "${None}",
# 					"expect_resp_body_contains": "${empty}",
# 					"expect_resp_json_contains": "${empty}"
# 				}
# 			}
#         ]
#    },
#    {
#         "name": "keyword 22",
#         "args":["${asdasd}","${dsadaddsa}"],
#         "steps":[
#             {
# 				"name": "测试步骤1",
# 				"type": "http",
# 				"input": {
# 					"method": "get",
# 					"url": "${url}/aa/bb/cc",
# 					"params": {
# 						"aa": "123",
# 						"bb": "sak"
# 					},
# 					"data": None,
# 					"req_json": "321",
# 					"req_headers": {
# 						"www": "sdsad",
# 						"NN": "dsaad"
# 					},
# 					"timeout": 45
# 				},
# 				"expect": {
# 					"expect_status_code": "${200}",
# 					"expect_resp_headers": {
# 						"aa": "213"
# 					},
# 					"expect_resp_body": "123",
# 					"expect_resp_json": "${None}",
# 					"expect_resp_body_contains": "${empty}",
# 					"expect_resp_json_contains": "${empty}"
# 				}
# 			}, {
# 				"name": "测试步骤2",
# 				"type": "http",
# 				"input": {
# 					"method": "get",
# 					"url": "${url}/aa/bb/cc",
# 					"params": {
# 						"aa": "123",
# 						"bb": "sak"
# 					},
# 					"data": None,
# 					"req_json": "321",
# 					"req_headers": {
# 						"www": "sdsad",
# 						"NN": "dsaad"
# 					},
# 					"timeout": 45
# 				},
# 				"expect": {
# 					"expect_status_code": "${200}",
# 					"expect_resp_headers": {
# 						"aa": "213"
# 					},
# 					"expect_resp_body": "123",
# 					"expect_resp_json": "${None}",
# 					"expect_resp_body_contains": "${empty}",
# 					"expect_resp_json_contains": "${empty}"
# 				}
# 			}
#         ]
#    }
#    ]
#
# print(parse('111/22','kaikai',aa))
