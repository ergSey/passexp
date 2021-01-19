#!/bin/python

import os
import datetime
import time

HOST = "Zabbix_Hostname"
ZabS = "Zabbix_Server_IP"

def user_list():
	command = "cat /etc/passwd | egrep '/bin/bash|/bin/tcsh' | awk -F: '{print$1}'"
	pipe = os.popen(command)
	out = pipe.read()
	A = list(out.split('\n'))

	userlist=list(filter(None,A))
	print(userlist)
	return userlist

def main(userlist):
	for acc in userlist:
		command = 'logins -xtol {0} | awk -F: \'{{print $9}}\' | cut -c -2'.format(acc)
		pipe = os.popen(command)
		month = pipe.read()
		month = month[:-1]

		command = 'logins -xtol {0} | awk -F: \'{{print $9}}\' | cut -c 3-4'.format(acc)
        	pipe = os.popen(command)
        	day = pipe.read()
		day = day[:-1]

		command = 'logins -xtol {0} | awk -F: \'{{print $9}}\' | cut -c 5-6'.format(acc)
        	pipe = os.popen(command)
        	year = pipe.read()
		year = year[:-1]
		if month !="00" and day !="00":
			aa = datetime.date(int("20"+year),int(month),int(day))
			bb = datetime.date.today()
			cc = str(bb-aa)
			cc = cc.split(' ')
			item = cc[0]
			if acc !="root":
				create_items(ZabS,HOST,acc)
			time.sleep(10)
			send_items(ZabS,HOST,acc,item)

def create_items(ZabS,HOST,acc):
	command = 'zabbix_sender -z {0} -s {1} -k new_user.finder -o \'{{"data":[{{"{{#NR}}":"{2}"}}]}}\''.format(ZabS,HOST,acc)
	print(command)
	pipe = os.popen(command)

def send_items(ZabS,HOST,acc,item):
	command = 'zabbix_sender -z {0} -s {1} -k \'user_paswd_[{2}]\' -o {3}'.format(ZabS,HOST,acc,item)
        print(command)
        pipe = os.popen(command)

userlist = user_list()
main(userlist)
