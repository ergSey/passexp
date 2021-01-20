import os
import time
import datetime

HOST = "Zabbix_Hostname"
IP1 = "Server_with_shadow_file"
ZabS = "Zabbix_Server"

def get_data(ip):
	command = 'sshpass -p "Password_here" ssh -q ossuser@{0} "cat /home/ossuser/passexp/passres.txt"'.format(ip)
	print(command)
	pipe = os.popen(command)
	output = pipe.read()
	result = list(output.split('\n'))
	result=list(filter(None,result))
	print(result)
	return result

def create_items(IP, HOST):
	result = get_data(IP)
        for acc in result:
                acc = acc.split(' ')
                if len(acc) == 2 and acc[0] != "root" and acc[1] != "":
			command = 'zabbix_sender -z {0}  -s {1} -k new_user.finder -o \'{{"data":[{{"{{#NR}}":"{2}"}}]}}\''.format(ZabS,HOST,acc[0])
        		print(command)
			pipe = os.popen(command)
		time.sleep(5)

def send_items(IP, HOST):
	result = get_data(IP)
        for acc in result:
                acc = acc.split(' ')
                if len(acc) == 2 and acc[1] != "":
			item = time_mod(acc[1])
			if item == "0:00:00":
                                item = 0
			command = 'zabbix_sender -z {0}  -s {1} -k \'user_paswd_[{2}]\'  -o {3}'.format(ZabS,HOST,acc[0],item)
                	print(command)
			pipe = os.popen(command)

def time_mod(acc):
	acc = int(acc)
	epoh = datetime.date(1970,01,01)
	print(epoh)
	ch_date = epoh + timedelta(acc)
	print(ch_date)
	today = datetime.date.today()
	print(today)
	cc = str(today - ch_date)
	print(cc)
    	cc = cc.split(' ')
	item = str(cc[0])
    	print(item)
	return item

create_items(IP, HOST)
time.sleep(30)
send_items(IP, HOST)
