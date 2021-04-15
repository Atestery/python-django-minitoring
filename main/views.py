from django.shortcuts import render
from django.http import HttpResponse, request
from django.template import context
from django.http import HttpResponse
from django.utils.html import escape
import threading
import requests
from openpyxl import load_workbook
import colorama
colorama.init()
from termcolor import colored
from playsound import playsound
from subprocess import PIPE, Popen
import os
import time
import datetime
from datetime import datetime
import subprocess
from pysnmp.hlapi import *
from ipaddress import *

messtime = 0
blockstart = True
stoppotok = False
critical_temp = ''
statetemp = ''
offlinehost2 = ''
temp1 = ''
temp2 = ''
temp3 = ''
result = ''




def startprogramm():
    try:
        global stoppotok
        global blockstart
        stoppotok = True
        if(blockstart == True):
            blockstart = False
            t1 = threading.Thread(target=startping, name="potok1-startping")
            t1.start()



    except Exception as err:
        log("Сработало Исключение в функции Start().")
        log(str(err))

def stopprogramm():
    global stoppotok
    global blockstart
    try:
        print("остановка основного потока")
        stoppotok = False
        blockstart = True
        t1.join()
    except Exception as err:
        log("Сработало Исключение в функции stopprogramm.")
        log(str(err))
        print("Сработало Исключение в функции stopprogramm.")
        print(str(err))



def snmp_getcmd(community, ip, port, OID):
    return (getCmd(SnmpEngine(),
                   CommunityData(community, mpModel=0),
                   UdpTransportTarget((ip, port)),
                   ContextData(),
                   ObjectType(ObjectIdentity(OID))))


def snmp_get_next(community, ip, port, OID):
    errorIndication, errorStatus, errorIndex, varBinds = next(snmp_getcmd(community, ip, port, OID))
    for name, val in varBinds:
        return (val.prettyPrint())


