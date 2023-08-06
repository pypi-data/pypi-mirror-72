#coding:utf-8
import os

def list_current_file(path='.',type='all',suffix='',not_prefix=(('~','.'))):
    '''
    列出当前目录下的文件或者文件夹
    :param path: 默认当前目录
    :param type: 可选 file,folder,all 默认all
    :param suffix: 对文件夹和文件后缀过滤
    :param not_prefix: 对文件夹和文件前缀过滤，默认不要隐藏文件和临时文件
    :return:文件或文件夹的集合
    '''
    all_files = [os.path.join(path,x) for x in os.listdir(path)
                    if x.endswith(suffix) and not x.startswith(not_prefix)]
    if type =='all':
        return all_files
    elif type =="file":
        return [x for x in all_files if os.path.isfile(x) ==True]
    elif type == "folder":
        return [x for x in all_files if os.path.isdir(x) ==True]
    else:
        raise Exception(f"type: {type} not defined.")



def list_files_deep(path='.',suffix='',not_prefix=(('~','.'))):
    '''
    :param path: 默认当前目录 '.'
    :param suffix: 文件后缀，单个或者元组
    :param not_prefix: 单个或者元组,默认去掉隐藏文件和临时文件
    :return: 文件全路径集合
    '''
    files = []
    list_dir = os.walk(path)
    for maindir, subdir, all_file in list_dir:
        for filename in all_file:
            if filename.endswith(suffix) and not filename.startswith(not_prefix):
                files.append(os.path.join(maindir,filename))
    return files

