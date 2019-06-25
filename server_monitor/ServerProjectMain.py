import json
import time
import threading as th
import os
from . import graph
from . import CServer

LOGS_PATH = r'D:\RND\Python\ServerMonitor\server_logs'
MEDIA_PATH = r'D:\RND\Python\ServerMonitor\Local\media'
server_set = []


def main():
    while True:
        json_file = open(
            r"D:\RND\Python\ServerMonitor\Local\server_list\all_servers.json", 'r')
        server_dict = json.load(json_file)
        json_file.close()

        if len(server_dict) > len(server_set):
            for key, value in server_dict.items():
                server = CServer.Server(key, value[0], value[1])
                server_set.append(server)

        threads_arr = []

        for server in server_set:
            thread = th.Thread(target=server.updateStatus)
            threads_arr.append(thread)

        for thread in threads_arr:
            thread.start()

        for thread in threads_arr:
            thread.join(timeout=10)

        graph.main()
        cleanLogsDir(LOGS_PATH)
        cleanLogsDir(MEDIA_PATH, days=30)
        time.sleep(5)


def cleanLogsDir(A, days=7, *arg):
    now = time.time()
    day = 86400
    for item in os.listdir(A):
        file_path = os.path.join(A, item)
        if os.path.isfile(file_path):
            filemtime = os.path.getmtime(file_path)
            if(now-(filemtime+(day*days)) > 0):
                os.remove(file_path)
        elif os.path.isdir(file_path):
            subdir = os.path.join(A, file_path)
            cleanLogsDir(subdir, days, *arg, os.path.join(A, item))
