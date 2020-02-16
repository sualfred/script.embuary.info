#!/usr/bin/python
# coding: utf-8

########################

import routing
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory
from datetime import date

from resources.lib.helper import *
from resources.lib.utils import *

########################

INDEX_MENU = {
    'discover': {
        'name': ADDON.getLocalizedString(32049),
        'route': 'discover',
        'folder': True,
        'menu': [
            { 'name': ADDON.getLocalizedString(32050), 'call': 'movie'},
            { 'name': ADDON.getLocalizedString(32051), 'call': 'tv' },
            { 'name': ADDON.getLocalizedString(32057), 'call': 'person' }
        ]
    },
    'movie': {
        'name': xbmc.getLocalizedString(342),
        'route': 'movie_listing',
        'folder': True,
        'menu': [
            { 'name': ADDON.getLocalizedString(32042), 'call': 'trending' },
            { 'name': ADDON.getLocalizedString(32029), 'call': 'top_rated' },
            { 'name': ADDON.getLocalizedString(32030), 'call': 'now_playing' },
            { 'name': ADDON.getLocalizedString(32031), 'call': 'upcoming' },
            { 'name': ADDON.getLocalizedString(32032), 'call': 'popular' },
        ]
    },
    'tv': {
        'name': xbmc.getLocalizedString(20343),
        'route': 'tv_listing',
        'folder': True,
        'menu': [
            { 'name': ADDON.getLocalizedString(32043), 'call': 'trending' },
            { 'name': ADDON.getLocalizedString(32033), 'call': 'top_rated' },
            { 'name': ADDON.getLocalizedString(32034), 'call': 'popular' },
            { 'name': ADDON.getLocalizedString(32035), 'call': 'airing_today' },
            { 'name': ADDON.getLocalizedString(32036), 'call': 'on_the_air' }
        ]
    },
    'search': {
        'name': xbmc.getLocalizedString(137),
        'route': 'search',
        'folder': False
    }
}

DISCOVER_INDEX = {
    'movie': [
        { 'name': ADDON.getLocalizedString(32050), 'option': 'all' },
        { 'name': ADDON.getLocalizedString(32052), 'option': 'year', 'param': 'year' },
        { 'name': ADDON.getLocalizedString(32053), 'option': 'genre', 'param': 'with_genres' },
    ],
    'tv': [
        { 'name': ADDON.getLocalizedString(32051), 'option': 'all' },
        { 'name': ADDON.getLocalizedString(32054), 'option': 'year', 'parmam': 'first_air_date_year' },
        { 'name': ADDON.getLocalizedString(32055), 'option': 'genre', 'param': 'with_genres' }
    ]
}

DEFAULT_ART = {
    'icon': 'DefaultFolder.png',
    'thumb': 'special://home/addons/script.embuary.info/resources/icon.png'
}

########################

plugin = routing.Plugin()

# entrypoint
@plugin.route('/')
def index():
    for i in ['discover', 'movie', 'tv', 'search']:
        item =  INDEX_MENU[i]
        li_item = ListItem(item['name'])
        li_item.setArt(DEFAULT_ART)
        addDirectoryItem(plugin.handle,
                         plugin.url_for(eval(item['route'])),
                         li_item, item['folder'])

    endOfDirectory(plugin.handle)


# actions
@plugin.route('/info/<call>/<tmdbid>')
def dialog(call,tmdbid):
    execute('RunScript(script.embuary.info,call=%s,tmdb_id=%s)' % (call, tmdbid))


@plugin.route('/search')
def search():
    execute('RunScript(script.embuary.info)')


# discover
@plugin.route('/discover')
@plugin.route('/discover/<directory>')
@plugin.route('/discover/<directory>/<option>')
@plugin.route('/discover/<directory>/<option>/<filterby>')
@plugin.route('/discover/<directory>/<option>/<filterby>/<page>')
def discover(directory=None,option='-',filterby='-',page=1,pages=1):
    if not directory:
        for i in INDEX_MENU['discover'].get('menu'):
            li_item = ListItem(i.get('name'))
            li_item.setArt(DEFAULT_ART)
            addDirectoryItem(plugin.handle,
                             plugin.url_for(discover, i.get('call')),
                             li_item, True)

        _category(category=INDEX_MENU['discover']['name'])

    else:
        category = _dict_match('name', INDEX_MENU['discover']['menu'], 'call', directory)

        if _previouspage(page):
            li_item = ListItem(ADDON.getLocalizedString(32056))
            li_item.setArt(DEFAULT_ART)
            addDirectoryItem(plugin.handle,
                             plugin.url_for(discover, directory, option, filterby, int(page)-1),
                             li_item, True)

        if directory == 'person':
            result, pages = _query('person', 'popular', params={'page': page})

            if result:
                _add(result, 'person')

            _category(directory, category)

        elif not option:
            for i in DISCOVER_INDEX[directory]:
                addDirectoryItem(plugin.handle,
                                 plugin.url_for(discover, directory, i.get('option')),
                                 ListItem(i.get('name')), True)

            _category(category=category)

        elif option == 'all':
            result, pages = _query('discover', directory, params={'page': page})

            if result:
                _add(result, directory)

            _category(directory, category)

        elif option in ['genre', 'year'] and not filterby:
            option_results, filter_value, icon = _discover_option(directory, option)

            for i in option_results:
                li_item = ListItem(i.get('name'))
                li_item.setArt({'icon': icon})

                addDirectoryItem(plugin.handle,
                                 plugin.url_for(discover, directory, option, i.get(filter_value)),
                                 li_item, True)

            _category(directory, category)

        else:
            filter_param = _dict_match('param', DISCOVER_INDEX[directory], 'option', option)
            result, pages = _query('discover', directory, params={filter_param: filterby, 'page': page})

            if result:
                _add(result, directory)

            _category(directory, category + ' (' + filterby + ')')

        if _nextpage(page, pages):
            li_item = ListItem(xbmc.getLocalizedString(33078))
            li_item.setArt(DEFAULT_ART)
            addDirectoryItem(plugin.handle,
                             plugin.url_for(discover, directory, option, filterby, int(page)+1),
                             li_item, True)

    endOfDirectory(plugin.handle)


