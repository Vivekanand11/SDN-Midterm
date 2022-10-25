
import os
import json
from threading import Thread
import threading
import sys

import pyshark

PortsDetected = {}


def Capture_Packet(run_event):
    while run_event.is_set():
        try:
            cap = pyshark.LiveCapture(interface='enp0s8', bpf_filter='tcp and (port 6653 or port 6633)')
            cap.sniff(packet_count=200)
            packetProcess = Thread(target=Analyze_Packet, args=(cap, run_event,))
            packetProcess.start()
        except KeyboardInterrupt:
            print("Shutting down the program")
            run_event.clear()
            # os.system("iptables -F")
            break
    sys.exit()


def Analyze_Packet(cap, run_event):
    for pkt in cap:
        if not run_event.is_set():
            break
        if not "OPENFLOW_V4" in str(pkt.layers):
            continue
        elif not str(pkt.openflow_v4.type) == "10":
            continue
        elif str(pkt.openflow_v4.type) == "10":
            source_ip = str(pkt.ip.src)
            source_port = str(pkt.tcp.srcport)
            if source_ip + ":" + source_port in PortsDetected:
                PortsDetected[source_ip + ":" + source_port] += 1
                if PortsDetected[source_ip + ":" + source_port] >= 100:
                    print("Detected attack with IP address {} and Port Number {}".format(source_ip, source_port))
                    print("Blocking the device with IP {} and Port Number {}".format(source_ip, source_port))
                    os.system(
                        "sudo iptables -I INPUT -p tcp -s {} -d 192.168.197.5 --dport 6653 --sport {} -m state --state NEW,ESTABLISHED -j DROP".format(
                            source_ip, source_port))
                    del PortsDetected[source_ip + ":" + source_port]
            else:
                PortsDetected[source_ip + ":" + source_port] = 1
    return


if __name__ == "__main__":
    run_event = threading.Event()
    run_event.set()
    Capture_Packet(run_event)
