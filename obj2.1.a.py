from netmiko import ConnectHandler
import regex


def R1():
    iosv2 = {
        'device_type': 'cisco_ios',
        'ip': '192.168.100.1',
        'username': 'r1',
        'password': 'r1'
    }

    net_connect = ConnectHandler(**iosv2)
    config_commands = ['do sh ip dhcp binding']
    net_connect.enable()
    a = net_connect.send_config_set(config_commands)
    print(a)
    b = regex.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', a)
    print(f'The IP address of the mininet vm is', b)


if __name__ == "__main__":
    R1()