def snmp_func_return(host_comment, ipaddr, port, community, oid):
    try:
        global temp1
        global temp2
        global temp3
        global result

        global offlinehost2
        global statetemp
        global critical_temp

        systemp = ''
        print('\033[92mВыполняю пинг: ' + host_comment + ': ' + ipaddr)
        res = Popen("ping -n 1 " + ipaddr, shell=True, stdout=PIPE)
        out = str(res.communicate()[0].decode("CP866"))
        if out.find("100% потерь") != -1:
            res = Popen("ping -n 1 " + ipaddr, shell=True, stdout=PIPE)
            out = str(res.communicate()[0].decode("CP866"))
            print('\033[92mВыполняю пинг: ' + ipaddr)
            if out.find("100% потерь") != -1:
                res = Popen("ping -n 1 " + ipaddr, shell=True, stdout=PIPE)
                out = str(res.communicate()[0].decode("CP866"))
                if out.find("100% потерь") != -1:
                    print('\033[0m __________________________________________________________________')
                    print('\033[1;31mНе пингуется: ' + host_comment + ': ' + ipaddr)
                    print('\033[0m __________________________________________________________________')
                    playsound('main\\work_files\\error_ping.mp3')
                    result = result + '<br>' + '<span class=' + '"' + 'colortextmaroon' + '">' + 'Не пингуется: ' + host_comment + ': ' + ipaddr + '</span>'
                    log('Не пингуется: ' + host_comment + ': ' + ipaddr)
                    offlinehost2 = offlinehost2 + ' ' + host_comment + ': ' + ipaddr + '\n'
                else:
                    systemp = (snmp_get_next(community, ipaddr, port, oid))
                    print('\033[92m Проверка температуры ' + str(systemp) + '*C')
                    statetemp = statetemp + host_comment + '-ip-' + ipaddr + ': ' + str(systemp) + '*C' + '\n'
                    if (systemp == None):
                        statetemp = statetemp + host_comment + '-ip-' + ipaddr + ': НЕТ ДАННЫХ!' + '*C' + '\n'
                        if (host_comment == 'temp_1'):
                            temp1 = '<span class=' + '"' + 'colortextolive' + '">' + 'НЕТ ДАННЫХ!' + '</span>'
                        if (host_comment == 'temp_2'):
                            temp2 = '<span class=' + '"' + 'colortextolive' + '">' + 'НЕТ ДАННЫХ!' + '</span>'
                        if (host_comment == 'temp_3'):
                            temp3 = '<span class=' + '"' + 'colortextolive' + '">' + 'НЕТ ДАННЫХ!' + '</span>'
                    if (systemp != '' and systemp != None):
                        if (int(systemp) <= 25):
                            print('\033[92mтемпература в пределах нормы : ' + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C')
                            if (host_comment == 'temp_1'):
                                temp1 = '<span class=' + '"' + 'colortextgreen' + '">' + str(systemp) + '</span>'
                            if (host_comment == 'temp_2'):
                                temp2 = '<span class=' + '"' + 'colortextgreen' + '">' + str(systemp) + '</span>'
                            if (host_comment == 'temp_3'):
                                temp3 = '<span class=' + '"' + 'colortextgreen' + '">' + str(systemp) + '</span>'
                        if (int(systemp) == 26):
                            print('\033[1;33m Внимание Температура Завышена ' + host_comment + '-' + ipaddr + ': ' + str(systemp))
                            if (host_comment == 'temp_1'):
                                temp1 = '<span class=' + '"' + 'colortextyellow' + '">' + str(systemp) + '</span>'
                            if (host_comment == 'temp_2'):
                                temp2= '<span class=' + '"' + 'colortextyellow' + '">' + str(systemp) + '</span>'
                            if (host_comment == 'temp_3'):
                                temp3 = '<span class=' + '"' + 'colortextyellow' + '">' + str(systemp) + '</span>'
                            playsound('main\\work_files\\st.mp3')
                            playsound('main\\work_files\\st.mp3')
                            playsound('main\\work_files\\st.mp3')
                            playsound('main\\work_files\\st.mp3')
                            log('Внимание Температура Завышена ' + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C')
                            print('Внимание Температура Завышена ' + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C')
                            result = result + '<br>' + '<span class=' + '"' + 'colortextyellow' + '">' + 'Внимание Температура Завышена ' + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C'  + '</span>'
                            critical_temp = critical_temp + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C' + '\n'
                        if (int(systemp) >= 27):
                            if (host_comment == 'temp_1'):
                                temp1 = '<span class=' + '"' + 'colortextred' + '">' + str(systemp) + '</span>'
                            if (host_comment == 'temp_2'):
                                temp2 = '<span class=' + '"' + 'colortextred' + '">' + str(systemp) + '</span>'
                            if (host_comment == 'temp_3'):
                                #l6.config(bg='red', text=str(systemp))
                                temp3 = '<span class=' + '"' + 'colortextred' + '">' + str(systemp) + '</span>'
                            print('\033[0m __________________________________________________________________')
                            print('\033[1;31m АВАРИЯ ПО ТЕМПЕРАТУРЕ: ' + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C')
                            print('\033[0m __________________________________________________________________')
                            result = result + '<br>' + '<span class=' + '"' + 'colortextred' + '">' + 'АВАРИЯ ПО ТЕМПЕРАТУРЕ: ' + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C' + '</span>'
                            playsound('main\\work_files\\st.mp3')
                            playsound('main\\work_files\\st.mp3')
                            playsound('main\\work_files\\st.mp3')
                            playsound('main\\work_files\\st.mp3')
                            playsound('main\\work_files\\st.mp3')
                            playsound('main\\work_files\\st.mp3')
                            playsound('main\\work_files\\st.mp3')
                            playsound('main\\work_files\\st.mp3')
                            log('АВАРИЯ ПО ТЕМПЕРАТУРЕ: ' + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C')
                            critical_temp = critical_temp + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C' + '\n'
        else:
            systemp = (snmp_get_next(community, ipaddr, port, oid))
            print('\033[92m Проверка температуры ' + str(systemp) + '*C')
            statetemp = statetemp + host_comment + '-' + ipaddr + ':' + str(systemp) + '*C' + '\n'
            if (systemp == None):
                statetemp = statetemp + host_comment + '-ip-' + ipaddr + ': НЕТ ДАННЫХ!' + '*C' + '\n'
                if (host_comment == 'temp_1'):
                    temp1 = '<span class=' + '"' + 'colortextolive' + '">' + 'НЕТ ДАННЫХ!' + '</span>'
                if (host_comment == 'temp_2'):
                    temp2 = '<span class=' + '"' + 'colortextolive' + '">' + 'НЕТ ДАННЫХ!' + '</span>'
                if (host_comment == 'temp_3'):
                    temp3 = '<span class=' + '"' + 'colortextolive' + '">' + 'НЕТ ДАННЫХ!' + '</span>'
            if (systemp != '' and systemp != None):
                if (int(systemp) <= 25):
                    if (host_comment == 'temp_1'):
                        temp1 = '<span class=' + '"' + 'colortextgreen' + '">' + str(systemp) + '</span>'
                    if (host_comment == 'temp_2'):
                        temp2 = '<span class=' + '"' + 'colortextgreen' + '">' + str(systemp) + '</span>'
                    if (host_comment == 'temp_3'):
                        temp3 = '<span class=' + '"' + 'colortextgreen' + '">' + str(systemp) + '</span>'
                    print('\033[92mтемпература в пределах нормы : ' + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C')
                if (int(systemp) == 26):
                    print('\033[1;33m Внимание Температура Завышена ' + host_comment + '-' + ipaddr + ': ' + str(systemp))
                    result = result + '<br>' + '<span class=' + '"' + 'colortextyellow' + '">' + 'Внимание Температура Завышена ' + host_comment + '-' + ipaddr + ': ' + str(systemp) + '</span>'

                    if (host_comment == 'temp_1'):
                        temp1 = '<span class=' + '"' + 'colortextyellow' + '">' + str(systemp) + '</span>'
                    if (host_comment == 'temp_2'):
                        temp2 = '<span class=' + '"' + 'colortextyellow' + '">' + str(systemp) + '</span>'
                    if (host_comment == 'temp_3'):
                        temp3 = '<span class=' + '"' + 'colortextyellow' + '">' + str(systemp) + '</span>'
                    playsound('main\\work_files\\st.mp3')
                    playsound('main\\work_files\\st.mp3')
                    playsound('main\\work_files\\st.mp3')
                    playsound('main\\work_files\\st.mp3')
                    log('Внимание Температура Завышена ' + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C')
                    critical_temp = critical_temp + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C' + '\n'
                if (int(systemp) >= 27):
                    if (host_comment == 'temp_1'):
                        temp1 = '<span class=' + '"' + 'colortextred' + '">' + str(systemp) + '</span>'
                    if (host_comment == 'temp_2'):
                        temp2 = '<span class=' + '"' + 'colortextred' + '">' + str(systemp) + '</span>'
                    if (host_comment == 'temp_3'):
                        temp3 = '<span class=' + '"' + 'colortextred' + '">' + str(systemp) + '</span>'
                    print('\033[0m __________________________________________________________________')
                    print('\033[1;31m АВАРИЯ ПО ТЕМПЕРАТУРЕ: ' + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C')
                    print('\033[0m __________________________________________________________________')
                    result = result + '<br>' + '<span class=' + '"' + 'colortextred' + '">' + 'АВАРИЯ ПО ТЕМПЕРАТУРЕ: ' + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C' + '</span>'

                    playsound('main\\work_files\\st.mp3')
                    playsound('main\\work_files\\st.mp3')
                    playsound('main\\work_files\\st.mp3')
                    playsound('main\\work_files\\st.mp3')
                    playsound('main\\work_files\\st.mp3')
                    playsound('main\\work_files\\st.mp3')
                    playsound('main\\work_files\\st.mp3')
                    playsound('main\\work_files\\st.mp3')
                    log('АВАРИЯ ПО ТЕМПЕРАТУРЕ: ' + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C')
                    critical_temp = critical_temp + host_comment + '-' + ipaddr + ': ' + str(systemp) + '*C' + '\n'
    except Exception as err:
        log("Сработало Исключение в функции snmp_func_return.")
        log(str(err))
        print("Сработало Исключение в функции snmp_func_return")
        print("перезапуск функции startping через 60 сек. из-за snmp_func_return!!!")
        time.sleep(60)
        startping()







def log(message):
    try:
        from datetime import datetime
        datein = datetime.strftime(datetime.now(), "%d.%m.%Y")
        if os.path.exists('main\\work_files\log\\' + datein + '\\'):
            file = open('main\\work_files\\log\\' + datein + '\\' + datein + '.log', "a")
            file.write("\n")
            file.write("\n")
            file.write("0-------------------------------------------0")
            file.write("\n")
            file.write(str(datetime.now()))
            file.write("\n")
            file.write(message)
            file.write("\n")
            file.write("1-------------------------------------------1")
            file.write("\n")
            file.write("\n")
            file.close()
        else:
            # Если такой папки нет то создаем ее и пишем в нее
            os.makedirs('main\\work_files\\log\\' + datein + '\\')  # Создаю такую папку и пишу в нее
            file = open('main\\work_files\\log\\' + datein + '\\' + datein + '.log', 'a')
            file.write("\n")
            file.write("\n")
            file.write("0-------------------------------------------0")
            file.write("\n")
            file.write(str(datetime.now()))
            file.write("\n")
            file.write(message)
            file.write("\n")
            file.write("1-------------------------------------------1")
            file.write("\n")
            file.write("\n")
            file.close()
    except Exception as err:
        log("Сработало Исключение в функции log.")
        log(str(err))

def startping():
    try:
        global result
        os.system('CLS')
        global offlinehost2
        global statetemp
        global critical_temp
        global stoppotok
        global messtime
        while stoppotok:
            result = ''
            offlinehost = ''
            timeping = ''
            f = open('main\\work_files\\hosts.txt', 'r')
            spisok = [line.strip() for line in f]
            f.close()
            dlinamas = len(spisok)
            for i in range(dlinamas):
                if (stoppotok == False):
                    break
                arr = spisok[i].split(';')
                hostname = arr[0]
                res = Popen("ping -n 1 " + hostname, shell=True, stdout=PIPE)
                out = str(res.communicate()[0].decode("CP866"))
                print('\033[92mВыполняю пинг: ' + arr[0])
                if out.find("100% потерь") != -1:
                    res = Popen("ping -n 1 " + hostname, shell=True, stdout=PIPE)
                    out = str(res.communicate()[0].decode("CP866"))
                    if out.find("100% потерь") != -1:
                        res = Popen("ping -n 1 " + hostname, shell=True, stdout=PIPE)
                        out = str(res.communicate()[0].decode("CP866"))
                        if out.find("100% потерь") != -1:
                            res = Popen("ping -n 1 " + hostname, shell=True, stdout=PIPE)
                            out = str(res.communicate()[0].decode("CP866"))
                            if out.find("100% потерь") != -1:
                                print('\033[0m __________________________________________________________________')
                                print('\033[1;31mНе пингуется: ' + arr[0] + ' ' + arr[1] + ' ' + arr[2])
                                print('\033[0m __________________________________________________________________')
                                playsound('main\\work_files\\error_ping.mp3')
                                result = result + '<br>' + '<span class=' + '"' + 'colortextmaroon' + '">' + 'Не пингуется: ' + \
                                         arr[0] + ' ' + arr[1] + ' ' + arr[2] + '</span>'
                                log('Не пингуется: ' + arr[0] + ' ' + arr[1] + ' ' + arr[2])
                                offlinehost = offlinehost + arr[0] + ' ' + arr[1] + ' ' + arr[2] + '\n'
                if out.find("Среднее = ") != -1:
                    index = out.find("Среднее = ")
                    index = index + 10
                    responmc = ''
                    while index != index + 10:
                        if out[index] != ' ':
                            responmc = responmc + out[index]
                        else:
                            break
                        index = index + 1
                    responmc = int(responmc)
                    if responmc > 1000:
                        print('\033[1;33m Внимание задержка пинга более 1000мс: ' + str(responmc) + ' ', arr[0], arr[1],
                              arr[2])
                        playsound('main\\work_files\\err_time_ms.mp3')
                        result = result + '<br>' + '<span class=' + '"' + 'colortextyellow' + '">' + 'Внимание задержка пинга более 1000мс: ' + str(
                            responmc) + ' ', arr[0], arr[1], arr[2] + '</span>'
                        log('Задержка пинга: ' + str(responmc) + ' ' + arr[0] + ' ' + arr[1] + ' ' + arr[2])
                        timeping = timeping + '\nЗадержка пинга: ' + str(responmc) + ': ' + arr[0] + ' ' + arr[
                            1] + ' ' + arr[2] + '\n'
            f = open('main\\work_files\\snmp.txt', 'r')
            spisok = [line.strip() for line in f]
            f.close()
            dlinamas = len(spisok)
            for i in range(dlinamas):
                if (stoppotok == False):
                    break
                arr = spisok[i].split(';')
                host_comment = arr[0]
                ipaddr = arr[1]
                port = arr[2]
                community = arr[3]
                oid = arr[4]
                snmp_func_return(host_comment, ipaddr, port, community, oid)

            wb_val = load_workbook(filename='main\\work_files\\Servers.xlsx', data_only=True)
            sheet_val = wb_val['Лист1']
            i = 0
            while i != 5000:
                if (stoppotok == False):
                    break
                i = i + 1
                A_val = sheet_val['A' + str(i)].value
                B_val = sheet_val['B' + str(i)].value
                color_cell = sheet_val['A' + str(i)].fill.start_color.index
                if A_val != '' and A_val != None and A_val != 'IP' and A_val != 'ESXi ХОСТЫ' and color_cell != 'FFFF0000':
                    hostname = A_val
                    res = Popen("ping -n 1 " + hostname, shell=True, stdout=PIPE)
                    out = str(res.communicate()[0].decode("CP866"))
                    print('\033[92mВыполняю пинг: ' + hostname)

                    if out.find("100% потерь") != -1:
                        res = Popen("ping -n 1 " + hostname, shell=True, stdout=PIPE)
                        out = str(res.communicate()[0].decode("CP866"))
                        if out.find("100% потерь") != -1:
                            res = Popen("ping -n 1 " + hostname, shell=True, stdout=PIPE)
                            out = str(res.communicate()[0].decode("CP866"))
                            if out.find("100% потерь") != -1:
                                res = Popen("ping -n 1 " + hostname, shell=True, stdout=PIPE)
                                out = str(res.communicate()[0].decode("CP866"))
                                if out.find("100% потерь") != -1:
                                    print('\033[0m _________________________________________________')
                                    print('\033[1;31mНе пингуется: ' + hostname + ' ' + B_val)
                                    print('\033[0m _________________________________________________')
                                    print("Должна играть песня")
                                    playsound('main\\work_files\\error_ping.mp3')
                                    result = result + '<br>' + '<span class=' + '"' + 'colortextmaroon' + '">' + 'Не пингуется: ' + hostname + ' ' + B_val + '</span>'
                                    log('Не пингуется: ' + hostname + ' ' + B_val)
                                    offlinehost = offlinehost + hostname + ' ' + B_val + '\n'
                    if out.find("Среднее = ") != -1:
                        index = out.find("Среднее = ")
                        index = index + 10
                        responmc = ''
                        while index != index + 10:
                            if out[index] != ' ':
                                responmc = responmc + out[index]
                            else:
                                break
                            index = index + 1
                        responmc = int(responmc)
                        if responmc > 1000:
                            print('\033[1;33m Внимание задержка пинга более 1000мс: ' + str(
                                responmc) + ' ' + hostname + ' ' + B_val)
                            playsound('main\\work_files\\err_time_ms.mp3')
                            result = result + '<br>' + '<span class=' + '"' + 'colortextyellow' + '">' + 'Внимание задержка пинга более 1000мс: ' + str(
                                responmc) + ' ' + hostname + ' ' + B_val + '</span>'
                            log('Задержка пинга: ' + str(responmc) + ' ' + hostname + ' ' + B_val)
                            timeping = timeping + '\nЗадержка пинга: ' + str(
                                responmc) + ': ' + hostname + ' ' + B_val + '\n'


            os.system('CLS')
            if offlinehost2 != '':
                print('\033[1;31m Авария по Температуре: :\n' + offlinehost2)
            if critical_temp != '':
                print('\033[1;31m Авария по Температуре: :\n' + critical_temp)
            if offlinehost != '':
                print('\033[1;31mНе пингуется :\n' + offlinehost)
            if timeping != '':
                print('\033[1;33m Внимание задержка пинга более 1000мс ' + timeping)
            if (stoppotok == False):
                break


            i = 60
            while i != 0:
                messtime = i
                if (stoppotok == False):
                    break
                if offlinehost2 != '':
                    print('\033[1;31m Авария по Температуре: \n' + offlinehost2)
                if statetemp != '':
                    print('\033[96mТекущие показатели температуры: \n' + statetemp + '\033[0m')
                if critical_temp != '':
                    print('\033[1;31m Авария по Температуре: :\n' + critical_temp)
                if offlinehost != '':
                    print('\033[1;31mНе пингуется :\n' + offlinehost)
                if timeping != '':
                    print('\033[1;33m Внимание задержка пинга более 1000мс: \n' + timeping)
                print('\033[0m\n\n\n\n\n\n\n\nПауза 1 минуту, осталось: ' + str(i) + ' сек.')
                i = i - 1
                time.sleep(1)
                os.system('CLS')
            offlinehost = ''
            timeping = ''

            offlinehost2 = ''
            statetemp = ''
            critical_temp = ''
    except Exception as err:
        print(str(err))
        print("Ошибка функции startping() " + str(err))
        log("Ошибка функции startping() " + str(err))


def index(request):
    global temp1
    global temp2
    global temp3
    global result
    global stoppotok
    global messtime

    if request.method == 'POST' and 'htmlbutton1' in request.POST:
        print('Нажата кнопка 1')
        startprogramm()
    if request.method == 'POST' and 'htmlbutton2' in request.POST:
        print('Нажата кнопка 2')
        stopprogramm()

    if(stoppotok == True):
        stats = '<span class=' + '"' + 'colortextgreen' + '">' + 'Вкл.' + '</span>'
    else:
        stats = '<span class=' + '"' + 'colortextred' + '">' + 'Откл.' + '</span>'


    data = {"result": result, "temp1": temp1, "temp2": temp2, "temp3": temp3, "message": stats, "messtime": str(messtime)}
    return render(request, "main/index.html", data)



def about(request):
    return render(request, 'main/about.html')


print('Программа запущена.')
log('Программа запущена.')

