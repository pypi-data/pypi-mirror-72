import os
import sys
import shutil
def get_all_files(dir):
    '''
    获取所有文件夹下的所有文件的绝对路径。
    :param dir:
    :return: list,如果是空，返回空列表。
    '''
    file_list = []
    for root_path, dirs, files in os.walk(dir):
        for filename in files:
            fullname = os.path.join(root_path, filename)
            if fullname.endswith('json') or fullname.endswith('yaml'):
                file_list.append(fullname)
    return file_list

def create_directory(dir):
    '''
    创建文件夹。如果文件夹存在，不创建文件夹。
    :param dir: string类型，相对路径或者绝对路径。
    '''
    if os.path.isfile(dir):
        print("有相同名字的文件: " + str(dir))
        sys.exit(-1)
    if not os.path.exists(dir):
        os.mkdir(dir)
        print('创建文件夹: ' + dir)

def create_file(file_path, content):
    '''
    创建文件。如果文件存在，完全替换文件。
    :param file_path:
    :return:
    '''
    if not os.path.exists(file_path):
        f = open(file_path, mode="w", encoding="utf-8")
        f.write(content)
        f.close()
        return
    if os.path.isdir(file_path):
        print("有相同名字的文件夹: " + str(file_path))
        sys.exit(-1)
    os.remove(file_path)
    f = open(file_path, mode="w", encoding="utf-8")
    f.write(content)
    f.close()

def remove(file_path):
    shutil.rmtree(file_path)

def remove_all_files(dir):
    for item in os.listdir(dir):
        file_path = dir + "/" + item
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            remove_all_files(file_path)
