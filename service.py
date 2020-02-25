#!/usr/bin/python
# coding: utf-8

########################

import xbmc

from resources.lib.helper import *
from resources.lib.nextaired import *

########################

''' Local library is cached for 24h. This service updates the cache if the library has been changed.
    Since multiple .OnUpdate() callbacks can happen at the same time the refreshing is done by Kodi's AlarmClock function.
'''
class Service(xbmc.Monitor):
    def __init__(self):
        while not self.abortRequested():
            self.waitForAbort(100)

    def onNotification(self, sender, method, data):
        if method in ['VideoLibrary.OnUpdate', 'VideoLibrary.OnScanFinished', 'VideoLibrary.OnCleanFinished']:
            execute('AlarmClock(EmbuaryInfoRefreshLibraryCache,RunScript(script.embuary.info,call=refresh_library_cache),00:05,silent)')


if __name__ == "__main__":
    if condition('Library.HasContent(TVShows)'):
        NextAired()

    Service()