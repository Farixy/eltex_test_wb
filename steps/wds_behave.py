#!/usr/bin/python
# -*- coding: utf-8 -*-

import pexpect
import sys
import time
from behave import *

@when(u'Подключиться по telnet к устройству с IP "{ip}" с prompt "{prompt}"')
def step(context, ip, prompt):
	context.prompt = prompt
	context.tn = pexpect.spawn('telnet ' + ip)
	#tn.logfile = sys.stdout
	match = context.tn.expect(['ogin:', pexpect.EOF, pexpect.TIMEOUT], timeout = 5)
	if  match != 0:
		raise NameError('Error connect to device ' + ip)
		sys.exit()
	context.tn.sendline('admin')
	context.tn.expect('assword:')
	context.tn.sendline('password')
	match = context.tn.expect([context.prompt, pexpect.EOF, pexpect.TIMEOUT], timeout = 5)
        if  match != 0:
                sys.exit()

@when(u'Сменить частотный канал на "{channel}"')
def step(context, channel):
	context.tn.sendline('sed -i \'1342c\        Channel: "' + channel + '"\' /etc/config/cfg.yaml')
	context.tn.expect(context.prompt)
	context.tn.sendline('reloadcfg')
	match = context.tn.expect(['Configuration accepted', pexpect.EOF, pexpect.TIMEOUT], timeout = 5)
        if  match != 0:
                sys.exit()
	try:
		context.tn.exit()
	except:
		pass

@when(u'Проверить пингом доступность хоста "{host_ip}"')
def step(context, host_ip):
	p = pexpect.spawn('ping ' + host_ip + ' -c 5')
	match = p.expect(['0% packet loss', pexpect.EOF, pexpect.TIMEOUT], timeout = 10)
	if match != 0:
		raise NameError('Error ping ' + host_ip)

@when(u'Подождать "{s}" секунд')
def step(context, s):
	time.sleep(int(s))
