import paramiko
import scp

class SSHClient():
    def connect(self, ip, user_name, passwd):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.ssh.load_system_host_keys()
        self.ssh.connect(ip, 22, user_name, passwd, timeout = 5)
        self.scp = scp.SCPClient(self.ssh.get_transport())
        
    def get(self,  remote_path, local_path='',
            recursive=False, preserve_times=False):
        self.scp.get(remote_path, local_path, recursive, preserve_times)
        
    def put(self, files, remote_path='.',
            recursive=False, preserve_times=False):
        self.scp.put(files, remote_path, recursive, preserve_times)
    
    def execute(self, cmd):
        return self.ssh.exec_command(cmd)
        


