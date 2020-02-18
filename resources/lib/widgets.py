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
    'nextaired': {
        'name': ADDON.getLocalizedString(32059),
        'route': 'nextaired',
        'folder': True,
        'menu': [
            { 'name': ADDON.getLocalizedString(32058), 'day': 'week' },
            { 'name': xbmc.getLocalizedString(11), 'day': '0' },
            { 'name': xbmc.getLocalizedString(12), 'day': '1' },
            { 'name': xbmc.getLocalizedString(13), 'day': '2' },
            { 'name': xbmc.getLocalizedString(14), 'day': '3' },
            { 'name': xbmc.getLocalizedString(15), 'day': '4' },
            { 'name': xbmc.getLocalizedString(16), 'day': '5' },
            { 'name': xbmc.getLocalizedString(17), 'day': '6' },
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
    for i in ['discover', 'movie', 'tv', 'nextaired', 'search']:
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


# next aired
@plugin.route('/nextaired')
@plugin.route('/nextaired/<day>')
def nextaired(day=None):
    if not day:
        for i in INDEX_MENU['nextaired'].get('menu'):
            li_item = ListItem(i.get('name'))
            li_item.setArt(DEFAULT_ART)
            addDirectoryItem(plugin.handle,
                             plugin.url_for(nextaired, i.get('day')),
                             li_item, True)

        _category(category=INDEX_MENU['nextaired']['name'])

    else:
        _nextaired(day)

    endOfDirectory(plugin.handle)

def _nextaired(day):
    airing_ids = []
    airing_ids_names = {}
    next_shows, pages = _query('tv', 'on_the_air')

    if pages > 1:
        for p in range(2, pages+1):
            tmp_next_shows, tmp = _query('tv', 'on_the_air', params={'page': p})
            next_shows = next_shows + tmp_next_shows

    for item in next_shows:
        next_show_id = int(item['id'])
        airing_ids.append(next_show_id)
        airing_ids_names[next_show_id] = [item.get('name', ''), item.get('original_name', '')]

    local_ids = []
    local_media = get_local_media()

    for item in local_media['shows']:
        found_data = None

        title = item.get('title')
        originaltitle = item.get('originaltitle')
        tmdb_id = item.get('tmdbid')
        tmdb_id = item.get('tmdbid')
        imdb_id = item.get('imdbnumber')
        tvdb_id = item.get('tvdbid')

        if tmdb_id:
            if int(tmdb_id) in airing_ids:
                local_ids.append(tmdb_id)
            continue

        else:
            for i in airing_ids:
                names = airing_ids_names[i]
                if title in names or originaltitle in names:
                    if imdb_id:
                        found_data = tmdb_find(call='tv', external_id=imdb_id, error_check=False)

                    if not found_data and tvdb_id:
                        found_data = tmdb_find(call='tv', external_id=tvdb_id, error_check=False)

                    if found_data:
                        if tmdb_id[0].get('id', '') in airing_ids:
                            local_ids.append(tmdb_id[0].get('id'))

    shows = []
    for item in local_ids:
        show = _query('tv', item, get_details=True)
        if show and show.get('next_episode_to_air', {}).get('air_date'):
            next_episode = show['next_episode_to_air']
            weekday, weekday_code = date_weekday(next_episode.get('air_date'))

            if not day in [None, 'week'] and int(day) != weekday_code:
                continue

            details = {}
            details['art'] = {}
            details['art']['poster'] = IMAGEPATH + show['poster_path'] if show['poster_path'] is not None else ''
            details['art']['fanart'] = IMAGEPATH + show['backdrop_path'] if show['backdrop_path'] is not None else ''
            details['art']['thumb'] = IMAGEPATH + next_episode['still_path'] if next_episode['still_path'] is not None else ''
            details['art']['thumb'] = details['art']['thumb'] or details['art']['fanart']
            details['premiered'] = next_episode.get('air_date', '')
            details['weekday'] = weekday
            details['tvshowtitle'] = show.get('name') or show.get('original_name') or ''
            details['title'] = next_episode.get('name', xbmc.getLocalizedString(13205))
            details['season'] = str(next_episode.get('season_number', 0))
            details['episode'] = str(next_episode.get('episode_number', 0))
            details['plot'] = next_episode.get('overview', '')
            details['id'] = str(show.get('id'))

            if day in [None, 'week']:
                details['label'] = '%s: %s %sx%s. %s' % (details.get('premiered'), details.get('tvshowtitle'), details.get('season'), details.get('episode'), details.get('title'))
            else:
                details['label'] = '%s %sx%s. %s' % (details.get('tvshowtitle'), details.get('season'), details.get('episode'), details.get('title'))

            shows.append(details)

    shows = sort_dict(shows,'premiered')

    for item in shows:
        list_item = ListItem(label=item.get('label'))
        list_item.setInfo('video', {'title': item.get('title'),
                                    'tvshowtitle': item.get('tvshowtitle'),
                                    'plot': item.get('plot'),
                                    'premiered': item.get('premiered'),
                                    'season': item.get('season'),
                                    'episode': item.get('episode'),
                                    'mediatype': 'episode'}
                                    )

        list_item.setProperty('AirDay', item.get('weekday'))

        list_item.setArt({'icon': 'DefaultVideo.png'})
        list_item.setArt(item.get('art'))

        addDirectoryItem(plugin.handle, plugin.url_for(dialog, 'tv', item['id']), list_item)

    category = 0 if day == 'week' else int(day) + 1
    _category(content='videos', category=INDEX_MENU['nextaired']['menu'][category]['name'])


# discover
@plugin.route('/discover')
@plugin.route('/discover/<directory>')
@plugin.route('/discover/<directory>/<option>')
@plugin.route('/discover/<directory>/<option>/<filterby>')
@plugin.route('/discover/<directory>/<option>/<filterby>/<page>')
def discover(directory=None,option=None,filterby=None,page=1,pages=1):
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
                li_item = ListItem(i.get('name'))
                li_item.setArt(DEFAULT_ART)
                addDirectoryItem(plugin.handle,
                                 plugin.url_for(discover, directory, i.get('option')),
                                 li_item, True)

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

#helpers
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
    elif content:
        plugincontent = content
    else:
        plugincontent = ''

    set_plugincontent(content=plugincontent, category=str(category))


def _query(content_type,call,get=None,params=None,get_details=False):
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

    if not get_details:
        try:
            return tmdb.get('results'), tmdb.get('total_pages')
        except KeyError:
            return [], 1

    else:
        return tmdb


def _nextpage(page,pages):
    if int(page) < int(pages) and condition('Window.IsVisible(MyVideoNav.xml)'):
        return True
    return False


def _previouspage(page):
    if int(page) > 1 and condition('Window.IsVisible(MyVideoNav.xml) + !Container.HasParent'):
        return True
    return False