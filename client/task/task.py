class Task(object):
    def __init__(self):
        pass
    def do(self, sshClient, ftpClient):
        pass
    def getDesription(self):
        return ""
    def logStart(self):
        with open("taskprogress.txt", "a") as fd:
            fd.write(self.__class__.__name__ + " start\n")
        pass
    def logFinish(self):
        with open("taskprogress.txt", "a") as fd:
            fd.write(self.__class__.__name__ + " finish\n")
        pass