import paramiko
import time

def ssh_connect(hostname, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password)
    return ssh

def ssh_command(chan, command, sleep_time=3):
    chan.send(command + '\n')
    time.sleep(sleep_time)
    return chan.recv(9999)

def transfer_files(chan, source, destination):
    chan.send("scp -r {} {}\n".format(source, destination))
    time.sleep(2)

def main():
    hostname = 'x.x.x.x'
    username = 'xxxxxxx'
    password = 'xxxxxxx'

    ssh = ssh_connect(hostname, username, password)
    chan = ssh.invoke_shell()

    for i in range(0, 5000):
        print("fetching files for the {}st time".format(i))
        
        # SSH from ez to sc1
        ssh_command(chan, "ssh root@10.80.68.37")
        opt = ssh_command(chan, "rootroot")
        
        # SSH from sc1 to pl3
        opt3 = ssh_command(chan, "ssh PL-3")

        # File transfer Pl-3 to sc-1
        tstart = time.time()
        while True:
            resp = ssh_command(chan, "/cluster/./send_files.sh")
            print("resp: {}".format(resp))
            if "PL-3:~" in resp:
                break
        opt4 = ssh_command(chan, "exit")
        tend = time.time()

        # File transfer from sc1- ez
        transfer_files(chan, "/dev/packets/*", "xxxxxx@x.x.x.x:/home/ezpedvi/packets/")
        time.sleep(tend - tstart)
        ssh_command(chan, "wait")
        opt5 = ssh_command(chan, "rm -rf /dev/packets/*")
        opt6 = ssh_command(chan, "exit")

    ssh.close()

if __name__ == "__main__":
    main()
