import paramiko
import time

def establish_ssh_connection(hostname, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    return ssh

def execute_command(ssh, command, sleep_time=0):
    chan = ssh.invoke_shell()
    chan.send(command + '\n')
    time.sleep(sleep_time)
    return chan.recv(9999)

def close_ssh_connection(ssh):
    ssh.close()

def fetch_files():
    ssh = establish_ssh_connection('134.138.212.12', 'ezpedvi', '9505100403@usha')
    chan = ssh.invoke_shell()

    for i in range(0, 5000):
        print("fetching files for the {}st time".format(i))
        execute_command(chan, "ssh root@10.80.100.101", 5)
        opt = execute_command(chan, "", 3)
        print("opt{}".format(opt))
        execute_command(chan, "rootroot", 3)
        opt2 = execute_command(chan, "", 3)
        print(opt2)
        execute_command(chan, "/cluster/./send_files.sh")
        while True:
            resp = execute_command(chan, "", 0)
            print(resp)
            if "password:" in resp:
                execute_command(chan, "9505100403@usha")
            if "SC-1:" in resp:
                break
        execute_command(chan, "exit", 3)

    close_ssh_connection(ssh)

fetch_files()
