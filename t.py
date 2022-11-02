#!/usr/bin/python3

import random
import time
import os.path
import datetime

txerrfile = 'txerr.txt'
str = "%DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_TX_ERRORS_DETECTED: Module {} \
    received tx errors on internal interface ii2/1/3 since last run TXErr={} TotalTXErr={}"
print (f'%DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_TX_ERRORS_DETECTED: Module {random.randrange(0,9)} \
    received tx errors on internal interface ii2/1/3 since last run TXErr={random.randrange(0,100)} \
    TotalTXErr={random.randrange(0,200)}')

err_num = int(str1.split()[14].split('=')[1])
module_num = int(str1.split()[2])
#time1 = int(os.path.getmtime(txerrfile))
#time2 = int(time.time())

if (time2 - time1) > 360:
    print("얼마 안됐네")
    if err_num > 100:
        if os.path.exists(txerrfile):
            print("File exist")
            time1 = int(os.path.getmtime(txerrfile))
            time2 = int(time.time())
            if (time2 - time1) > 360:
                with open(txerrfile, 'a+') as fd:
                    linenum = len(fd.readline())
                    if linenum <= 4:
                        fd.write(module_num, err_num+"\n")
                        fd.close()
                    else:
                        print("Syslog")
            else:
                with open(txerrfile, 'w') as fd:
                    fd.write(module_num, err_num+"\n")
                    fd.close()
        else:
            with open(txerrfile, 'w') as fd:
                fd.write(module_num, err_num+"\n")
                fd.close()
    else:
        print("///") 
else:
    print("좀 지났네")  

unixtodatetime1 = datetime.datetime.fromtimestamp(time1)
unixtodatetime2 = datetime.datetime.fromtimestamp(time2)
print(unixtodatetime1, unixtodatetime2)
time.sleep(1)