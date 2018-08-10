#sudo timeout 100 tcpdump -i enp0s3 greater 1500 | awk '{print $1, $15}' > packet_info.txt

declare -a time_interval
declare -a packet_count


#time_array=($(cat packet_info.txt | awk '{ print $1 }'))
#packetsize_array=($(cat packet_info.txt | awk '{ print $2 }'))

#echo all : ${time_array[*]}
#echo one : ${time_array[1]}
#echo all : ${packetsize_array[*]}
#echo one : ${packetsize_array[1]}
#echo length of array
#echo ${#time_array[@]}


#packet_count=($(uniq -c --check-chars=2 /home/vidyadhar/packet_info.txt | awk '{print $1}'))
#time_interval=($(uniq -c --check-chars=2 /home/vidyadhar/packet_info.txt | awk '{print $2}'))
uniq -c --check-chars=2 /home/vidyadhar/packet_info.txt | sed -e 's/^\(.\{10\}\).*$/\1/'> count_time.txt

echo ${packet_count[*]}
echo ${time_interval[*]}


gnuplot -persist <<-EOFMarker
	set title "packet size vs time"
	set xlabel "time"
	set ylabel "size of packet"
	set style data histogram
	set style histogram cluster gap 1
        set style fill solid border -1
	set grid
	plot "/home/vidyadhar/count_time.txt" using 1:xticlabels(2) with histogram
EOFMarker

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

sudo timeout 100 tcpdump -i enp0s3 greater 1500 | awk '{print $1, $15}' > packet_info.txt
#sed '/^\s*$/d' packet_info.txt > packet_info.txt

: '
uniq -c --check-chars=2 /home/vidyadhar/packet_info.txt | sed -e 's/^\(.\{10\}\).*$/\1/'> count_time.txt


declare -a time_interval
declare -a packet_count

gnuplot -persist <<-EOFMarker
	set title "packet size vs time"
	set xlabel "time"
	set ylabel "size of packet"
	set style data histogram
	set style histogram cluster gap 1
        set style fill solid border -1
	set grid
	plot "/home/vidyadhar/count_time.txt" using 1:xticlabels(2) with histogram
EOFMarker
'

