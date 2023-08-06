'''
收集测试用例状态
'''
STATUS_OK=1
STATUS_NOK=0
STATUS='status'
ERROR_MSG='error_msg'
PATH='path'
SUITE='suite'
CASE='case'
STEP='step'
CONTENT='content'
STEP_TYPE='step_type'

def create_step_error_msg(file_path, suite_name,case_name,step_name,error_msg):
    error_message='[' + file_path + ']'
    if suite_name is not None and suite_name!='':
        error_message+='['+suite_name +']'
    if case_name is not None and case_name!='':
        error_message+='['+case_name +']'
    if step_name is not None and step_name!='':
        error_message +='['+step_name +']'
    error_message+=error_msg
    return error_message

def get_step_content(file_path, status, suite_name, case_name, step_name, step_type, error_msg, content=None):
    return {  STATUS: status,
              PATH: file_path,
              SUITE: suite_name,
              CASE: case_name,
              STEP: step_name,
              STEP_TYPE: step_type,
              ERROR_MSG:create_step_error_msg(file_path, suite_name,case_name,step_name,error_msg),
              CONTENT:content
          }


