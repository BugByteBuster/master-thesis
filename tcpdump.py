import subprocess
import sys
f = open('output.txt','w')
sys.stdout = f
P=subprocess.Popen(['sudo', 'timeout', '5', 'tcpdump', '-i', 'enp0s3', 'greater', '1500'], stdout=subprocess.PIPE)
linelist= P.stdout.readlines()
print linelist
f.close()

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
import subprocess
import sys
import time
import matplotlib


#command = "sudo timeout 10 tcpdump -w packetinfo.pcap -i enp0s3 greater 1500"
command="sudo timeout 10 tcpdump -i enp0s3 greater 1500"
print command.split()
array=[]



f = open('output.txt','w')
sys.stdout = f
P=subprocess.Popen(command.split(), stdout=subprocess.PIPE)
linelist= P.stdout.readlines()
print linelist
for i in range(0, len(linelist)-1):
        values = linelist[i].split()
        print values
        print values[0], values[-1]

f.close()
print array
#time.sleep(10)
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

