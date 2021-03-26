import os
import time
import datetime

HOST = "Zabbix_Hostname"
IP1 = "Server_with_shadow_file"
ZabS = "Zabbix_Server"

def get_data(ip):
	output = os.popen('sshpass -p "Password_here" ssh -q ossuser@{0} "cat /home/ossuser/passexp/passres.txt"'.format(ip)).read()
	result=list(filter(None,list(output.split('\n'))))
	return result

def create_items(IP, HOST):
	result = get_data(IP)
        for acc in result:
                acc = acc.split(' ')
                if len(acc) == 2 and acc[0] != "root" and acc[1] != "":
			pipe = os.popen('zabbix_sender -z {0}  -s {1} -k new_user.finder -o \'{{"data":[{{"{{#NR}}":"{2}"}}]}}\''.format(ZabS,HOST,acc[0]))
		time.sleep(5)

def send_items(IP, HOST):
	result = get_data(IP)
        for acc in result:
                acc = acc.split(' ')
                if len(acc) == 2 and acc[1] != "":
			item = time_mod(acc[1])
			if item == "0:00:00": item = 0
			pipe = os.popen('zabbix_sender -z {0}  -s {1} -k \'user_paswd_[{2}]\'  -o {3}'.format(ZabS,HOST,acc[0],item))

def time_mod(acc):
	acc = int(acc)
	ch_date = datetime.date(1970,01,01) + timedelta(acc)
	today = datetime.date.today()
    	cc = str(today - ch_date).split(' ')
	item = str(cc[0])
	return item

if __name__ == '__main__':
	create_items(IP, HOST)
	time.sleep(30)
	send_items(IP, HOST)
