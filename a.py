#!/usr/bin/python3

import random
import time
import os.path
import datetime

txerrfile = 'txerr.txt'
modulelist = [1, 2, 3, 4, 5, 6, 7, 8, 22, 23, 24, 25]

str = "%DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_TX_ERRORS_DETECTED: Module {} \
    received tx errors on internal interface ii2/1/3 since last run TXErr={} TotalTXErr={}"

'''
print (f'%DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_TX_ERRORS_DETECTED: Module {random.randrange(0,9)} \
    received tx errors on internal interface ii2/1/3 since last run TXErr={random.randrange(0,100)} \
    TotalTXErr={random.randrange(0,200)}')
'''

with open(txerrfile, 'r') as fd:
    lines = fd.readlines()
    lines = [line.split(',', 1)[0] for line in lines]
    fd.close()
    ### append last entry into lines
    if (len(lines) >= 4):
        dup_dict = {}
        for i in lines:
            dup_dict[i] = lines.count(i)
        print(f"Not sorted : {dup_dict}")
        sorted_dict = dict( sorted(dup_dict.items(), key=lambda item: item[1], reverse=True))
        print(f"Decending Sorted : {sorted_dict}")
        print(f"Highest TXErr LC or FM is {list(sorted_dict.keys())[0]}")
    else:
        pass


 #   for each_line in lines:
 #       each_line.split(',')
 #       print(each_line)

#    if len(x) > 4:
#        print(f"length is {len(x)}")

#    print(x[0][0])
#    fd.close()