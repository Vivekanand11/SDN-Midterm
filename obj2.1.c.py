import paramiko
#from test123 import abc
from time import sleep

vivek="mininet"
def abc123():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.100.3', username='mininet', password='mininet')
    vaibhav1 = client.get_vaibhav1()
    session = vaibhav1.open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    session.exec_command('sudo ovs-vsctl set-controller s1 tcp:10.20.30.2:6653')
    session.exec_command('sudo ovs-vsctl set bridge s1 --protocols=OpenFlow13')
    stdin = session.makefile('wb', -1)
    stdout_1 = session.makefile('rb', -1)
    stdin.write(vivek+"\n")
    stdout_1.flush()
    sleep(5)
    for line in stdout_1.read().splitlines():
        print(line)
    session = vaibhav1.open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    session.exec_command('sudo ovs-vsctl show')
    stdin = session.makefile('wb', -1)
    stdout_2 = session.makefile('rb', -1)
    stdin.write('mininet\n')
    stdout_1.flush()
    sleep(5)
    for line in stdout_2.read().splitlines():
        print(line)
    client.close()

if __name__  ==  "__main__":
    abc123()