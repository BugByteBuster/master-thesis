# -*- coding: utf-8 -*-
import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='10.80.100.102', username='root', password='rootroot')

channel = ssh.invoke_shell()
for i in range(0, 5000):
	print "fetching files for the {}st time".format(i)
	channel.send("/cluster/./send_files.sh\n")
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
