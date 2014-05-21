import task

class tasksysteminfo(task.Task):
    
    def do(self, sshClient, ftpClient):
        self.logStart()
        stdin, stdout, stderr = sshClient.execute("uname -a")
        outs = stdout.readlines()
        errs = stderr.readlines()
        with open(self.__classs.__name__ + ".txt", 'a') as fd:
            if len(outs) > 0:
                fd.write("uanme={0}".format(outs[0]))
        
        stdin, stdout, stderr = sshClient.execute("cat /etc/redhat-release")
        outs = stdout.readlines()
        errs = stderr.readlines()
        if len(errs) > 0:
            pass
        else:
            with open(self.__classs.__name__ + ".txt", 'a') as fd:
                if len(outs) > 0:
                    fd.write("distribution={0}".format(outs[0]))
        self.logFinish()
        
    def getDesription(self):
        return "by uname -a; /etc/redhat-release"