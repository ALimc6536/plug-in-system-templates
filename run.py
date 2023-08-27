import os,sys,json
from colorama import Fore, Back, Style # 文字颜色
from flask import Flask,request
app=Flask(__name__) 
#限制log输出
import logging
app.logger.disabled = True
Logger = logging.getLogger('werkzeug')
Logger.disabled = True
import traceback # 详细报错:traceback.format_exc()
import psutil # 系统进程
# 修饰器
class tool:
    pluginFunction={
        'request':[],
        'notice':[],
        'message':[],
        'message_sent':[],
        'meta_event':[],
        'test':0
    }
    class mtypeError(Exception):
        def __init__(self, ei):
            super().__init__(self)
            self.errorinfo=ei
        def __str__(self):
            return self.errorinfo
    def m(self,mtype):
        '''
        \nmtype:
        \n    request 请求
        \n    notice 通知
        \n    message 收到消息
        \n    message_sent 发送消息
        \n    meta_event 元事件
        '''
        if mtype not in self.pluginFunction: raise self.mtypeError('未知的mtype：%s'%mtype)
        self.pluginFunction['test']+=1
        def d(fc):
            self.pluginFunction[mtype].append(fc)
            return fc
        return d
t=tool()
if __name__ == '__main__':
    def pri(cue:str,errinfo:str='',color:str='red'):
        if color == 'red':
            print(Fore.RED+'%s->\n%s%s%s'%(cue ,Fore.WHITE ,Back.RED ,errinfo))
        else:
            exec('print(Fore.%s+cue)'%color.upper())
        print(Style.RESET_ALL,end='')
    os.chdir("./") # 设置项目路径
    os.system('cls')# 清屏
    cwd=os.getcwd()# 脚本所在目录
    #-----------插件加载-----------
    if True:
        if not os.path.isdir('plugin'):os.mkdir('plugin')
        allPluginNames=sorted(os.listdir('plugin'))#获取全部拓展文件完整名称并排序
        for i in allPluginNames:
            fileNameS = os.path.splitext(i)
            if fileNameS[-1] == '.py':
                for ii in fileNameS[0]:
                    if ord(ii) not in range(ord('a'),ord('z')+1):
                        if ord(ii) not in range(ord('A'),ord('Z')+1):
                            if ii not in '_-':
                                if ord(fileNameS[0][0]) in range(ord('0'),ord('9')+1):
                                    pri('[%s] 加载失败'%i, '文件名只允许a-z,A-Z,-,_且不可以数字开头 但是出现了"%s"'%ii)
                                    break
                else:
                    try:
                        exec('''from plugin.%s import *'''%fileNameS[0]) # 导入
                    except:
                        pri('[%s] 加载失败'%i, traceback.format_exc())
                    else:
                        pri('[%s] 加载成功'%i, color='green')
    input('end')