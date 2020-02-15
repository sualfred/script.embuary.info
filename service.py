#!/usr/bin/python
# coding: utf-8

########################

import xbmc

from resources.lib.helper import *

########################

class Service(xbmc.Monitor):
    def __init__(self):
        while not self.abortRequested():
            self.waitForAbort(100)

    def onNotification(self, sender, method, data):
        if method in ['VideoLibrary.OnUpdate', 'VideoLibrary.OnScanFinished', 'VideoLibrary.OnCleanFinished']:
            execute('AlarmClock(EmbuaryInfoRefreshLibraryCache,RunScript(script.embuary.info,call=refresh_library_cache),00:05,silent)')


if __name__ == "__main__":
    Service()