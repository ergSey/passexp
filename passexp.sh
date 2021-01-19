#!/bin/bash
HOST="Zabbix_Hostname"
DLINE="Last Change"

user=$(cat /etc/passwd | grep "/bin/bash\|sftp-server" | grep -v "root" | awk -F':' '{print$1}')
for var in $(echo $user)
     do
        month=$(chage -l $var | grep "$DLINE" | awk -F "," '{print $1,$2}' | awk -F ":" '{print $2}' | awk '{print$1}')
        day=$(chage -l $var | grep "$DLINE" | awk -F "," '{print $1,$2}' | awk -F ":" '{print $2}' | awk '{print$2}')
        year=$(chage -l $var | grep "$DLINE" | awk -F "," '{print $1,$2}' | awk -F ":" '{print $2}' | awk '{print$3}')
        sysdate=$(date '+%s')
        paschgdate=$(date --date=''$day' '$month' '$year' 00:00:00' '+%s')
        paslifetime=$(($sysdate - $paschgdate))
        value=$(($paslifetime / 86400))
        /usr/bin/zabbix_sender -z Zabbix_Server_IP -s "$HOST" -k new_user.finder -o '{"data":[{"{#NR}":"'$var'"}]}'
     done

sleep 2m

user=$(cat /etc/passwd | grep "/bin/bash\|sftp-server" | awk -F':' '{print$1}')
for var in $(echo $user)
     do
        month=$(chage -l $var | grep "$DLINE" | awk -F "," '{print $1,$2}' | awk -F ":" '{print $2}' | awk '{print$1}')
        day=$(chage -l $var | grep "$DLINE" | awk -F "," '{print $1,$2}' | awk -F ":" '{print $2}' | awk '{print$2}')
        year=$(chage -l $var | grep "$DLINE" | awk -F "," '{print $1,$2}' | awk -F ":" '{print $2}' | awk '{print$3}')
        sysdate=$(date '+%s')
        paschgdate=$(date --date=''$day' '$month' '$year' 00:00:00' '+%s')
        paslifetime=$(($sysdate - $paschgdate))
        value=$(($paslifetime / 86400))
        /usr/bin/zabbix_sender -z Zabbix_Server_IP -s "$HOST" -k 'user_paswd_['$var']' -o "$value"
     done
