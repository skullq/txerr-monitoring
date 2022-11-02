#!/usr/bin/env python
import sys
import syslog
from cli import *
import time
import random
import time
import datetime
import os.path
from collections import Counter

txerrfile = '/bootflash/scripts/txerr.txt'
file_exist = False
file_age = False
input_list = []

msg = sys.argv[1]
input_list = []
input_list.append(msg.split()[3])
input_list.append(msg.split()[15].split('=')[1])


if os.path.exists(txerrfile):
    file_exist = True
    time1 = int(os.path.getmtime(txerrfile))
    time2 = int(time.time())
    if (time2 - time1) < 360:
        file_age = True
    else:
        file_age = False
else:
    file_exist = False

if int(input_list[1]) > 100:
    syslog.syslog(2,'Total TXErr is increasing in Module %s.  ' % input_list[0])
    if file_exist == True and file_age == True:
        with open(txerrfile, 'r') as fd:
            lines = fd.readlines()
            lines = [line.split(',', 1)[0] for line in lines]
            fd.close()
            lines.append(input_list[0])
            if (len(lines) >= 4):
                c = Counter(lines)
                order = c.most_common()
                maximum = order[0][1]
                max_mod = []
                for num in order:
                    if num[1] == maximum:
                        max_mod.append(num[0])
                syslog.syslog(1,'Highest TXErr LC or FM Module is %s' % list(max_mod))
                with open(txerrfile, 'a+') as fd:
                    fd.write(input_list[0] + "," + input_list[1] + "\n")
                    fd.close()
            else:
                with open(txerrfile, 'a+') as fd:
                    fd.write(input_list[0] + "," + input_list[1] + "\n")
                    fd.close()
    else:
        with open(txerrfile, 'w') as fd:
            fd.write(input_list[0] + "," + input_list[1] + "\n")
            fd.close()
else:
    pass


#event manager applet TXerr
#  event syslog pattern ".INTERNAL_PORT_MONITOR_*.*_ERRORS_DETECTED"
#  action 1 cli sleep 1
#  action 2 cli source txerr_n9k_modify.py "$_syslog_msg"

