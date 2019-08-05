#!/usr/bin/python
# coding: utf-8

########################

import xbmc
import xbmcaddon
import xbmcgui
import json
import time
import datetime
import os
import operator

########################

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path').decode('utf-8')

NOTICE = xbmc.LOGNOTICE
WARNING = xbmc.LOGWARNING
DEBUG = xbmc.LOGDEBUG

DIALOG = xbmcgui.Dialog()

########################

def log(txt,loglevel=NOTICE,force=False):
    ''' Python 2 requires to decode stuff at first
    '''
    try:
        if isinstance(txt, str):
            txt = txt.decode('utf-8')
    except AttributeError:
        pass

    message = u'[ %s ] %s' % (ADDON_ID,txt)

    try:
        xbmc.log(msg=message.encode('utf-8'), level=loglevel) # Python 2
    except TypeError:
        xbmc.log(msg=message, level=loglevel)


def sort_dict(item,by,reverse=False):
    try:
        return sorted(item, key=operator.itemgetter(by), reverse=reverse)
    except KeyError:
        return item


def remove_quotes(label):
    if not label:
        return ''

    if label.startswith("'") and label.endswith("'") and len(label) > 2:
        label = label[1:-1]
        if label.startswith('"') and label.endswith('"') and len(label) > 2:
            label = label[1:-1]

    return label


def get_date(date_time):
    date_time_obj = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    date_obj = date_time_obj.date()

    return date_obj


def execute(cmd):
    xbmc.executebuiltin(cmd, DEBUG)


def visible(condition):
    return xbmc.getCondVisibility(condition)


def busydialog(close=False):
    if not close and not visible('Window.IsVisible(busydialognocancel)'):
        execute('ActivateWindow(busydialognocancel)')
    elif close:
        execute('Dialog.Close(busydialognocancel)')


def winprop(key, value=None, clear=False, window_id=10000):
    window = xbmcgui.Window(window_id)

    if clear:
        window.clearProperty(key.replace('.json', '').replace('.bool', ''))

    elif value is not None:

        if key.endswith('.json'):
            key = key.replace('.json', '')
            value = json.dumps(value)

        elif key.endswith('.bool'):
            key = key.replace('.bool', '')
            value = 'true' if value else 'false'

        window.setProperty(key, value)

    else:
        result = window.getProperty(key.replace('.json', '').replace('.bool', ''))

        if result:
            if key.endswith('.json'):
                result = json.loads(result)
            elif key.endswith('.bool'):
                result = result in ('true', '1')

        return result


def get_bool(value,string='true'):
    try:
        if value.lower() == string:
            return True
        raise Exception

    except Exception:
        return False


def get_joined_items(item):
    if len(item) > 0:
        item = ' / '.join(item)
    else:
        item = ''
    return item


def get_first_item(item):
    if len(item) > 0:
        item = item[0]
    else:
        item = ''

    return item


def json_call(method,properties=None,sort=None,query_filter=None,limit=None,params=None,item=None,options=None,limits=None):
    json_string = {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': {}}

    if properties is not None:
        json_string['params']['properties'] = properties

    if limit is not None:
        json_string['params']['limits'] = {'start': 0, 'end': int(limit)}

    if sort is not None:
        json_string['params']['sort'] = sort

    if query_filter is not None:
        json_string['params']['filter'] = query_filter

    if options is not None:
        json_string['params']['options'] = options

    if limits is not None:
        json_string['params']['limits'] = limits

    if item is not None:
        json_string['params']['item'] = item

    if params is not None:
        json_string['params'].update(params)

    json_string = json.dumps(json_string)

    result = xbmc.executeJSONRPC(json_string)

    ''' Python 2 compatibility
    '''
    try:
        result = unicode(result, 'utf-8', errors='ignore')
    except NameError:
        pass

    return json.loads(result)