#!/bin/python

import os
import datetime
import time

HOST = "Zabbix_Hostname"
ZabS = "Zabbix_Server_IP"

def user_list():
	out = os.popen("cat /etc/passwd | egrep '/bin/bash|/bin/tcsh' | awk -F: '{print$1}'").read()
	userlist=list(filter(None,list(out.split('\n'))))
	return userlist

def main(userlist):
	for acc in userlist:
		month = os.popen('logins -xtol {0} | awk -F: \'{{print $9}}\' | cut -c -2'.format(acc)).read()
		month = month[:-1]

        	day = os.popen('logins -xtol {0} | awk -F: \'{{print $9}}\' | cut -c 3-4'.format(acc)).read()
		day = day[:-1]

        	year = os.popen('logins -xtol {0} | awk -F: \'{{print $9}}\' | cut -c 5-6'.format(acc)).read()
		year = year[:-1]
		if month !="00" and day !="00":
			cc = str(datetime.date.today()-datetime.date(int("20"+year),int(month),int(day))).split(' ')
			item = cc[0]
			if item == "0:00:00": item = 0
			if acc !="root": create_items(ZabS,HOST,acc)
			time.sleep(10)
			send_items(ZabS,HOST,acc,item)

def create_items(ZabS,HOST,acc):
	pipe = os.popen(command = 'zabbix_sender -z {0} -s {1} -k new_user.finder -o \'{{"data":[{{"{{#NR}}":"{2}"}}]}}\''.format(ZabS,HOST,acc))

def send_items(ZabS,HOST,acc,item):
        pipe = os.popen('zabbix_sender -z {0} -s {1} -k \'user_paswd_[{2}]\' -o {3}'.format(ZabS,HOST,acc,item))
	
if __name__ == '__main__':
	userlist = user_list()
	main(userlist)
