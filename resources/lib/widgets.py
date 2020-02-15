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
    'movie': {
        'name': xbmc.getLocalizedString(342),
        'menu': [
            { 'name': ADDON.getLocalizedString(32049), 'call': 'discover'},
            { 'name': ADDON.getLocalizedString(32042), 'call': 'trending' },
            { 'name': ADDON.getLocalizedString(32029), 'call': 'top_rated' },
            { 'name': ADDON.getLocalizedString(32030), 'call': 'now_playing' },
            { 'name': ADDON.getLocalizedString(32031), 'call': 'upcoming' },
            { 'name': ADDON.getLocalizedString(32032), 'call': 'popular' },
        ]
    },
    'tv': {
        'name': xbmc.getLocalizedString(20343),
        'menu': [
            { 'name': ADDON.getLocalizedString(32049), 'call': 'discover' },
            { 'name': ADDON.getLocalizedString(32043), 'call': 'trending' },
            { 'name': ADDON.getLocalizedString(32033), 'call': 'top_rated' },
            { 'name': ADDON.getLocalizedString(32034), 'call': 'popular' },
            { 'name': ADDON.getLocalizedString(32035), 'call': 'airing_today' },
            { 'name': ADDON.getLocalizedString(32036), 'call': 'on_the_air' }
        ]
    }
}

DISCOVER_INDEX = {
    'movie': [
        { 'name': ADDON.getLocalizedString(32050), 'info': 'discover', 'option': 'all' },
        { 'name': ADDON.getLocalizedString(32052), 'info': 'discover', 'option': 'year', 'param': 'year' },
        { 'name': ADDON.getLocalizedString(32053), 'info': 'discover', 'option': 'genre', 'param': 'with_genres' }
    ],
    'tv': [
        { 'name': ADDON.getLocalizedString(32051), 'info': 'discover', 'option': 'all' },
        { 'name': ADDON.getLocalizedString(32054), 'info': 'discover', 'option': 'year', 'parmam': 'first_air_date_year' },
        { 'name': ADDON.getLocalizedString(32055), 'info': 'discover', 'option': 'genre', 'param': 'with_genres' }
    ]
}

########################

plugin = routing.Plugin()

# entrypoint
@plugin.route('/')
def index():
    for i in INDEX_MENU:
        addDirectoryItem(plugin.handle,
                         plugin.url_for(listing, i),
                         ListItem(INDEX_MENU[i].get('name')), True)


    search_item = ListItem(xbmc.getLocalizedString(137))
    search_item.setArt({'icon': 'DefaultMusicSearch.png'})
    addDirectoryItem(plugin.handle,
                     plugin.url_for(search),
                     search_item
                     )

    endOfDirectory(plugin.handle)


# actions
@plugin.route('/info/<call>/<tmdbid>')
def dialog(call,tmdbid):
    execute('RunScript(script.embuary.info,call=%s,tmdb_id=%s)' % (call, tmdbid))


@plugin.route('/search')
def search():
    execute('RunScript(script.embuary.info)')


# discover
@plugin.route('/<directory>/discover/<option>/<filterby>/<page>')
@plugin.route('/<directory>/discover/<option>/<filterby>')
@plugin.route('/<directory>/discover/<option>')
@plugin.route('/<directory>/discover')
def discover(directory,option=None,filterby=None,page=1,pages=1):
    category = ADDON.getLocalizedString(32050) if directory == 'movie' else ADDON.getLocalizedString(32051)

    if _previouspage(page):
        addDirectoryItem(plugin.handle,
                         plugin.url_for(discover, directory, option, filterby, int(page)-1),
                         ListItem(ADDON.getLocalizedString(32056)), True)

    if not option:
        for i in DISCOVER_INDEX[directory]:
            addDirectoryItem(plugin.handle,
                             plugin.url_for(eval(i.get('info')), directory, i.get('option')),
                             ListItem(i.get('name')), True)

        _category(category=category)

    elif option == 'all':
        result, pages = _query('discover', directory, params={'page': page})

        if result:
            _add(result, directory)

        _category(directory, category)

    elif option and not filterby:
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
        addDirectoryItem(plugin.handle,
                         plugin.url_for(discover, directory, option, filterby, int(page)+1),
                         ListItem(xbmc.getLocalizedString(33078)), True)

    endOfDirectory(plugin.handle)


# common
@plugin.route('/<directory>/<call>/<page>')
@plugin.route('/<directory>/<call>')
@plugin.route('/<directory>')
def listing(directory,call=None,page=1,pages=1):
    if _previouspage(page):
        addDirectoryItem(plugin.handle,
                         plugin.url_for(discover, directory, call, int(page)-1),
                         ListItem(ADDON.getLocalizedString(32056)), True)

    if not call:
        result = None

        for i in INDEX_MENU[directory].get('menu'):
            log(i, force=True)
            addDirectoryItem(plugin.handle,
                             plugin.url_for(listing, directory, i.get('call')),
                             ListItem(i.get('name')), True)

        _category(category=INDEX_MENU[directory]['name'])

    elif call == 'trending':
        result, pages = _query('trending', directory, 'week')

    else:
        result, pages = _query(directory, call)

    if result:
        _add(result, directory)
        _category(content=directory, call=call)

    if _nextpage(page, pages):
        addDirectoryItem(plugin.handle,
                         plugin.url_for(discover, directory, call, int(page)-1),
                         ListItem(xbmc.getLocalizedString(33078)), True)

    endOfDirectory(plugin.handle)


# helpers
def _dict_match(get,source,key,value,key2=None,value2=None):
    if not key2:
        result = [i.get(get) for i in source if i.get(key) == value]
    else:
        result = [i.get(get) for i in source if i.get(key) == value and i.get(key2) == value2]

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


def _category(content='',category='',call=None,info=None):
    if content == 'tv':
        plugincontent = 'tvshows'
    elif content == 'movie':
        plugincontent = 'movies'
    else:
        plugincontent = 'videos'

    if not category:
        category = _dict_match('name', INDEX_MENU[content]['menu'], 'call', call, 'info', content)

    set_plugincontent(content=plugincontent, category=str(category))


def _query(content_type,call,get=None,params=None):
    cache_key = 'widget' + content_type + call + str(get)
    tmdb = get_cache(cache_key)
    args = {'region': COUNTRY_CODE}
    if params:
        args.update(params)

    if not tmdb:
        tmdb = tmdb_query(action=content_type,
                          call=call,
                          get=get,
                          params=args
                          )

        if tmdb:
            write_cache(cache_key,tmdb,3)
            return tmdb.get('results'), tmdb.get('total_pages')

    return {}


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


def _nextpage(page,pages):
    if int(page) < int(pages) and condition('Window.IsVisible(MyVideoNav.xml)'):
        return True
    return False


def _previouspage(page):
    if int(page) > 1 and condition('Window.IsVisible(MyVideoNav.xml)'):
        return True
    return False