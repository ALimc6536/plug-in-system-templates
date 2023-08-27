#导入库
try:
    import json
    from pickletools import int4
    from tkinter import N
    from operator import concat
    from sqlite3 import connect
    from tkinter import E
    import datetime
    import re
    import os
    import time
    import _thread as thread # 多线程 thread.start_new_thread(def, ())
    import msvcrt
    import psutil
    import traceback # 详细报错:traceback.format_exc()
    import requests # 网络
    requests.packages.urllib3.disable_warnings()
    import random # 随机
    import subprocess # 复制
    import atexit
    from multiprocessing import Process
    if os.name == "nt":
        os.system("")
except Exception as err :
    print('导入库失败-> ', traceback.format_exc())
    msvcrt.getwche()
    exit()

# 格式化时间
def timestr(format='%Y-%m-%d %H:%M:%S')->str:
    '''
    获取格式化时间
    '%Y-%m-%d %H:%M:%S'
    '''
    format = format.replace('%年%','%Y').replace('%月%','%m').replace('%日%',r'%d').replace('%时%','%H').replace('%分%','%M').replace('%秒%','%S')
    return datetime.datetime.now().strftime(format)

#读入文件
def getfile(path:str='')->str:
    if os.path.exists(path) == False:
        raise Exception('%s文件不存在'%path)
    with open(path, "r", encoding = "utf-8") as file:
        return str(file.read())
#写出文件
def setfile(path:str='', text:str='')->None:
    with open(path, "w", encoding = "utf-8") as file:
        file.write(text)
#追加文本
def addfile(path:str='', text:str='')->str:
    with open(path, "a", encoding = "utf-8") as file:
        file.write(text)

# log输出
def log(*info,log:bool=True):
    text = timestr('[%Y-%m-%d %H:%M:%S] ')
    for i in info:
        text += str(i)
    global logs
    logs.append(text)
    if len(logs) > 200:
        del logs[0]
    if log:
        if not os.path.exists('.\\log\\'):
            os.mkdir('.\\log\\')
        addfile('.\\log\\%s.log'%timestr('%Y-%m-%d'), text+'\n')

#生成颜色文本
def color(text:str, type:int=0, FV:int=None, BC:int=None)->str:
    """
    在控制台输出彩色文本

    参数:
        *text: str -> 你可以输入多个显示文本
        end: str -> 结尾字符(不会加到颜色文本中)默认'\n'
        type: int -> 显示方式: 0(终端默认设置),1(高亮显示),22(非高亮显示),4(使用下划线),24(去下划线),5(闪烁),25(去闪烁),7(反白显示),27(非反显),8(不可见),28(可见
        FV: int -> 前景色: 30(黑色)、31(红色)、32(绿色)、 33(黄色)、34(蓝色)、35(梅色)、36(青色)、37(白色)
        BC: int -> 背景色: 40(黑色)、41(红色)、42(绿色)、 43(黄色)、44(蓝色)、45(梅色)、46(青色)、47(白色)
    返回: None
    """
    return "\033[%s;%s;%sm%s\033[0m" % (str(type), str(FV), str(BC), text)
# get提交
def geturl(url:str, data:dict={}, timeout:int=2)->any:
    '''
    自动加:"?"
    '''
    getdata = ''
    if data == {} :
        geturl = url
    else : 
        geturl = url+'?'
        for i in data:
            getdata += '%s=%s&'%(i,data[i])
        del getdata[-1]
    geturl += getdata
    return requests.get(geturl, timeout=timeout).text.replace("true", "True").replace("false", "False").replace("null", "None")

#正则表达式统计字符串内每个字符的位置
def positionOfCharactersWithinString(input:str, str:str)->dict:
    starts = [each.start() for each in re.finditer(str, input)] # [0, 8]
    ends = [start + len(str) - 1 for start in starts]
    span = [(start, end) for start, end in zip(starts, ends)]
    return {'starts' : starts, 'ends' : ends, 'span' : span}

#在列表中查找字符串
def setstrlistInt(text:str, list:list)->int:
    for i in range(len(list)):
        if text == list[i]:
            return i
    return -1

#取文本中间
def textzhong(text, q, h):
    return text[text.find(q):text.find(h)].replace(q,"")

#取出第一个正则表达式匹配的文本
def getStrReText(str:str, Re:str)->str:
    return re.compile(Re).search(str).group()

#格式化字典
def dictdumps(dict:dict,indent:int=4,sort_keys:bool=False,separators:tuple=(', ', ': '))->str:
    '''
    dict:dict 字典
    indent:int=4 缩进
    sort_keys:bool=False 排序
    '''
    json.dumps(dict, sort_keys=sort_keys, indent=indent, separators=separators)

#生成随机字符串
def randomtext(quantity:int,number:int=1,separated:str='')->str:
    '''
    参数:
        quantity:int 每次生成数量
        number:int 生成次数
        separated:str 分隔字符
    '''
    list = []
    for i in range(number):
        list.append(''.join(random.sample('q0w1e2r3t4y5u6i7o8p9lkjhgfdsazxcvbnm'*(quantity%36+1),quantity)))
    return separated.join(list)

#获取目录下文件夹
def getFoinefList(ml:str)->list:
    '''
    获取目录下文件夹
    '''
    if ml[-1] != "\\" or ml[-1] != "//" :
        mlm = ml+"\\"
    else :
        mlm = ml
    mlm = mlm.replace('/','\\')
    list = []
    path = os.listdir(mlm)
    for i in path:
        if os.path.isdir(mlm + i):
            list.append(str(i))
    return list

#获取目录下文件
def getFoinefFileList(ml:str)->list:
    '''
    获取目录下文件
    '''
    if ml[-1] != "\\" or ml[-1] != "//" :
        mlm = ml+"\\"
    else :
        mlm = ml
    mlm = mlm.replace('/','\\')
    list = []
    path = os.listdir(mlm)
    for i in path:
        if os.path.file(mlm + i):
            list.append(str(i))
    return list

# 复制文件到指定文件夹
def mycopyfile(srcfile:str,dstpath:str):
    '''
    srcfile:str 文件位置
    dstpath:str 目的位置
    '''
    subprocess.check_output('copy %s %s '%(srcfile,dstpath), shell=True)

# 推迟一段时间运行的函数
def sleepDefFunction(sleeptime:float,deffunction,param:tuple):
    '''
    sleeptime:int 时间，秒
    deffunction 运行的函数
    '''
    def a (b:float,c,d:tuple):
        time.sleep(b)
        thread.start_new_thread(c, d)
    thread.start_new_thread(a, (sleeptime,deffunction,param))

# 推迟一段时间运行的代码段
def sleepStrFunction(sleeptime:float,deffunction:str):
    '''
    sleeptime:int 时间，秒
    deffunction 运行的函数
    '''
    def a (b:float,c:str):
        time.sleep(b)
        try:
            exec(c)
        except Exception as err :
            raise Exception(err)
    thread.start_new_thread(a, (sleeptime,deffunction))

def testfunction():
    print(1654646)