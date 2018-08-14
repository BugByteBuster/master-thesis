cd packets
exception=$(ls -1tr | tail -1)
for fn in *; do
  if [[ $fn == $exception ]]; then
    continue
  fi
  scp -r "$fn" root@SC-1:/root/packets/ 
  rm -rf "$fn"
done
cd ..

#send files from PL-3 to SC-1: remember to write tcpdump output to a folder ex:packets
#make sure that SC-1 has an empty folder named packets

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
cd /cluster/packets
exception=$(ls -1tr | tail -1)
for fn in *; do
  if [[ $fn == $exception ]]; then
    continue
  fi
  scp -r "$fn" root@SC-1:/dev/packets/ 
  rm -rf "$fn"
done
cd ..
echo "completed"


nohup timeout 43200 tcpdump -i eth0 greater 1500 -W 5000 -C 600 -w /cluster/packets/packetinfo >/dev/null 2>&1

