#!/usr/bin/python
# coding: utf-8

########################

import sys
import xbmc
import xbmcgui
import requests

from resources.lib.helper import *
from resources.lib.utils import *

########################

class TMDBSeasons(object):
    def __init__(self,call_request):
        self.result = {}
        self.call = call_request['call']
        self.tmdb_id = call_request['tmdb_id']
        self.season = call_request['season']

        if self.tmdb_id:
            cache_key = 'season' + str(self.season) + str(self.tmdb_id)
            self.details = get_cache(cache_key)

            if not self.details:
                self.details = tmdb_item_details('tv',self.tmdb_id,'season',self.season,append_to_response='credits')

            if not self.details:
                return

            if DEFAULT_LANGUAGE != FALLBACK_LANGUAGE and not self.details['overview']:
                fallback_details = tmdb_item_details('tv',self.tmdb_id,'season',self.season,use_language=False)
                self.details['overview'] = fallback_details.get('overview')

            write_cache(cache_key,self.details)

            self.tvshow_details = self.get_tvshow_details()
            self.person_duplicate_handler = list()

            self.result['details'] = self.get_details()
            self.result['cast'] = self.get_cast()
            self.result['gueststars'] = self.get_gueststars()

    def __getitem__(self, key):
        return self.result.get(key,'')

    def get_tvshow_details(self):
        tvshow_cache_key = self.call + str(self.tmdb_id)
        tvshow_details = get_cache(tvshow_cache_key)

        if not tvshow_details:
            tvshow_details = tmdb_item_details('tv',self.tmdb_id,append_to_response='release_dates,content_ratings,external_ids,credits,videos,translations')
            write_cache(tvshow_cache_key,tvshow_details)

        return tvshow_details

    def get_details(self):
        li = list()

        list_item = tmdb_handle_season(self.details,self.tvshow_details,full_info=True)
        li.append(list_item)

        return li

    def get_cast(self):
        li = list()

        for item in self.details['credits']['cast']:
            item['label2'] = item.get('character','')
            list_item = tmdb_handle_credits(item)
            li.append(list_item)
            self.person_duplicate_handler.append(item['id'])

        return li

    def get_gueststars(self):
        li = list()

        for episode in self.details['episodes']:
            for item in episode['guest_stars']:

                if item['id'] not in self.person_duplicate_handler and item['character']:
                    item['label2'] = item['character']
                    list_item = tmdb_handle_credits(item)
                    li.append(list_item)
                    self.person_duplicate_handler.append(item['id'])

        return li