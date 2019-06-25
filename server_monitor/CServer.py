import os
import random
import socket
import time
from datetime import datetime


class Server:

    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.cpu = "Error"
        self.ram = "Error"
        self.diskspace = "Error"
        self.netstats = "Error"
        self.time = 0
        self.date = 0
        self.process_list = 0
        self.last_test_time = 0
        self.logs_dir = 'D:\\RND\\Python\\ServerMonitor\\server_logs\\{}'.format(
            self.ip)
        self.paths_dict = {
            'CPU_PATH': os.path.join(self.logs_dir, 'CPU'),
            'MEM_PATH': os.path.join(self.logs_dir, 'RAM'),
            'NET_PATH': os.path.join(self.logs_dir, 'NET'),
            'STRG_PATH': os.path.join(self.logs_dir, 'DSK')
        }

    def updateStatus(self):
        try:
            ts = time.time()
            self.time = str(datetime.now())[:19]
            self.date = self.time[:10]
            self.cpu = self.requestStat(self.ip, self.port, 'cpu')
            self.ram = self.requestStat(self.ip, self.port, 'ram')
            self.diskspace = self.requestStat(self.ip, self.port, 'diskspace')
            self.netstats = "Active"
            # self.netstats = self.requestStat(self.ip, self.port, 'network')
            # try:
            #     ram_tester = float(self.ram.rstrip('%'))
            # except:
            #     ram_tester = 0
            # if ram_tester > 90:
            #     self.process_list = self.requestStat(
            #         self.ip, self.port, 'high_ram')
        except:
            pass
        self.writeToLog()
        te = time.time()
        self.last_test_time = ('%2.3f Seconds' % (te - ts))

    def requestStat(self, ip, port, request):
        # try:
        #     dongle = ip, port
        #     BUFFER_SIZE = 10000
        #     request = request.encode('utf-8')
        #     conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     conn.connect(dongle)
        #     conn.send(request)
        #     data = conn.recv(BUFFER_SIZE)
        #     conn.close()
        #     return(data.decode('utf-8'))
        # except:
        #     return('Error')
        return ("{}%".format(random.randint(0, 100)))

    def writeToLog(self):
        CPU = self.cpu
        RAM = self.ram
        NET = self.netstats
        DSK = self.diskspace
        PRC = self.process_list
        for one in self.paths_dict:
            CURRENT_LOG = os.path.join(
                self.paths_dict[one], self.date + '.txt')
            LOG_VALUE = os.path.dirname(CURRENT_LOG)[-3:]
            if not os.path.exists(self.paths_dict[one]):
                os.makedirs(self.paths_dict[one])
            with open(CURRENT_LOG, 'a') as logger:
                logger.write(self.time + ' ' + eval(LOG_VALUE) + '\n')
        if not self.process_list == 0:
            with open(os.path.join(self.logs_dir, 'PROCESS_LIST.txt'), 'w') as logger:
                logger.write(self.time + ' ')
                logger.write(self.process_list)
            self.process_list = 0

    def __str__(self):
        return({'name': self.name, 'ip': self.ip, 'port': self.port, 'cpu': self.cpu, 'mem': self.ram, 'strg': self.diskspace, 'net': self.netstats, 'time': self.time, 'test_time': self.last_test_time})
