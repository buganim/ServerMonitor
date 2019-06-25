#!/usr/bin/env python

import socket
import shutil
from psutil import virtual_memory
import psutil


##return disk size function:
def get_disk(disk_name):
	return_value = 0
	total, used, free = shutil.disk_usage(disk_name)
	total = total // (2**30)
	used1 = used // (2**30)
	return_value = (used1 / total)*100
	return_value = int(return_value)
	return_value = str(return_value)
	return return_value + '%'

##return RAM percent:
def get_ram():
	ram_percent = virtual_memory()
	ram_percent.total
	ram_result = "{}%".format(ram_percent.percent)
	return ram_result

##return cpu percent:
def get_cpu():
	cpu_percent = str(int(psutil.cpu_percent(interval=1))) + '%'
	return cpu_percent

##return net_stats:
def get_net():
	net_stats = (psutil.net_io_counters())
	bytes_recv = net_stats.bytes_recv
	return_msg = ''
	if(bytes_recv > 0):
		return_msg += "Active"
	else:
		return_msg += "Disconnected"
	return return_msg


TCP_IP = ""
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
    try:
        conn, addr = s.accept()
        print ('Connection address:', addr)
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data: 
                break
            disk_size = get_disk('//')
            ram_result = get_ram()
            cpu_percent = get_cpu()
            net_stats = get_net()
            if(data.decode('utf-8') == 'diskspace'):
                conn.send(disk_size.encode('utf-8'))
            elif(data.decode('utf-8') == 'ram'):
                conn.send(ram_result.encode('utf-8'))
            elif(data.decode('utf-8') == 'cpu') :
                conn.send(str(cpu_percent).encode('utf-8'))
            elif(data.decode('utf-8') == 'network') :
                conn.send(str(net_stats).encode('utf-8'))
            else:
                conn.send('Nothing asked'.encode('utf-8'))
            conn.close()
    except:
        continue