from scapy.all import *
def main():
    x = rdpcap('vivek.pcap')
    c_ip = x[130]['IP'].src
    print('IP of the controller is',c_ip)
    c_port = x[130]['TCP'].sport
    print('port of the controller is', c_port)

if __name__ == "__main__":
    main()