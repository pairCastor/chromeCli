#!/usr/bin/python3

from sys import argv, stderr
from enum import Enum
from time import sleep
from zeroconf import ServiceBrowser, Zeroconf

def usage(progname):
    print("Usage: " +progname +" --devices [--timeout]\n"\
        "or: " +progname +" --connect ADDR\n"\
        "\n"\
        "chromecli chromecast client implementation\n"\
        "\n"\
        "--devices\tscan network for chromecast devices\n\n"\
        "--connect ADDR:PORT\tconnect to device located at ADDR\n\n"\
        "--timeout=SECONDS\tsearch for devices until timeout is reached (default is 5)\n"\
        "\n"\
        "Examples:\n"\
        "chromecli --devices\tlist devices\n\n"\
        "chromecli --connect 192.168.5.5:8008\tconnect to chromecast located at address\n\n")

def version():
    print("chromecli 0.2\n"\
        "Copyright (C) 2016 Free Software Foundation, Inc.\n"\
        "License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.\n"\
        "This is free software: you are free to change and redistribute it.\n"\
        "There is NO WARRANTY, to the extent permitted by law.\n"\
        "\n"\
        "Written by isundil.\n")

class ChromecastReceiver(object):
    def __init__(self, name, info):
        self.name = name
        self.info = info

class ChromecastListener(object):
    def __init__(self):
        self.zeroconf = Zeroconf()
        self.browser = ServiceBrowser(self.zeroconf, "_googlecast._tcp.local.", self)
        self.receivers = []

    def __del__(self):
        self.close()

    def close(self):
        if self.zeroconf != None:
            self.zeroconf.close()
            self.zeroconf = None

    def add_service(self, zeroconf, type, name):
        self.receivers.append(ChromecastReceiver(name, zeroconf.get_service_info(type, name)))

    def del_service(self, zeroconf, type, name):
        for i in range(len(self.receivers)):
            if (self.receivers[i].name == name):
                self.receivers.pop(i)
                break

class ActionType(Enum):
    listDevices = 1
    connect     = 2

def listDevices(timeout):
    listener = ChromecastListener()
    print("discovering devices...")
    sleep(timeout)
    listener.close()
    devices = listener.receivers
    for device in devices:
        ip = "{0}.{1}.{2}.{3}:{4}".format(
                device.info.address[0],
                device.info.address[1],
                device.info.address[2],
                device.info.address[3],
                device.info.port)
        name = device.info.properties[b'md'].decode("utf-8") \
                +" / " \
                +device.info.properties[b'fn'].decode("utf-8")
        print (ip + "\t" +name)

def connect(timeout, addr):
    print("Error: not implemented")

def main(progname, av):
    action = None
    addr = None
    timeout = None

    for i in range(len(av)):
        if av[i] == "-v" or av[i] == "--version":
            version()
            return 0
        elif av[i] == "-h" or av[i] == "--help":
            usage(progname)
            return 0
        elif action == None:
            if av[i] == "--devices":
                action = ActionType.listDevices
            elif av[i] == "--connect":
                action = ActionType.connect
            else:
                raise ValueError("Unknown operation: " +av[i])
        elif action == ActionType.connect and addr == None:
            addr = av[i]
        elif av[i][:10] == "--timeout=":
            if timeout != None:
                raise ValueError("Multiple timeout values")
            timeout = float(av[i][10:])
        else:
            stderr.write("Unknown parameter " +av[i] +"\n")
            usage(progname)
            return -1

    if action == None:
        raise ValueError("No action requested")
    elif action == ActionType.listDevices:
        listDevices(timeout if timeout != None else 5)
    elif action == ActionType.connect:
        connect((timeout if timeout != None else 5), addr)
    return 0

if __name__ == "__main__":
    try:
        if (main(argv[0], argv[1:]) == -1):
            exit(1)
    except ValueError as e:
        stderr.write("Error: " +e.args[0] +"\n")
        usage(argv[0])
        exit(1)
    exit(0)

