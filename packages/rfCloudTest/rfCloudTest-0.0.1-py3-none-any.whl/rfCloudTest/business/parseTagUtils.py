'''
["tag1","tag2"]
'''
from xforceCloudTestBasic import statusObj as statusObj
TAG="tag"

def parse_suite_tag(file_path, suite_name, suite_tag_list):
    if not isinstance(suite_tag_list,list):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, TAG + '不是list类型')
    if len(suite_tag_list)==0:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, TAG + '不允许是空list')
    content="Default Tags" + " " * 2
    for item in suite_tag_list:
        if not isinstance(item,str):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, TAG + '数组里必须都是string类型')
        content+=item + " "*2
    content+="\n"
    return statusObj.get_step_content(file_path, statusObj.STATUS_OK, suite_name, None, None, None, 'OK', content=content)

def parse_test_tag(file_path, suite_name, case_name, case_tag_list):
    if not isinstance(case_tag_list,list):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, TAG + '不是list类型')
    if len(case_tag_list)==0:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, TAG + '不允许是空list')
    content=" "*4 + "[Tags]" + " "*2
    for item in case_tag_list:
        if not isinstance(item,str):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, None, TAG + '数组里必须都是string类型')
        content+=item+ " "*2
    content+="\n"
    return statusObj.get_step_content(file_path, statusObj.STATUS_OK, suite_name, case_name, None, None, 'OK', content=content)
