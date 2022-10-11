from time import sleep
from netmiko import ConnectHandler
iosv2 = {
        'device_type': 'cisco_ios',
        'ip': '192.168.100.1',
        'username': 'r1',
        'password': 'r1'
}

ssh = ConnectHandler(**iosv2)
configcommand = ['router ospf 10', 'network 192.168.100.0 0.0.0.255 area 0', 'network 192.168.200.0 0.0.0.255 area 0', 'exit']
get_r1_config = ssh.send_config_set(configcommand)
print(get_r1_config)
#ssh into router 2
ssh.write_channel('ssh -l r2 192.168.200.2'+'\n')
sleep(5)
password = 'r2'
x = 'r4'
passwd = ssh.read_channel()
print(passwd)
if "Password" in passwd:
        ssh.write_channel(password+"\n")
        sleep(5)
        ssh.write_channel('conf t'+'\n')
        ssh.write_channel('router ospf 10'+'\n')
        ssh.write_channel('network 172.16.100.0 0.0.0.255 area 0'+'\n')
        ssh.write_channel('network 192.168.200.0 0.0.0.255 area 0'+'\n')
        ssh.write_channel('end'+'\n')
        #ssh into r4
        ssh.write_channel('ssh -l r4 172.16.100.1' + '\n')
        sleep(5)
        router3 = ssh.read_channel()
        print(router3)

        if "Password" in passwd:
                ssh.write_channel(x+"\n")
                sleep(10)
                ssh.write_channel('conf t' + '\n')
                ssh.write_channel('router ospf 10' + '\n')
                ssh.write_channel('network 172.16.100.0 0.0.0.255 area 0' + '\n')
                ssh.write_channel('network 10.20.30.0 0.0.0.255 area 0' + '\n')
                ssh.write_channel('end \n')
                sleep(5)
                router4 = ssh.read_channel()
                print(router4)


