##!/usr/bin/env python

#!/usr/bin/python3

import sys
import syslog
#from cisco import cli
import random
import time
import datetime
import os.path

txerrfile = 'txerr.txt'
file_exist = False
file_age = False
input_list = []

modulelist = [1, 2, 3, 4, 5, 6, 7, 8, 22, 23, 24, 25]
str = "%DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_TX_ERRORS_DETECTED: Module {} received tx errors on internal interface ii2/1/3 since last run TXErr={} TotalTXErr={}"
#print (f'%DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_TX_ERRORS_DETECTED: Module {random.randrange(0,9)} received tx errors on internal interface ii2/1/3 since last run TXErr={random.randrange(0,100)} TotalTXErr={random.randrange(0,200)}')

while(1):
    # syslog simulation code about random case
    ran1 = random.choice(modulelist)
    ran2 = random.randrange(0,100)
    ran3 = random.randrange(0,200)
    str1 = str.format(ran1, ran2, ran3)
    input_list = []
    input_list.append(str1.split()[2])
    input_list.append(str1.split()[14].split('=')[1])

    #syslog.syslog(2,'%DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_TX_ERRORS_DETECTED: Module %s received tx errors on internal interface ii2/1/3 since last run TXErr=%s TotalTXErr=%s' % (ran1, ran2, ran3))

    print(str1)
    print("----------------------------------------------")
    print(f"Module = {input_list[0]}, TotalTXErr = {input_list[1]} ")
    print("----------------------------------------------")

    #msg = sys.argv[1]
    #input_list = []
    #input_list.append(msg.split()[2])   <<<< In front of log date should be placed so need to change list[number]
    #input_list.append(msg.split()[14].split('=')[1])   <<<< In front of log date should be placed so need to change list[number]

    if os.path.exists(txerrfile):
        file_exist = True
        print("File exist")   ## debug ##
        time1 = int(os.path.getmtime(txerrfile))
        time2 = int(time.time())
        if (time2 - time1) < 360:
            file_age = True
            print("File age looks good. Time is {}".format(time2 - time1)) ## debug ##
        else:
            file_age = False
            print("File age is too old. Time is {}".format(time2 - time1)) ## debug ##
    else:
        file_exist = False
        print("File doesn't exist.")  ## debug ##

    print(input_list)  ## debug ##
    if int(input_list[1]) > 100:
        if file_exist == True and file_age == True:
            with open(txerrfile, 'r') as fd:
                lines = fd.readlines()
                lines = [line.split(',', 1)[0] for line in lines]
                print(f"Before append in lines : {lines}")
                fd.close()
                lines.append(input_list[0])
                print(f"After append in lines : {lines}")
                if (len(lines) >= 4):    ## need to adjust 4 or 5?
                    dup_dict = {}
                    onetime_print = True  ## debug ##
                    for i in lines:
                        dup_dict[i] = lines.count(i)
                        if onetime_print == True:    ### debug ##
                            print(f"Not sorted : {dup_dict}")    ## debug ##
                            onetime_print = False ## debug
                        sorted_dict = dict(sorted(dup_dict.items(), key=lambda item: item[1], reverse=True))
                    print(f"Sort in descending order : {sorted_dict}")     ## debug ##
                    print(f"Highest TXErr LC or FM is {list(sorted_dict.keys())[0]}")    ## debug ##
                    #if we need to get all same values at the begining of script, need to add some more codes
                    #syslog.syslog(1,'Highest TXErr LC or FM is %s' % (list(sorted_dict.keys())[0]))

                    with open(txerrfile, 'a+') as fd:
                        fd.write(input_list[0] + "," + input_list[1] + "\n")
                        fd.close()
                        print("Appended")  ## debug ##
                        #syslog.syslog(2,'Total TXErr is increasing in Module Number %s ' % (list(sorted_dict.keys())[0]))
                else:
                    with open(txerrfile, 'a+') as fd:
                        fd.write(input_list[0] + "," + input_list[1] + "\n")
                        fd.close()
                        print("Appended")  ## debug ##
                        #syslog.syslog(2,'Total TXErr is increasing in Module Number %s ' % (list(sorted_dict.keys())[0]))
        else:
            with open(txerrfile, 'w') as fd:
                    fd.write(input_list[0] + "," + input_list[1] + "\n")
                    fd.close()
                    print("Created")   ## debug ##
                    #syslog.syslog(2,'Total TXErr is increasing in Module Number %s ' % (list(sorted_dict.keys())[0]))
    else:
        pass
    time.sleep(5)


