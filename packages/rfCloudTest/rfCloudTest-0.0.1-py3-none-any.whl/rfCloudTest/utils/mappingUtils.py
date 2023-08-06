import importlib

_HTTP_TYPE = 'http'
_MYSQL_TYPE = 'mysql'
_ROBOT_FRAMEWORK_TYPE = 'rft'
_PYTHON_TYPE = 'python'
_ROBOT_TYPE = 'robot'
_KEYWORD_TYPE = 'keyword'
_MYSQL_UPDATE_TYPE = 'mysql-update'
_HTTP_PAIR_TYPE = 'http-pair'
_LOOP_TYPE = 'loop'
_BROWSER_UI = "browser-ui"
_BROWSER_UI_BASIC = "browser-ui-basic"
# _STEP_TYPE_MAPPING 的key都必须是小写的
_STEP_TYPE_MAPPING = {
    _HTTP_TYPE: 'xfctRftHttpStep',
    _MYSQL_TYPE: 'xfctRftMysqlStep',
    _ROBOT_FRAMEWORK_TYPE: 'xfctRftStep',
    _PYTHON_TYPE: 'xfctRftPythonStep',
    _ROBOT_TYPE: 'xfctRobotStep',
    _KEYWORD_TYPE: 'xfctKeywordStep',
    _MYSQL_UPDATE_TYPE: 'xfctRftMysqlUpdateStep',
    _HTTP_PAIR_TYPE: 'xfctRftPairHttpStep',
    _LOOP_TYPE: 'xfctRftLoopStep',
    _BROWSER_UI: 'xfctBrowserUiStep',
    _BROWSER_UI_BASIC: 'xfctBrowserUiBasicStep'

}


def parse_step(file_path, suite_name, case_name, step_type, step_detail_json):
    if step_type.lower() in _STEP_TYPE_MAPPING:
        module = importlib.import_module(get_module_by_package_name(_STEP_TYPE_MAPPING[step_type.lower()]))
        return module.parse(file_path, suite_name, case_name, step_detail_json)

    module = importlib.import_module(get_module_by_package_name(step_type))
    return module.parse(file_path, suite_name, case_name, step_detail_json)


def get_module_by_package_name(package_name):
    '''
    通过模板名获取依赖的参数。比如包名叫abc,对外暴露的就是abcMain.所以要import abc.abcMain.
    :param package_name:
    :return:
    '''
    return package_name + '.' + package_name + 'Main'


def check_step_type(step_type):
    try:
        if step_type.lower() in _STEP_TYPE_MAPPING:
            module = importlib.import_module(get_module_by_package_name(_STEP_TYPE_MAPPING[step_type.lower()]))
            return True
        module = importlib.import_module(get_module_by_package_name(step_type))
        return True
    except Exception as e:
        print(str(e))
        print('测试步骤的类型' + step_type + '不存在')
        return False
