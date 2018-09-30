#!/usr/bin/python

import pexpect
import sys
import time

def telnet(ip, prompt):
	tn = pexpect.spawn('telnet ' + ip)
	#tn.logfile = sys.stdout
	match = tn.expect(['ogin:', pexpect.EOF, pexpect.TIMEOUT], timeout = 5)
	if  match != 0:
		print ('Error connect to ' + ip)
		sys.exit()
	tn.sendline('admin')
	tn.expect('assword:')
	tn.sendline('password')
	match = tn.expect([prompt, pexpect.EOF, pexpect.TIMEOUT], timeout = 5)
        if  match != 0:
                print ('Error prompt ' + prompt)
		print tn.before
                sys.exit()
	print ('Telnet to ' + ip + ' success')
	return tn

def change_channel(tn, prompt, channel):
	tn.sendline('sed -i \'1342c\        Channel: "' + channel + '"\' /etc/config/cfg.yaml')
	tn.expect(prompt)
	tn.sendline('reloadcfg')
	match = tn.expect(['Configuration accepted', pexpect.EOF, pexpect.TIMEOUT], timeout = 5)
        if  match != 0:
                print ('Error reloadcfg. Channel: ' + channel)
		print tn.before
                sys.exit()
	print ('set channel ' + channel)
	try:
		tn.exit()
	except:
		pass

def ping(host_ip):
	p = pexpect.spawn('ping ' + host_ip + ' -c 5')
	match = p.expect(['0% packet loss', pexpect.EOF, pexpect.TIMEOUT], timeout = 10)
	if match != 0:
		print 'Error ping'
		sys.exit
	print 'ping success'

prompt = 'root@WB([0-9]+)'
host_ip = '192.168.1.20'
channel_list = ['36', '40', '44', '48' , '52', '56', '60', '64']
for channel in channel_list:
	ip = '192.168.1.2'
	tn = telnet(ip, prompt)
	change_channel(tn, prompt, channel)
	ip = '192.168.1.1'
        tn = telnet(ip, prompt)
        change_channel(tn, prompt, channel)
	time.sleep(30)
	ping(host_ip)
