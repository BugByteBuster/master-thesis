# -*- coding: utf-8 -*-
import paramiko
import time
import re
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='134.138.212.12', username='ezpedvi', password='9505100403@usha')

chan = ssh.invoke_shell()

for i in range(0, 5000):
	print "fetching files for the {}st time".format(i)
	command = chan.send("ssh root@10.80.100.101\n")
	time.sleep(5)
    	opt = chan.recv(9999)
    	print "opt{}".format(opt)
    	chan.send("rootroot\n")
    	time.sleep(3)
    	opt2 = chan.recv(9999)
    	print opt2
	chan.send("/cluster/./send_files.sh\n")
        while True:
        	resp = chan.recv(9999)
		print resp
		if "password:" in resp:
                	chan.send("9505100403@usha\n")
		if "SC-1:" in resp:
			break
        chan.send("exit\n")
        time.sleep(3)
        opt = chan.recv(9999)
ssh.close()
