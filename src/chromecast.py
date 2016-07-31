from zeroconf import ServiceBrowser, Zeroconf

class ChromecastReceiver(object):
    def __init__(self, name, info):
        print(info)
        self.name = name
        self.info = info

""" Chromecast API v2 """
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

