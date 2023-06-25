#!/bin/bash

generate_packet_info() {
    sudo timeout 100 tcpdump -i enp0s3 greater 1500 | awk '{print $1, $15}' > packet_info.txt
}

filter_packet_info() {
    sed -i '/^\s*$/d' packet_info.txt
}

generate_count_time() {
    uniq -c --check-chars=2 packet_info.txt | sed -e 's/^\(.\{10\}\).*$/\1/' > count_time.txt
}

plot_packet_size_vs_time() {
    gnuplot -persist <<-EOFMarker
        set title "packet size vs time"
        set xlabel "time"
        set ylabel "size of packet"
        set style data histogram
        set style histogram cluster gap 1
        set style fill solid border -1
        set grid
        plot "count_time.txt" using 1:xticlabels(2) with histogram
EOFMarker
}

generate_packet_info
filter_packet_info
generate_count_time
plot_packet_size_vs_time
