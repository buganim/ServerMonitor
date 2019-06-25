import tcpClientSide
import shelve
import time
import os
from datetime import datetime
import json
from threading import Thread, Event
from threading import Lock

stop_event = Event()
LOGS_PATH = r'\\192.168.20.3\fingenom shares\RND\IT\monitor_logs'
MEDIA_PATH = r'C:\inetpub\wwwroot\buganim\media'
mutex = Lock()


def test_server(key,server_dict):
    name = key
    port = server_dict[key][1]
    ip = server_dict[key][0]
    cpu = tcpClientSide.get_server_stats(ip,port,'cpu')
    ram = tcpClientSide.get_server_stats(ip,port,'ram')
    net = tcpClientSide.get_server_stats(ip,port,'network')
    storage = tcpClientSide.get_server_stats(ip,port,'diskspace')
    process_list = ''
    try:
        ram_tester = float(ram.rstrip('%'))
    except:
        ram_tester = 0
    if ram_tester > 90:
        process_list = tcpClientSide.get_server_stats(ip,port,'high_ram')
    result_time = str(datetime.now())[:19]

    mutex.acquire()
    with shelve.open(os.path.join(os.path.dirname(__file__),'data')) as db:
        db[key] = name
        db[key+'_port'] = port
        db[key+'_ip'] = ip
        db[key+'_cpu'] = cpu
        db[key+'_ram']= ram
        db[key+'_net'] = net
        db[key+'_storage'] = storage
        db[key+'_result_time'] = result_time
    mutex.release()
    writeToLog(name,ip,cpu,ram,net,storage,process_list,result_time)
    print('Extracted data from: {}'.format(name))
    if stop_event.is_set():
        return


def writeToLog(server_name,ip,CPU,RAM,NET,DSK,PRC,res_time):
    DATE_NOW = str(datetime.now())[:10]
    SERVER_PATH = os.path.join(LOGS_PATH, ip)
    PATHS_DICT = {
        'CPU_PATH': os.path.join(SERVER_PATH, 'CPU'),
        'MEM_PATH': os.path.join(SERVER_PATH, 'RAM'),
        'NET_PATH': os.path.join(SERVER_PATH, 'NET'),
        'STRG_PATH': os.path.join(SERVER_PATH, 'DSK')
    }
    for one in PATHS_DICT:
        CURRENT_LOG = os.path.join(PATHS_DICT[one], DATE_NOW + '.txt')
        LOG_VALUE = os.path.dirname(CURRENT_LOG)[-3:]
        if not os.path.exists(PATHS_DICT[one]):
            os.makedirs(PATHS_DICT[one])
        with open(CURRENT_LOG, 'a') as logger:
            logger.write(res_time + ' ' + eval(LOG_VALUE) +'\n')
    if not PRC == '':
        with open(os.path.join(SERVER_PATH, 'PROCESS_LIST.txt'), 'w') as logger:
            logger.write(res_time)
            logger.write(PRC)
    
def cleanLogsDir(A,days=7, *arg):
    now = time.time()
    day = 86400
    for item in os.listdir(A):
        file_path = os.path.join(A, item)
        if os.path.isfile(file_path):
            filemtime = os.path.getmtime(file_path)
            if(now-(filemtime+(day*days))>0):
                os.remove(file_path)
        elif os.path.isdir(file_path):
            subdir = os.path.join(A, file_path)
            cleanLogsDir(subdir,days,*arg,os.path.join(A, item))


while True:
    json_file = open(r'C:\inetpub\wwwroot\buganim\server_list\all_servers.json','r')
    server_dict = json.load(json_file)
    threads = []
    json_file.close()
    for key in server_dict:
        t = Thread(target=test_server, args=(key,server_dict))
        stop_event.set()
        threads.append(t)
    for t in threads:
        t.start()
        time.sleep(0.2)
    for t in threads:
        t.join(timeout=10)
    time.sleep(2)
    os.system(r'C:\inetpub\wwwroot\buganim\backend\Data\Graphs\graph.exe')
    cleanLogsDir(LOGS_PATH)
    cleanLogsDir(MEDIA_PATH,days=30)