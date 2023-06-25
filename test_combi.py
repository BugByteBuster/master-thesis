import os
import dpkt


def process_pcap_file(filename):
    count_ipv6 = 0
    count_ipv4 = 0
    count_tipc = 0
    count_sctp = 0
    count_tcp = 0
    count_udp = 0
    count_attribute_errors = 0

    with open(filename, "rb") as f:
        pcap = dpkt.pcap.Reader(f)
        for timestamp, buf in pcap:
            link_eth = dpkt.ethernet.Ethernet(buf)
            if link_eth.type == 35018:
                count_tipc += 1
            elif link_eth.type == 34525:
                count_ipv6 += 1
            elif link_eth.type == 2048:
                count_ipv4 += 1

            network_layer = link_eth.data
            try:
                transport_layer = network_layer.data
                if transport_layer.p == 132:
                    if len(transport_layer) >= 1500:
                        print(len(transport_layer))
                    count_sctp += 1
                elif transport_layer.p == 6:
                    count_tcp += 1
                elif transport_layer.p == 17:
                    count_udp += 1
                else:
                    print(transport_layer.p)
                    print("********************************", len(transport_layer))
            except AttributeError:
                count_attribute_errors += 1

    return (
        count_ipv6,
        count_ipv4,
        count_tipc,
        count_sctp,
        count_tcp,
        count_udp,
        count_attribute_errors,
    )


def main():
    count_ipv6_total = 0
    count_ipv4_total = 0
    count_tipc_total = 0
    count_sctp_total = 0
    count_tcp_total = 0
    count_udp_total = 0
    count_attribute_errors_total = 0

    directory = "/home/ezpedvi/packets_sctp"
    for filename in os.listdir(directory):
        if filename.startswith("sctp") and filename != "packetinfo0078":
            print(filename)
            filepath = os.path.join(directory, filename)
            (
                count_ipv6,
                count_ipv4,
                count_tipc,
                count_sctp,
                count_tcp,
                count_udp,
                count_attribute_errors,
            ) = process_pcap_file(filepath)

            count_ipv6_total += count_ipv6
            count_ipv4_total += count_ipv4
            count_tipc_total += count_tipc
            count_sctp_total += count_sctp
            count_tcp_total += count_tcp
            count_udp_total += count_udp
            count_attribute_errors_total += count_attribute_errors

            print("attribute_errors: ", count_attribute_errors)
            print(
                "count_tipc: %s, count_sctp= %s, count_tcp=%s, count_udp=%s"
                % (count_tipc, count_sctp, count_tcp, count_udp)
            )
            print(
                "total packets: %s" % (count_tipc + count_sctp + count_tcp + count_udp)
            )
            print("total packets count: %s" % (count_ipv6 + count_ipv4 + count_tipc))
            print(
                "count_ipv4:%s, count_ipv6:%s, count_tipc:%s"
                % (count_ipv4, count_ipv6, count_tipc)
            )

    print(
        "total packets count: %s"
        % (count_ipv6_total + count_ipv4_total + count_tipc_total)
    )
    print(
        "count_ipv4:%s, count_ipv6:%s, count_tipc:%s"
        % (count_ipv4_total, count_ipv6_total, count_tipc_total)
    )
    print(count_tipc_total, count_sctp_total, count_tcp_total, count_udp_total)


if __name__ == "__main__":
    main()
