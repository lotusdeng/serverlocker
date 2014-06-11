import os

def mkServerLockDir(sshClient):
    sshClient.execute("mkfs -q /dev/ram1 8192")
    sshClient.execute("mkdir -p /serverlocker")
    sshClient.execute("mount /dev/ram1 /serverlocker")

def getFtpProcessId(sshClient):
    stdin, stdout, stderr = sshClient.execute("ps -ef | grep ftpserver.py")
    lines = stdout.readlines()
    for i in lines:
        if i.find("python ftpserver.py") != -1 and i.find("bash -c") == -1:
            #this line is proc
            pass
def getServerOS(sshClient):
    return "linux"
        
def stopFtpServer(sshClient):
    pass
    
def installFtpServer(sshClient, user, passwd, ip, port):
    
    sshClient.put("../server", "/serverlocker", True)
    
    os.system("cp ../server/ftpserver.py ./ftpserver.py")
    lines = []
    with open("./ftpserver.py", "r") as fd:
        lines = fd.readlines()
    newLines = []
    for i in lines:
        if i.find("user") == 0:
            i = "user = '{0}'\n".format(user)
        elif i.find("passwd") == 0:
            i = "passwd = '{0}'\n".format(passwd)
        elif i.find("ip") == 0:
            i = "ip = '{0}'\n".format(ip)
        elif i.find("port") == 0:
            i = "port = {0}\n".format(port)
        else:
            pass
        newLines.append(i)
    with open("./ftpserver.py", 'w') as fd:
        fd.writelines(newLines)
    
    sshClient.put("./ftpserver.py", "/serverlocker/server")
    
    stdin, stdout, stderr = sshClient.execute("cd /serverlocker/server && python ftpserver.py &")
    #print stdout.readlines()
    #print stderr.readlines()
    pass