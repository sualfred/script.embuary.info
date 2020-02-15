#!/usr/bin/python
# coding: utf-8

########################

import xbmc

from resources.lib.helper import *
from resources.lib.utils import *

########################

class Service(xbmc.Monitor):
    def __init__(self):
        while not self.abortRequested():
            self.waitForAbort(100)

    def onNotification(self, sender, method, data):
        if method in ['VideoLibrary.OnUpdate', 'VideoLibrary.OnScanFinished', 'VideoLibrary.OnCleanFinished']:
            get_local_media(force=True)


if __name__ == "__main__":
    Service()