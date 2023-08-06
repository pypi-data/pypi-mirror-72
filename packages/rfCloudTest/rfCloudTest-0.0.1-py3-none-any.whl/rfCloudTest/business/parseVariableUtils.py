'''
解析variables.
"variables": {
	"url": "http://localhost:45000",
	"数据库":{
	    "aa":"123",
	    "bb":"456",
	    "cc":789
	},
	"列表": [11,22,33]
}
'''

from xforceCloudTestBasic import statusObj as statusObj

_SEPERATE=" " * 2
_VARIABLES='variables'
def parse(file_path, suite_name,variable_json):
    if not isinstance(variable_json,dict):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, None, None, None, _VARIABLES +'不是字典类型')
    content='''*** Variables ***\n'''
    for variable_key,variable_value in variable_json.items():
        if isinstance(variable_value,str):
            content+='${' + variable_key + '}'+ _SEPERATE + variable_value +'\n'
        if isinstance(variable_value,list):
            content+='@{'+variable_key+'}'
            for list_item in variable_value:
                content+=_SEPERATE+list_item
            content +='\n'
        if isinstance(variable_value,dict):
            content += '&{' + variable_key + '}'
            for key,value in variable_value.items():
                content += _SEPERATE + key+'='+str(value)
            content += '\n'
    return statusObj.get_step_content(file_path, statusObj.STATUS_OK, suite_name, None, None, None, 'OK',content=content)
