import subprocess
import time
import dpkt


def run_tcpdump(interface, timeout):
    command = [
        "sudo",
        "timeout",
        str(timeout),
        "tcpdump",
        "-i",
        interface,
        "greater",
        "1500",
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    process.wait()
    linelist = process.stdout.readlines()
    return linelist


def process_pcap_file(filename):
    timestamps = []
    mtu = []

    with open(filename, "rb") as f:
        pcap = dpkt.pcap.Reader(f)

        for timestamp, buf in pcap:
            ip = dpkt.ethernet.Ethernet(buf).data
            tcp = ip.data
            timestamps.append(timestamp)
            mtu.append(len(tcp.data))

    return timestamps, mtu


def main():
    interface = "enp0s3"
    timeout = 5

    linelist = run_tcpdump(interface, timeout)
    print(linelist)

    filename = "packetinfo.pcap"
    time.sleep(10)

    timestamps, mtu = process_pcap_file(filename)
    print(timestamps)
    print(mtu)


if __name__ == "__main__":
    main()