def _discover_option(call,option):
    if option == 'genre':
        tmdb = tmdb_query(action='genre',
                          call=call,
                          get='list'
                          )

        return tmdb['genres'], 'id', 'DefaultGenre.png'

    elif option == 'year':
        cur_year = date.today().year
        index = cur_year
        years = []

        for i in range(cur_year - 1900 + 1):
            years.append({'name': str(index)})
            index -= 1

        return years, 'name', 'DefaultYear.png'

    elif option == 'keyword':
        keyboard = xbmc.Keyboard()
        keyboard.doModal()

        if keyboard.isConfirmed():
            return keyboard.getText(),


# common
@plugin.route('/movie')
@plugin.route('/movie/<call>')
@plugin.route('/movie/<call>/<page>')
def movie_listing(call=None,page=1,pages=1):
    _listing('movie', call, page, pages)

@plugin.route('/tv')
@plugin.route('/tv/<call>')
@plugin.route('/tv/<call>/<page>')
def tv_listing(call=None,page=1,pages=1):
    _listing('tv', call, page, pages)

def _listing(directory, call, page, pages):
    route = '%s_listing' % directory
    category = _dict_match('name', INDEX_MENU[directory]['menu'], 'call', call)

    if _previouspage(page):
        li_item = ListItem(ADDON.getLocalizedString(32056))
        li_item.setArt(DEFAULT_ART)
        addDirectoryItem(plugin.handle,
                         plugin.url_for(eval(route), call, int(page)-1),
                         li_item, True)

    if not call:
        result = None
        for i in INDEX_MENU[directory].get('menu'):
            li_item = ListItem(i.get('name'))
            li_item.setArt(DEFAULT_ART)
            addDirectoryItem(plugin.handle,
                             plugin.url_for(eval(route), i.get('call')),
                             li_item, True)

        _category(category=INDEX_MENU[directory]['name'])

    elif call == 'trending':
        result, pages = _query('trending', directory, 'week', params={'page': page})

    else:
        result, pages = _query(directory, call, params={'page': page})

    if result:
        _add(result, directory)
        _category(directory, category)

    if _nextpage(page, pages):
        li_item = ListItem(xbmc.getLocalizedString(33078))
        li_item.setArt(DEFAULT_ART)
        addDirectoryItem(plugin.handle,
                         plugin.url_for(eval(route), call, int(page)+1),
                         li_item, True)

    endOfDirectory(plugin.handle)

# helpers
def _dict_match(get,source,key,value):
    result = [i.get(get) for i in source if i.get(key) == value]
    if result:
        return result[0]


def _add(items,call):
    local_items = get_local_media()

    if call == 'tv':
        for item in items:
            list_item, is_local = tmdb_handle_tvshow(item, local_items=local_items.get('shows', []), mediatype='video')
            addDirectoryItem(plugin.handle, plugin.url_for(dialog, 'tv', item['id']), list_item)

    elif call == 'movie':
        for item in items:
            list_item, is_local = tmdb_handle_movie(item, local_items=local_items.get('movies', []), mediatype='video')
            addDirectoryItem(plugin.handle, plugin.url_for(dialog, 'movie', item['id']), list_item)

    elif call == 'person':
        for item in items:
            list_item = tmdb_handle_person(item)
            addDirectoryItem(plugin.handle, plugin.url_for(dialog, 'person', item['id']), list_item)


def _category(content='',category='',call=None,info=None):
    if content == 'tv':
        plugincontent = 'tvshows'
    elif content == 'movie':
        plugincontent = 'movies'
    elif content == 'person':
        plugincontent = 'actors'
    else:
        plugincontent = ''

    set_plugincontent(content=plugincontent, category=str(category))


def _query(content_type,call,get=None,params=None):
    args = {'region': COUNTRY_CODE}
    if params:
        args.update(params)

    cache_key = 'widget' + content_type + call + str(get) + str(args)
    tmdb = get_cache(cache_key)

    if not tmdb:
        tmdb = tmdb_query(action=content_type,
                          call=call,
                          get=get,
                          params=args
                          )

    if tmdb:
        write_cache(cache_key,tmdb,3)
        return tmdb.get('results'), tmdb.get('total_pages')

    return {}, 1


def _nextpage(page,pages):
    if int(page) < int(pages) and condition('Window.IsVisible(MyVideoNav.xml)'):
        return True
    return False


def _previouspage(page):
    if int(page) > 1 and condition('Window.IsVisible(MyVideoNav.xml) + !Container.HasParent'):
        return True
    return False