#-*- coding: UTF-8 -*-
#==================================================================================================
#         Copyright (C)   :   2019
#         File Name       :   Copy.py
#         Discription     :   
#         Author          :    Li Minghua
#         Date            :   2019年11月27日 星期三 10时36分38秒
#==================================================================================================

import os
import platform
import re
import urllib
import time
import datetime
import json
import requests
import subprocess
import multiprocessing
import sys

PlugName = []
MyRepo    = "curl -X POST --header 'Content-Type: application/json;charset=UTF-8' 'https://gitee.com/api/v5/user/repos' -d "

def getPlugName(file):
    """
    From init.vim get plug names
    """
    global PlugName
    f = open(file,mode="r+")
    allText = f.read()
    f.close()
    allPlugs = re.findall(r'^Plug\ \'.*?\n',allText,re.M | re.S) # Get every Plug ... or "Plug ...
    for names in allPlugs:
        n = re.findall(r'\'.*?\'' ,names,re.M )[0][1:-1]  # get name in '...'
        qx, n1 = n.split('/')
        PlugName.append(n1)

def getUrlName(url:str):
    response = requests.get(url).text
    allPlugs = re.findall(r'\'qiaoxiaoqianxi/.*?\'',response,re.S | re.M)
    for names in allPlugs:
        qx, n1 = names[1:-1].split('/')
        PlugName.append(n1)

def downloadAndUpload(plugname:str):
    """
    downloads and update one plugin
    """
    cmd_rm     = "rm -rf .git"
    cmd_init   = "git init"
    cmd_remote = "git remote add origin git@gitee.com:qiaoxiaoqianxi/"
    cmd_add    = "git add ."
    cmd_commit_upload = 'git commit -m "Upload"'
    cmd_commit_update = 'git commit -m "Update'
    cmd_push   = "git push origin master"
    url_base   = "https://github.com/"

    #   download plugin from github
    os.chdir("/home/travis/.config/nvim/build/")
    n = re.sub("LMH","/",plugname)
    print("Start :  " + n)
    cmd_clone = "git clone " + url_base + n + ".git"
    os.system(cmd_clone)

    #   gitee operation
    dir_name = re.findall(r'/.*', n, re.I | re.S)[0][1:]

    MyRepoTail = "'{\"access_token\":\"dda869c399ca33e736f09ba11ae405d9\",\"name\":\"" + plugname + "\",\"description\":\"Mirror\",\"has_issues\":\"true\",\"has_wiki\":\"true\"}'"
    os.chdir("/home/travis/.config/nvim/build/" + dir_name)  #   进入插件目录

    res = requests.get("https://gitee.com/qiaoxiaoqianxi/" + plugname).status_code
    if 404 == res:                                # 本就不存在仓库，
        os.system(MyRepo + MyRepoTail)            # 新建仓库

        os.system(cmd_rm)                         # 删除原有.git
        os.system(cmd_init)                       # 新的初始化
        os.system(cmd_remote + plugname + ".git") # 链接
        os.system(cmd_add)                        # 添加
        os.system(cmd_commit_upload)              # 提交
        os.system(cmd_push)                       # 推送
        print("Created: " + n)
    else:                                         # 存在仓库，更新仓库
        UpdateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        os.system("git clone git@gitee.com:qiaoxiaoqianxi/" + plugname + ".git") # 用ssh方式克隆
        os.system("rm -rf .git")
        os.system("mv " + plugname + "/.git .")   # 移动.git
        os.system("rm -rf " + plugname)           # 删除多余内容
        os.system(cmd_add)
        os.system(cmd_commit_update + UpdateTime + '"')
        os.system(cmd_push)
        print("Updated: " + n)
        print("UpdateTime: " + UpdateTime)

def replaceLine(file, oldstr, newstr):
    """
    replace github addr to my gitee addr
    """
    with open(file, "r") as f1, open("%s.bak" % file, "w") as f2:
        for line in f1:
            f2.write(re.sub(oldstr,newstr,line))
    os.remove(file)
    os.rename("%s.bak" % file,file)
    
def AllCopy():
    """Copy all plugins
    :returns: TODO

    """
    startTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(startTime)
    getUrlName('https://gitee.com/qiaoxiaoqianxi/nvim/blob/master/init.vim')
    # getPlugName("init.vim")

    if not os.path.exists("/home/travis/.config/nvim/build") :
        os.makedirs("/home/travis/.config/nvim/build")
    os.chdir("/home/travis/.config/nvim/build")

    pool = multiprocessing.Pool(processes=16)
    for pname in PlugName:
        pool.apply_async(downloadAndUpload,( pname ,))

    pool.close()
    pool.join()

    endTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(endTime)

    os.system('rm -rf ~/.config/nvim/build')

#   Delete a Repo 
MyRepoDel = "curl -X DELETE --header 'Content-Type: application/json;charset=UTF-8' 'https://gitee.com/api/v5/repos/qiaoxiaoqianxi/"
def delRepo(RepoName : str):
    """Delete a repo named RepoName

    """
    MyRepoDel_Tail = RepoName + "?access_token=dda869c399ca33e736f09ba11ae405d9'"

    os.system(MyRepoDel + MyRepoDel_Tail)
    
if __name__ == "__main__":
    # print(PlugName)
    AllCopy()

