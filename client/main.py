import ConfigParser
import base.ftpclient
from task.task import Task
from base.sshclient import SSHClient
from base.ftpclient import FTPClient
from paramiko.ssh_exception import SSHException
import sys
import os
import util

sshClient = SSHClient()
ftpClient = FTPClient()
currentReconnect = 0
maxReconnect = 0

def createTask(taskName):
    moduleName = "task." + taskName
    __import__(moduleName.lower())
    module = sys.modules[moduleName] 
    className = getattr(module, taskName)
    task = className()
    return task


def init():
     cf = ConfigParser.ConfigParser()
     cf.read("task.ini")
     sshClient = SSHClient()
     ip = cf.get("server", "ip")
     user = cf.get("server", "user")
     passwd = cf.get("server", "passwd")
     newpasswd = cf.get("server", "newpasswd")
     ftpport = cf.getint("server", "ftpport")
     sshClient.connect(ip , user, passwd)
     serverOs = util.getServerOS(sshClient)
     if serverOs == "linux":
         if not os.path.isfile("installed"):
             print "first time init, so install ftp server"
             util.mkServerLockDir(sshClient)
             util.installFtpServer(sshClient, user, newpasswd, ip, ftpport)
             with open("installed", "w") as fd:
                 pass
         else:
             print "alread install ftp server"
             pass
     else:
         pass
     
     
def doTasks():
    cf = ConfigParser.ConfigParser()
    cf.read("task.ini")
    global currentReconnect
    global maxReconnect
    currentReconnect  = currentReconnect + 1
    if(currentReconnect > maxReconnect):
        return
                             
    try:
        sshClient.connect(cf.get("server", "ip"), cf.get("server", "user"), cf.get("server", "newpasswd"))
        ftpClient.connect(cf.get("server", "ip"),  cf.get("server", "ftpport"),
                          cf.get("server", "user"), cf.get("server", "newpasswd"))
        currentReconnect = 0
    except SSHException, e:
        print e
        doTasks()
    
    taskNamesStr = cf.get("task", "tasknames")
    taskNames = set(taskNamesStr.split(","))
    taskStatus={}
  
    with open("taskprogress.txt", 'r') as fd:
        lines = fd.readlines()
        for i in lines:
            words = i.split("=")
            if len(words) == 2:
                taskStatus[words[0]] = words[1]
    
    for i in taskNames:
        task = createTask(i)
        try:
            if i in taskStatus:
                if taskStatus[i] == "start":
                    task.do(sshClient, ftpClient)
                    pass
                elif taskStatus[i] == "finish":
                    pass
                else:
                    pass
            else:
                task.do(sshClient, ftpClient)
        except SSHException, e:
            print e
            doTasks()
            
def main():
    init()
    
    cf = ConfigParser.ConfigParser()
    cf.read("task.ini")
    global currentReconnect
    global maxReconnect
    currentReconnect = 0
    maxReconnect = cf.getint("server", "maxreconnect")
    doTasks()
    

if __name__ == "__main__":
    main()