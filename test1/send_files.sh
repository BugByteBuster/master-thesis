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
