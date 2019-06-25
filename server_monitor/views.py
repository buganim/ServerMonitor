from django.shortcuts import render
from django.views.generic import View, TemplateView
from . import models
from datetime import datetime
import time
import shelve
import json
import os
from . import ServerProjectMain
from threading import Thread

# Create your views here.


class myThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            ServerProjectMain.main()


myThread()
server_set = ServerProjectMain.server_set


def sort_dict(sort_var):
    sorted_dict = {}
    errors_dict = {}
    context = {}

    i = 0
    for server in server_set:
        try:
            server_data = {'name': server.name, 'ip': server.ip, 'port': server.port, 'cpu': server.cpu,
                           'mem': server.ram, 'strg': server.diskspace, 'net': server.netstats, 'time': server.time, 'test_time': server.last_test_time}
            context.update({i: server_data})
            i += 1
        except:
            continue

    if sort_var == 'net':
        i = 0
        k = len(context) + 10
        for key, value in context.items():
            if(value['net'] == 'Active'):
                sorted_dict.update({i: value})
                i += 1
            else:
                errors_dict.update({k: value})
                k += 1
        for one in errors_dict:
            sorted_dict.update({one: errors_dict[one]})

    elif sort_var == 'name':
        names_list = []
        i = 0
        for key, value in context.items():
            names_list.append(value['name'])
        names_list = sorted(names_list)
        for one in names_list:
            for key, value in context.items():
                if one == value['name']:
                    sorted_dict.update({i: value})
                    i += 1

    else:
        i = 0
        k = len(context) + 10
        while len(context):
            highest = 0
            for key, value in context.items():
                try:
                    current = float(value[sort_var].rstrip('%'))
                    if(current >= highest):
                        highest = float(value[sort_var].rstrip('%'))
                        current_item = value
                        current_key = key
                except:
                    if(value[sort_var] == 'Error'):
                        errors_dict.update({k: value})
                        error_key = key
            try:
                if(not current_item in sorted_dict.values()):
                    sorted_dict.update({i: current_item})
            except:
                pass
            try:
                del context[error_key]
            except:
                pass
            try:
                del context[current_key]
            except:
                pass
            i += 1
            k += 1
        for one in errors_dict:
            sorted_dict.update({one: errors_dict[one]})
    return sorted_dict


def StatusView(request):
    try:
        context = sort_dict('name')
        context = {'items': context}
    except:
        context = {}
    return render(request, 'status.html', context=context)


def CPUView(request):
    try:
        context = sort_dict('cpu')
        context = {'items': context}
    except:
        context = {}
    return render(request, 'status.html', context=context)


def MEMView(request):
    try:
        context = sort_dict('mem')
        context = {'items': context}
    except:
        context = {}
    return render(request, 'status.html', context=context)


def STRGView(request):
    try:
        context = sort_dict('strg')
        context = {'items': context}
    except:
        context = {}
    return render(request, 'status.html', context=context)


def NETView(request):
    try:
        context = sort_dict('net')
        context = {'items': context}
    except:
        context = {}
    return render(request, 'status.html', context=context)


def GraphView(request, ip):
    today = str(datetime.now())[:10]
    context = {today: ip}
    context = {'items': context}
    return render(request, 'graphs.html', context=context)


def AlertsView(request):
    context = {}
    i = 0
    for server in server_set:

        try:

            cpu = float(server.cpu.rstrip('%'))
            mem = float(server.ram.rstrip('%'))
            storage = float(server.diskspace.rstrip('%'))

            if(storage > 85):
                context.update({i: {'name': server.name, 'ip': server.ip,
                                    'status': server.diskspace, 'type': 'Disk Space'}})
            i += 1

            if(mem > 70):
                context.update(
                    {i: {'name': server.name, 'ip': server.ip, 'status': server.ram, 'type': 'Memory'}})
            i += 1

            if(cpu > 70):
                context.update(
                    {i: {'name': server.name, 'ip': server.ip, 'status': server.cpu, 'type': 'CPU'}})
            i += 1

        except:

            try:
                context.update({i: {'name': server.name, 'ip': server.ip,
                                    'status': 'No Communication', 'type': 'Network', 'row_color': 'red'}})
                i += 1

            except:
                continue

    context = {'items': context}
    return render(request, 'alerts.html', context=context)
