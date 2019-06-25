import os
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import interactive
import numpy as np
from datetime import datetime

BASE_DIR = r'D:\RND\Python\ServerMonitor\server_logs'
MEDIA_PATH = r'D:\RND\Python\ServerMonitor\Local\media'
today_date = str(datetime.now())[:10]
matplotlib.use('Agg')


def graph_stats(data_file, test_type, save_dir):
    data = []
    new_data = {}
    x = []
    y = []
    with open(data_file, 'r') as stats_file:
        data = str(stats_file.read())
        data = data.rsplit('\n')
        for one in data:
            try:
                curr_time = float(one.rsplit(' ')[1].rsplit(
                    ':')[0] + '.' + one.rsplit(' ')[1].rsplit(':')[1])
                curr_value = float(one.rsplit(' ')[2].rstrip('%)'))
                current = {curr_time: curr_value}
                new_data.update(current)
            except:
                continue

    for one in new_data.keys():
        x.append(one)
    for one in new_data.values():
        y.append(one)

    plt.xlabel('Time in Day')
    plt.ylabel(test_type)
    bottom, top = plt.ylim()
    left, right = plt.xlim()
    plt.ylim(bottom=0, top=100)
    plt.xlim(left=0, right=24)
    plt.step(x, y)
    plt.savefig('{}\\{}_{}_Graph.png'.format(save_dir, today_date, test_type))
    plt.clf()
    plt.close()


def main():
    for one in os.listdir(BASE_DIR):
        current_dir = os.path.join(BASE_DIR, one)
        curr_media_dir = os.path.join(MEDIA_PATH, one)
        curr_cpu_dir = os.path.join(current_dir, 'CPU')
        curr_ram_dir = os.path.join(current_dir, 'RAM')
        cpu_images_dir = os.path.join(curr_media_dir, 'CPU')
        ram_images_dir = os.path.join(curr_media_dir, 'RAM')
        if not os.path.exists(cpu_images_dir):
            os.makedirs(cpu_images_dir)
        if not os.path.exists(ram_images_dir):
            os.makedirs(ram_images_dir)
        for one in os.listdir(curr_cpu_dir):
            if today_date in one and not '.png' in one:
                curr_cpu_file = os.path.join(curr_cpu_dir, one)
                graph_stats(curr_cpu_file, 'CPU', curr_cpu_dir)
                graph_stats(curr_cpu_file, 'CPU', cpu_images_dir)
        for one in os.listdir(curr_ram_dir):
            if today_date in one and not '.png' in one:
                curr_ram_file = os.path.join(curr_ram_dir, one)
                graph_stats(curr_ram_file, 'RAM', curr_ram_dir)
                graph_stats(curr_ram_file, 'RAM', ram_images_dir)
