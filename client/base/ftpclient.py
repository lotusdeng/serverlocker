from ftplib import FTP
import os


class FTPFile():
    def __init__(self, str):
        words = str.split(";")
        self.name = words[len(words) - 1]
        self.name = self.name.strip()
        for word in words:
                property = word.split("=")
                if len(property) == 2:
                    if property[0] == "modify":
                        self.modify = property[1]
                    elif property[0] == "perm":
                        self.perm = property[1]
                    elif property[0] == "size":
                        self.size = int(property[1])    
                    elif property[0] == "type":
                        self.type = property[1]
                    elif property[0] == "unique":
                        self.unique = property[1]
                    else:
                        pass
        pass


class FTPClient():
    def connect(self, ip, port, user, passwd):
        self.ftp = FTP()
        self.ftp.connect(ip, port)
        self.ftp.login(user, passwd)
        #self.ftp.set_debuglevel(2)
        self.ftp.set_pasv(False)
        
    def getFileSize(self, filePath):
        dir = os.path.dirname(filePath)
        self.ftp.cwd(dir)
        fileName = os.path.basename(filePath)
        fileSize = self.ftp.size(fileName)
        return fileSize
    
#     def Read(self, filePath, pos, len):
#         dir = os.path.dirname(filePath)
#         self.ftp.cwd(dir)
#         fileName = os.path.basename(filePath)
#         conn = self.ftp.transfercmd("RETR " + fileName, pos)
    def downloadFile(self, remotePath, localPath):
        remoteDir = os.path.dirname(remotePath)
        remoteFileName = os.path.basename(remotePath)
        self.ftp.cwd(remoteDir)
        remoteFileSize = self.ftp.size(remoteFileName)
        
        if os.path.isdir(localPath):
            localPath = os.path.join(localPath, remoteFileName)
            os.system("touch " + localPath)
        elif os.path.isfile(localPath):
            pass
        else:
            pass
        
        localSize = os.stat(localPath).st_size
        if localSize >= remoteFileSize:
            return
        self.ftp.voidcmd('TYPE I')#set binary model
        if localSize == 0:
            conn = self.ftp.transfercmd("RETR " + remoteFileName)
        else:
            conn = self.ftp.transfercmd("RETR " + remoteFileName , localSize)
        localFd = open(localPath, "ab")
        while True:
            data = conn.recv(1024*1024)
            if not data:
                break
            localFd.write(data)
        
        localFd.close()
    
   
    def downloadFolder(self, remoteDirPath, localDirPath):
        self.ftp.cwd(remoteDirPath)
        lines = []
        print "start get dir ", remoteDirPath

        self.ftp.retrlines("MLSD", lines.append)
        for i in lines:
            self.ftp.cwd(remoteDirPath)
            file = FTPFile(i)
            if file.type == "file":
                print "start get file ", os.path.join(remoteDirPath, file.name)
                localFilePath = os.path.join(localDirPath, file.name)
                if not os.path.exists(localFilePath):
                    os.system("touch " + localFilePath)
                if file.size != 0:
                    localSize = os.stat(localFilePath).st_size
                    if localSize >= file.size:
                        continue
                    self.ftp.voidcmd('TYPE I')#set binary model
                    print "localsize:", localSize
                    if localSize == 0:
                        conn = self.ftp.transfercmd("RETR " + file.name)
                    else:
                        conn = self.ftp.transfercmd("RETR " + file.name , str(localSize))
                    with open(localFilePath, "ab") as localFd:
                        while True:
                            data = conn.recv(1024*1024)
                            if not data:
                                break
                            localFd.write(data)
                    #conn.close()
                    
            elif file.type == "dir":
                localChildDir = os.path.join(localDirPath, file.name)
                remoteChildDir = os.path.join(remoteDirPath, file.name)
                if not os.path.exists(localChildDir):
                    os.makedirs(localChildDir)
                self.downloadFolder(remoteChildDir, localChildDir)
                    
               
            
        
        
        
        
    def close(self):
        self.ftp.voidcmd('NOOP')
        self.ftp.voidresp()
        self.ftp.quit()
        

if __name__ == "__main__":
    cli = FTPClient()
    cli.connect("172.18.10.12", 21, "root", "root")
    cli.downloadFolder("/var/log", "./log")
    cli.close()