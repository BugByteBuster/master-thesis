cd /cluster/packets/
exception=$(ls -1tr | tail -1)

for fn in *; do
  if [[ $fn == $exception ]]; then
    continue
  fi
  scp "$fn" ezpedvi@134.138.212.12:/home/ezpedvi/packets/
  rm -rf "$fn"
  done
cd ..
echo "completed"
