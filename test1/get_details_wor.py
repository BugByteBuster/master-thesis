import paramiko
import time

def connect_ssh(hostname, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    return ssh

def execute_command(ssh, command, delay):
    chan = ssh.invoke_shell()
    chan.send(command)
    time.sleep(delay)
    output = chan.recv(9999)
    return output

def fetch_files(hostname, username, password, target_ip, target_password):
    ssh = connect_ssh(hostname, username, password)
    
    for i in range(5000):
        print("fetching files for the {}st time".format(i))
        
        output = execute_command(ssh, "ssh root@{}\n".format(target_ip), 5)
        print("opt: {}".format(output))
        
        output = execute_command(ssh, "rootroot\n", 3)
        print(output)
        
        output = execute_command(ssh, "/cluster/./send_files.sh\n", 0)
        while True:
            resp = chan.recv(9999)
            print(resp)
            if "password:" in resp:
                chan.send("{}\n".format(target_password))
            if "SC-1:" in resp:
                break
        
        output = execute_command(ssh, "exit\n", 3)
        print(output)
    
    ssh.close()

if __name__ == "__main__":
    hostname = 'x.x.x.x'
    username = 'ezpedvi'
    password = 'xxxxxxxx'
    target_ip = 'x.x.x.x'
    target_password = 'xxxxxxxxxx'
    
    fetch_files(hostname, username, password, target_ip, target_password)
