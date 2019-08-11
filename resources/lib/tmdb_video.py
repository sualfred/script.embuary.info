#!/usr/bin/python
# coding: utf-8

########################

import sys
import xbmc
import xbmcgui

from resources.lib.helper import *
from resources.lib.tmdb_utils import *

########################

class TMDBVideos(object):
    def __init__(self,call_request):
        self.result = {}
        self.call = call_request['call']
        self.tmdb_id = call_request['tmdb_id']
        self.local_movies = call_request['local_movies']
        self.local_shows = call_request['local_shows']
        self.movie = get_bool(self.call,'movie')
        self.tvshow = get_bool(self.call,'tv')

        if self.tmdb_id:
            self.result['details'] = self.get_details()
            self.result['cast'] = self.get_cast()
            self.result['crew'] = self.get_crew()
            self.result['similar'] = self.get_similar()
            self.result['youtube'] = self.get_yt_videos()
            self.result['images'] = self.get_images()

    def __getitem__(self, key):
        try:
            value = self.result[key]
            return value
        except KeyError:
            return

    def get_details(self):
        details = tmdb_item_details(self.call,self.tmdb_id,append_to_response='release_dates,content_ratings,external_ids,credits,videos,translations')
        self.created_by = details['created_by'] if details.get('created_by') else ''
        self.cast = details['credits']['cast']
        self.crew = details['credits']['crew']
        self.videos = details['videos']['results']
        details['crew'] = self.crew
        li = list()

        if self.movie:
            list_item = tmdb_handle_movie(details,self.local_movies,full_info=True)
        elif self.tvshow:
            list_item = tmdb_handle_tvshow(details,self.local_shows,full_info=True)

        li.append(list_item)
        return li

    def get_cast(self):
        li = list()

        for item in self.cast:
            item['label2'] = item.get('character','')
            list_item = tmdb_handle_credits(item)
            li.append(list_item)

        return li

    def get_crew(self):
        li_clean_crew = list()
        li_crew_duplicate_handler_id = list()
        li = list()

        for item in self.crew:
            if item['job'] in ['Director','Producer','Screenplay','Writer','Original Music Composer','Novel','Storyboard','Executive Producer','Comic Book']:
                if item['id'] not in li_crew_duplicate_handler_id:
                    li_clean_crew.append(item)
                    li_crew_duplicate_handler_id.append(item['id'])
                else:
                    for duplicate in li_clean_crew:
                        if duplicate['id'] == item['id']:
                            duplicate['job'] = duplicate['job'] + ' / ' + item['job']


        for item in self.created_by:
            item['label2'] = 'Creator'
            list_item = tmdb_handle_credits(item)
            li.append(list_item)

        for item in li_clean_crew:
            if item['department'] == 'Directing':
                item['label2'] = item.get('job','')
                list_item = tmdb_handle_credits(item)
                li.append(list_item)

        for item in li_clean_crew:
            if item['department'] == 'Writing':
                item['label2'] = item.get('job','')
                list_item = tmdb_handle_credits(item)
                li.append(list_item)

        for item in li_clean_crew:
            if item['department'] == 'Production':
                item['label2'] = item.get('job','')
                list_item = tmdb_handle_credits(item)
                li.append(list_item)

        for item in li_clean_crew:
            if item['department'] == 'Sound':
                item['job'] = 'Music Composer' if item['job'] == 'Original Music Composer' else item['job']
                item['label2'] = item.get('job','')
                list_item = tmdb_handle_credits(item)
                li.append(list_item)

        return li

    def get_similar(self):
        similar = tmdb_item_details(self.call,self.tmdb_id,'similar')
        similar = similar['results']
        li = list()

        if self.movie:
            similar = sort_dict(similar,'release_date',True)

            for item in similar:
                list_item = tmdb_handle_movie(item,self.local_movies)
                li.append(list_item)

        elif self.tvshow:
            similar = sort_dict(similar,'first_air_date',True)

            for item in similar:
                list_item = tmdb_handle_tvshow(item,self.local_shows)
                li.append(list_item)

        return li

    def get_images(self):
        images = tmdb_item_details(self.call,self.tmdb_id,'images',use_language=False,include_image_language='%s,en,null' % DEFAULT_LANGUAGE)
        images = images['backdrops']
        li = list()

        for item in images:
            list_item = tmdb_handle_images(item)
            li.append(list_item)

        return li

    def get_yt_videos(self):
        videos = self.videos
        li = list()

        ''' Add EN videos next to the user configured language
        '''
        if DEFAULT_LANGUAGE != FALLBACK_LANGUAGE:
            videos_en = tmdb_item_details(self.call,self.tmdb_id,'videos',use_language=False)
            videos_en = videos_en.get('results')
            videos = videos + videos_en

        for item in videos:
            if item['site'] == 'YouTube':
                list_item = tmdb_handle_yt_videos(item)
                if not list_item == 404:
                    li.append(list_item)

        return li