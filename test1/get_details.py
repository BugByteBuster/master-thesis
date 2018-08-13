# -*- coding: utf-8 -*-
import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='xxxxxxxx', username='ezpedvi', password='xxxxxxx')
chan = ssh.invoke_shell()

time.sleep(3)
#ssh from ez to sc1
command = chan.send("ssh root@10.80.68.37\n")
time.sleep(5)
opt = chan.recv(9999)
print "opt{}".format(opt)
chan.send("rootroot\n")
time.sleep(3)
opt2 = chan.recv(9999)
print opt2

#ssh from  sc1 to pl3
chan.send("ssh PL-3\n")
time.sleep(3)
opt3 = chan.recv(9999)
print opt3

#file transfer Pl-3 to sc-1
chan.send("./send_files.sh\n")
time.sleep(10)
chan.send("exit\n")
time.sleep(3)
opt4= chan.recv(9999)
print opt4

#file transfer from sc1- ez
chan.send("scp -r /root/packets ezpedvi@1xxxxxxxx:/home/ezpedvi/packets\n")
time.sleep(2)
chan.send("xxxxxxx\n")
time.sleep(10)
opt5=chan.recv(9999)
print opt5
chan.send("rm -rf packets\n")
time.sleep(4)
chan.send("mkdir packets\n")
time.sleep(4)
chan.send("exit\n")

opt6=chan.recv(9999)
print opt6
ssh.close()

'''
script to run commands over ssh channel and get the files, VM to ez to SC1 to PL3 sends back files exit sl3 sends back files to ez
'''
#timeout 3600 tcpdump -i eth0 greater 1500 -W 200 -C 600 -w /cluster/packets/packetinfo
