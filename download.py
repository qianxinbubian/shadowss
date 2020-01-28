#==================================================================================================
#         Copyright (C)   :   2019
#         File Name       :   download.py
#         Discription     :   
#         Author          :    Li Minghua
#         Date            :   2020年01月27日 星期一 21时27分41秒
#==================================================================================================

import os
import platform
import multiprocessing
import requests
import datetime
from url import Inf

MyRepo    = "curl -X POST --header 'Content-Type: application/json;charset=UTF-8' 'https://gitee.com/api/v5/user/repos' -d "
def getUrl():
    pass

def dl(na:str,url:str):
    os.mkdir("na")
    os.chdir("na")
    os.system('wget ' + url)

    cmd_rm     = "rm -rf .git"
    cmd_init   = "git init"
    cmd_remote = "git remote add origin git@gitee.com:qiaoxiaoqianxi/"
    cmd_add    = "git add ."
    cmd_commit_upload = 'git commit -m "Upload"'
    cmd_commit_update = 'git commit -m "Update'
    cmd_push   = "git push origin master"
    url_base   = "https://github.com/"

    MyRepoTail = "'{\"access_token\":\"dda869c399ca33e736f09ba11ae405d9\",\"name\":\"" + na  + "\",\"description\":\"Mirror\",\"has_issues\":\"true\",\"has_wiki\":\"true\"}'"

    res = requests.get("https://gitee.com/qiaoxiaoqianxi/" + na ).status_code
    if 404 == res:                                # 本就不存在仓库，
        os.system(MyRepo + MyRepoTail)            # 新建仓库

        # os.system(cmd_rm)                         # 删除原有.git
        os.system(cmd_init)                       # 新的初始化
        os.system(cmd_remote + na  + ".git")      # 链接
        os.system(cmd_add)                        # 添加
        os.system(cmd_commit_upload)              # 提交
        os.system(cmd_push)                       # 推送
        print("Created: " + na)
    else:                                         # 存在仓库，更新仓库
        UpdateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        os.system("git clone git@gitee.com:qiaoxiaoqianxi/" + na  + ".git") # 用ssh方式克隆
        os.system("rm -rf .git")
        os.system("mv " + na  + "/.git .")   # 移动.git
        os.system("rm -rf " + na )           # 删除多余内容
        os.system(cmd_add)
        os.system(cmd_commit_update + UpdateTime + '"')
        os.system(cmd_push)
        print("Updated: " + na)
        print("UpdateTime: " + UpdateTime)


if __name__ == "__main__":
    na  = Inf[0][0]
    url = Inf[0][1]
    dl(na,url)
    pass
