# -*- coding: utf-8 -*-
import paramiko

ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
connection=ssh_client.connect(hostname="192.168.xx.xx",username="ezpedvi",password="***********")
print connection

stdin,stdout,stderr=ssh_client.exec_command("ls")
print(stdout.readlines())

ftp_client=ssh_client.open_sftp()
ftp_client.get('scr.sh','/home/vidyadhar/scr.sh')
ftp_client.close()
stdin,stdout,stderr=ssh_client.exec_command("rm -rf scr.sh")
