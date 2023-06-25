import paramiko
import time

def connect_ssh(hostname, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    return ssh

def fetch_files(ssh):
    channel = ssh.invoke_shell()
    for i in range(0, 5000):
        print("fetching files for the {}st time".format(i))
        channel.send("/cluster/./send_files.sh\n")
        while True:
            resp = channel.recv(9999)
            print(resp)
            if "password:" in resp:
                channel.send("xxxxxxxx\n")
            if "SC-1:" in resp:
                break
        channel.send("exit\n")
        time.sleep(3)
        opt = channel.recv(9999)

def close_ssh(ssh):
    ssh.close()

# SSH connection details
hostname = '10.80.100.102'
username = 'xxxx'
password = 'xxxx'

# Connect to SSH
ssh = connect_ssh(hostname, username, password)

# Fetch files
fetch_files(ssh)

# Close SSH connection
close_ssh(ssh)