"""
## EEM pattern to run this script
event syslog pattern ".INTERNAL_PORT_MONITOR_*.*_ERRORS_DETECTED"

Base Logic to create this code

파일이 있는지 없는지 여부를 확인 true/false
파일의 시간이 360 이하인지 확인 true/false

if err_num > 100 이면
	if exist = true and mtime=true
		file 열어서 라인수 읽어서 list에 저장하고 지금 발생한거 append하고 파일 close
		if list가 count가 >= 4
			중복되는 모듈판단하고 sev1 syslog 생성
			file open as a+
			라인 추가 
			sev2 syslog 생성  
		else
			file open as a+
			라인추가
			sev2 syslog 생성
	else
		파일 생성하고 값넣고 sev2 syslog생성
else 
	pass

첫 메시지의 TXErr은 항상 0부터 시작하고 TotalTXErr만 증가
TotalTXErr은 같은 모듈의 같은 iEthe 인터페이스에서 발생한 에러에 대해서만 SUM을 함 (2과 3를 비교시 1092 + 621 = 1713)
결국 TXErr가 중요한게 아닌 TotalTXErr 값이 중요
테스트 주기는 각 모듈별로 1분이며 순차적인지는 모르지만 조금씩 다르기 때문에  8slot의 경우 운좋으면 8개의 로그가 발생할 수 있음

N9K-C9516-1#  show system internal interface ii2/1/3 counters | inc ii|Crc|Errors | exclude Mac ; show system internal interface ii22/1/133 counters | inc ii|Crc|Errors | exclude Mac ;
Internal Port Statistics for Slot: ii2/1/3 If_Index 0x4a080002
    Crc:            0x0000000000000000/0
    Input Errors:   0x0000000000000000/0
    Output Errors:  0x000000000000f235/62005     >> LC iEth reports TX err (LC iEth의 TX로 깨질경우 일반적으로 CRC가 안보이나 어떤 경우는 CRC가 보일 수도 있음)
Internal Port Statistics for Slot: ii22/1/133 If_Index 0x4aa80084
    Crc:            0x000000000000f238/62008
    Input Errors:   0x000000000000f23a/62010   >> FM iEth reports RX CRC  (LC에서 잘못된 프래임이 FM으로 들어올 경우 CRC와 Input Error가 같이 보이게됨)
    Output Errors:  0x0000000000000000/0

2022-09-01        4:58:08      SRV_A4     %DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_TX_ERRORS_DETECTED: Module 2 received tx errors on internal interface ii2/1/3 since last run TXErr=0 TotalTXErr=4692  <<  1
2022-09-01        4:59:33      SRV_A4     %DEVICE_TEST-SLOT24-3-INTERNAL_PORT_MONITOR_TX_ERRORS_DETECTED: Module 24 received tx errors on internal interface ii24/1/11 since last run TXErr=0 TotalTXErr=2608 
2022-09-01        5:01:08      SRV_A4     %DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_CRC_ERRORS_DETECTED: Module 2 received tx errors on internal interface ii2/1/5 since last run TXErr=1091 TotalTXErr=1092  <<  2
2022-09-01        5:03:07      SRV_A4     %DEVICE_TEST-SLOT23-3-INTERNAL_PORT_MONITOR_CRC_ERRORS_DETECTED: Module 23 received tx errors on internal interface ii23/1/9 since last run TXErr=4840 TotalTXErr=4840
2022-09-01        5:03:08      SRV_A4     %DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_CRC_ERRORS_DETECTED: Module 2 received tx errors on internal interface ii2/1/14 since last run TXErr=1942 TotalTXErr=1942 
2022-09-01        5:03:08      SRV_A4     %DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_CRC_ERRORS_DETECTED: Module 2 received tx errors on internal interface ii2/1/13 since last run TXErr=11510 TotalTXErr=11510
2022-09-01        5:13:08      SRV_A4     %DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_CRC_ERRORS_DETECTED: Module 2 received tx errors on internal interface ii2/1/5 since last run TXErr=621 TotalTXErr=1713  << 3
2022-09-01        5:14:09      SRV_A4     %DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_CRC_ERRORS_DETECTED: Module 2 received tx errors on internal interface ii2/1/11 since last run TXErr=3828 TotalTXErr=3829
2022-09-01        5:14:09      SRV_A4     %DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_CRC_ERRORS_DETECTED: Module 2 received tx errors on internal interface ii2/1/7 since last run TXErr=2900 TotalTXErr=2900
2022-09-01        5:15:06      SRV_A4     %DEVICE_TEST-SLOT23-3-INTERNAL_PORT_MONITOR_TX_ERRORS_DETECTED: Module 23 received tx errors on internal interface ii23/1/9 since last run TXErr=0 TotalTXErr=4245 
2022-09-01        5:15:08      SRV_A4     %DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_CRC_ERRORS_DETECTED: Module 2 received tx errors on internal interface ii2/1/3 since last run TXErr=5788 TotalTXErr=5790
2022-09-01        5:16:09      SRV_A4     %DEVICE_TEST-SLOT2-3-INTERNAL_PORT_MONITOR_CRC_ERRORS_DETECTED: Module 2 received tx errors on internal interface ii2/1/1 since last run TXErr=1469 TotalTXErr=1470
2022-09-01        5:17:06      SRV_A4     %DEVICE_TEST-SLOT23-3-INTERNAL_PORT_MONITOR_TX_ERRORS_DETECTED: Module 23 received tx errors on internal interface ii23/1/11 since last run TXErr=0 TotalTXErr=793
"""



