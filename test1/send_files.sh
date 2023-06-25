send_files() {
  local source_dir=$1
  local destination_dir=$2
  local exception_file=$3

  cd "$source_dir"
  local files=$(ls -1tr)
  local exception=$(echo "$files" | tail -1)

  for file in $files; do
    if [[ $file == $exception ]]; then
      continue
    fi

    scp -r "$file" "root@SC-1:$destination_dir"
    rm -rf "$file"
  done

  cd ..
}

cd packets
send_files . /root/packets

cd /cluster/packets
send_files . /dev/packets

echo "completed"

nohup timeout 43200 tcpdump -i eth0 greater 1500 -W 5000 -C 600 -w /cluster/packets/packetinfo >/dev/null 2>&1
