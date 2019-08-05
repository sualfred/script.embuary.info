#!/usr/bin/python

########################

import xbmcgui

from resources.lib.helper import *
from resources.lib.tmdb_main import *

########################

class Main:

    def __init__(self):
        self.call = False
        self._parse_argv()

        if self.call:
            TheMovieDB(self.call,self.params)
        else:
            DIALOG.ok(ADDON.getLocalizedString(32000), ADDON.getLocalizedString(32001))


    def _parse_argv(self):
        args = sys.argv

        for arg in args:
            if arg == ADDON_ID:
                continue
            if arg.startswith('call='):
                self.call = arg[5:].lower()
            else:
                try:
                    self.params[arg.split("=")[0].lower()] = "=".join(arg.split("=")[1:]).strip()
                except:
                    self.params = {}
                    pass


if __name__ == "__main__":
    Main()
