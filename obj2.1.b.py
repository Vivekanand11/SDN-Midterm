import paramiko
from time import sleep
vivek = paramiko.SSHClient()
vivek.set_missing_host_key_policy(paramiko.AutoAddPolicy())
vivek.connect('192.168.100.3', username='mininet', password='mininet')
vivek123 = vivek.get_vivek123()
session = vivek123.open_session()
session.set_combine_stderr(True)
session.get_pty()
session.exec_command("sudo -k mn")

stdin = session.makefile('wb', -1)
stdout = session.makefile('rb', -1)
stdin.write('mininet\n')
print(stdout.read())
session.exec_command('sudo ovs-vsctl show')
for line in stdout.read().splitlines():
    print(f'{line}')
vivek.close()


