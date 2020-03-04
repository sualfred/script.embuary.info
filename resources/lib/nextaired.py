#!/usr/bin/python
# coding: utf-8

########################

import requests

from resources.lib.helper import *
from resources.lib.tvdb import *
from resources.lib.trakt import *
from resources.lib.localdb import *

########################

class NextAired():
    def __init__(self):
        self.date_today = str(datetime.date.today())

        local_media = get_local_media()
        self.local_media = local_media['shows']

        cache_key = 'nextaired_' + self.date_today + '_' + md5hash(self.local_media)
        self.airing_items = get_cache(cache_key)

        if not self.airing_items:
            airing_items = {}
            airing_items['week'] = []
            airing_items['0'] = []
            airing_items['1'] = []
            airing_items['2'] = []
            airing_items['3'] = []
            airing_items['4'] = []
            airing_items['5'] = []
            airing_items['6'] = []

            self.airing_items = airing_items
            self.getdata()

        if self.airing_items:
            write_cache(cache_key, self.airing_items, 24)

    def get(self,day=None):
        if day is not None and day in self.airing_items:
            return self.airing_items[day]
        else:
            return self.airing_items['week']

    def getdata(self):
        if not self.local_media:
            return

        local_media_data = []
        for item in self.local_media:
            local_media_data.append([item.get('tmdbid'), item.get('tvdbid'), item.get('imdbnumber'), item.get('art'), item.get('title'), item.get('originaltitle'), item.get('year')])

        tvdb_api = TVDB_API()
        trakt_results = trakt_api('/calendars/all/shows/' + self.date_today + '/7?countries=' + COUNTRY_CODE.lower() + '%2Cus')

        if trakt_results:
            for item in trakt_results:
                show = item.get('show', {})
                episode = item.get('episode', {})

                airing_date, airing_time = utc_to_local(item.get('first_aired'))
                weekday, weekday_code = date_weekday(airing_date)

                tmp = {}
                tmp['show'] = show.get('title')
                tmp['year'] = show.get('year')
                tmp['show_tmdbid'] = show.get('ids', {}).get('tmdb')
                tmp['show_tvdbid'] = show.get('ids', {}).get('tvdb')
                tmp['show_imdbid'] = show.get('ids', {}).get('imdb')
                tmp['episode_tvdbid'] = episode.get('ids', {}).get('tvdb')

                for i in local_media_data:
                    if str(tmp['show_tmdbid']) == i[0] or str(tmp['show_tvdbid']) == i[1] or str(tmp['show_imdbid']) == i[2] or (tmp['show'] in [i[4], i[5]] and tmp['year'] == i[6]):
                        tvdb_query = tvdb_api.call('/episodes/' + str(tmp['episode_tvdbid']))

                        if tvdb_query and not tvdb_query['overview'] and COUNTRY_CODE != 'US':
                            tvdb_query = tvdb_api.call('/episodes/' + str(tmp['episode_tvdbid']), lang='us')

                        if tvdb_query:
                            tvdb_query['localart'] = i[3]
                            tvdb_query['showtitle'] = i[4] or i[5]
                            tvdb_query['airing'] = airing_date
                            tvdb_query['airing_time'] = airing_time
                            tvdb_query['weekday'] = weekday
                            tvdb_query['weekday_code'] = weekday_code

                            self.airing_items['week'].append(tvdb_query)
                            self.airing_items[str(weekday_code)].append(tvdb_query)

                        break