import subprocess
import sys
f = open('output.txt','w')
sys.stdout = f
P=subprocess.Popen(['sudo', 'timeout', '5', 'tcpdump', '-i', 'enp0s3', 'greater', '1500'], stdout=subprocess.PIPE)
linelist= P.stdout.readlines()
print linelist
f.close()



