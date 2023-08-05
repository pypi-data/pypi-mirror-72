#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     fileMonitor
   Description :
   Author :       CoolCat
   date：          2019/1/3
-------------------------------------------------
   Change Activity:
                   2019/1/3:
-------------------------------------------------
"""
__author__ = 'CoolCat'

from watchdog.observers import Observer
from watchdog.events import *
import time
import sys
import argparse


class FileEventHandler(FileSystemEventHandler):

    def __init__(self):
        FileSystemEventHandler.__init__(self)
        self.showDir = False
        self.unspyDirs = []
        pass

    def on_created(self, event):  # 文件创建
        for p in self.unspyDirs:
            if p in event.src_path:
                return
        self.print_str(1, event.is_directory, event.src_path)

    def on_deleted(self, event):  # 文件删除
        for p in self.unspyDirs:
            if p in event.src_path:
                return
        self.print_str(2, event.is_directory, event.src_path)

    def on_moved(self, event):  # 文件移动
        for p in self.unspyDirs:
            if p in event.src_path:
                return
        self.print_str(3, event.is_directory, "from {} to {}".format(event.src_path,event.dest_path))

    def on_modified(self, event):  # 文件修改
        for p in self.unspyDirs:
            if p in event.src_path:
                return
        self.print_str(4, event.is_directory, event.src_path)

    def print_str(self, on_type=int, is_directory=bool, src_path=str):
        if on_type == 1:
            action = u'created'
            colour = u'5;32m'  # 文件创建显示绿色
        if on_type == 2:
            action = u'deleted'
            colour = u'0;31m'  # 文件删除显示红色
        if on_type == 3:
            action = u'moved'
            colour = u'0;36m'  # 文件移动显示青色
        if on_type == 4:
            action = u'modified'
            colour = u'0;34m'  # 文件修改显示蓝色
        f2d = u'file'
        if is_directory:
            f2d = u'directory'
        pstr = time.strftime(u'[%H:%M:%S]:') + u"\033[%s%s\033[0m" % (
        colour, u"{0} {1}:{2}".format(f2d, action, src_path))

        if is_directory:
            if self.showDir:
                print(pstr)
        else:
            print(pstr)


def logo():
    print("""    ______ _  __       __  ___               _  __              
   / ____/(_)/ /___   /  |/  /____   ____   (_)/ /_ ____   _____
  / /_   / // // _ \ / /|_/ // __ \ / __ \ / // __// __ \ / ___/
 / __/  / // //  __// /  / // /_/ // / / // // /_ / /_/ // /    
/_/    /_//_/ \___//_/  /_/ \____//_/ /_//_/ \__/ \____//_/     
Github:https://github.com/TheKingOfDuck/FileMonitor
                               Coding by {} Version:{}""".format("CoolCat","1.0"))

def getOpts():

    parser = argparse.ArgumentParser(usage="\n\tfilemon -p ./wwwroot -hp ./wwwroot/runtime -sd no")
    parser.add_argument("-p" , metavar=' /path/spydir',type=str, required=False, help="Spy on the file directory")
    parser.add_argument("-hp", metavar='/path/notspydir', type=str, required=False,default="TheKingOfDuck", help="Not spy on the file directory")
    parser.add_argument("-sd", metavar='no', type=str, required=False, choices=["yes","no"], default="no", help="Show directory or not")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # 输出提示
    logo()

    #获取命令行参数
    args = getOpts()
    if args.p == None:
        # 获取输入,为兼容 python2 不做汉化
        if sys.version_info.major == 2:
            try:
                spyDir = raw_input(time.strftime('[%H:%M:%S]:') + "Please enter a directory:")
                unspyDir = raw_input(time.strftime('[%H:%M:%S]:') + "Unnecessary directory:")
                showDir = raw_input(time.strftime('[%H:%M:%S]:') + "Display directory changes(yes or no):")
            except:
                pass
        else:
            spyDir = input(time.strftime('[%H:%M:%S]:') + "Please enter a directory:")
            unspyDir = input(time.strftime('[%H:%M:%S]:') + "Unnecessary directory:")
            showDir = input(time.strftime('[%H:%M:%S]:') + "Show directory changes(yes or no):")
    else:
        spyDir = args.p
        if args.hp != "":
            unspyDir = args.hp
        else:
            unspyDir = {}
        showDir = args.sd
    # 参数格式化
    print(time.strftime('[%H:%M:%S]:') + "\033[1;33m%s\033[0m" % "FileMonitor is running...")
    event_handler = FileEventHandler()
    if showDir == 'yes':
        event_handler.showDir = True
    if len(unspyDir) > 1:
        event_handler.unspyDirs = unspyDir.split(',')

    observer = Observer()
    observer.schedule(event_handler, spyDir, True)
    observer.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()