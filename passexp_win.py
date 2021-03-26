import os
import datetime

HOST = "ZabbixHostname"
ZabS = "Zabbix_Server_IP"

def user_list():
    out = os.popen('net user').read()
    acc = out[116:-37]
    netuser = ''
    for i in range(len(acc)):
        if acc[i] != ' ' and acc[i] != '\n':
            netuser += acc[i]
        elif acc[i] == ' ' and acc[i+1] != ' ':
            netuser += ':'
    netuser=list(filter(None,list(netuser.split(':'))))
    return netuser

def get_data(netuser):
    for acc in netuser:
        out = os.popen('net user {0}'.format(acc)).read()
        listing = ''
        for i in range(len(out)):
            if out[i] != '\n':
                listing += out[i]
            else:
                listing +='&'
 
        date = list(listing.split('&'))[8].split(' ')[14].split('/')
        cc = str(datetime.date.today() - datetime.date(int(date[2]),int(date[0]),int(date[1])))
        item = str(cc.split(' ')[0])
        if item == "0:00:00": item = 0
        zabbix_sender(item, acc)

def zabbix_sender(item,acc):
    for path in ['C:\\zabbix\\bin\\win32\\zabbix_sender.exe', 'C:\\zabbix\\zabbix_sender.exe']:
        if os.path.isfile(path) == True: pipe = os.popen('{0} -z {1} -s {2} -k user_paswd_[{3}] -o "{4}"'.format(path,ZabS,HOST,acc,item))

if __name__ == '__main__': 
    netuser = user_list()
    get_data(netuser)
