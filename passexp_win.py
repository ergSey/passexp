import os
import datetime

HOST = "ZabbixHostname"
ZabS = "Zabbix_Server_IP"

def user_list():
    command = 'net user'
    pipe = os.popen(command)
    out = pipe.read()
    acc = out[116:-37]
    netuser = ''
    for i in range(len(acc)):
        if acc[i] != ' ' and acc[i] != '\n':
            netuser += acc[i]
        elif acc[i] == ' ' and acc[i+1] != ' ':
            netuser += ':'
    A = list(netuser.split(':'))
    netuser=list(filter(None,A))
    return netuser

def get_data(netuser):
    for acc in netuser:
        command = 'net user {0}'.format(acc)
        pipe = os.popen(command)
        out = pipe.read()
        listing = ''
        for i in range(len(out)):
            if out[i] != '\n':
                listing += out[i]
            else:
                listing +='&'
        listing = list(listing.split('&'))
        datastring = listing[8]
        datastring = datastring.split(' ')
        date = datastring[14]

        date = date.split('/')
        aa = datetime.date(int(date[2]),int(date[0]),int(date[1]))
        bb = datetime.date.today()
        cc = str(bb - aa)
        cc = cc.split(' ')
        item = str(cc[0])
        if item == "0:00:00":
            item = 0
        zabbix_sender(item, acc)

def zabbix_sender(item,acc):
        if os.path.isfile('C:\\zabbix\\bin\\win32\\zabbix_sender.exe') == True:
                path = os.path.join(r'C:\zabbix\bin\win32', 'zabbix_sender.exe')
                command = '{0} -z {1} -s {2} -k user_paswd_[{3}] -o "{4}"'.format(path,ZabS,HOST,acc,item)
                print(command)
                pipe = os.popen(command)
        elif os.path.isfile('C:\\zabbix\\zabbix_sender.exe') == True:
                path = os.path.join(r'C:\zabbix', 'zabbix_sender.exe')
                command = '{0} -z {1} -s {2} -k user_paswd_[{3}] -o "{4}"'.format(path,ZabS,HOST,acc,item)
                pipe = os.popen(command)
                print(command)

netuser = user_list()
get_data(netuser)
