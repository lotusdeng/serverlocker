import task
import os

class tasklog(task.Task):
    def do(self, sshClient, ftpClient):
        self.logStart()
        localDir = os.path.join("./", "tasklog")
        if not os.path.isdir(localDir):
            os.makedirs(localDir)
        ftpClient.downloadFolder("/var/log", localDir)
        self.logFinish()
    def getDesription(self):
        return "get /var/log"