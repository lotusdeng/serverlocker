import task
import os
import ConfigParser

class taskfindfile(task.Task):
    def do(self, sshClient, ftpClient):
        self.logStart()
        
        if os.path.isfile("./task/taskfindfile-find-finish"):
            pass
        else:
            cf = ConfigParser.ConfigParser()
            cf.read("./task/taskfindfile.ini")
            findargs = cf.get("files", "findargs")
            stdin, stdout, stderr = sshClient.execute("find " + findargs)
            lines = stdout.readlines()
            with open("./task/taskfindfile-find-finish", 'w') as fd:
                fd.writelines(lines)
        
        
        self.logFinish()
    def getDesription(self):
        return "get /var/log"