#!/usr/bin/python
# coding: utf-8

########################

import sys
import xbmc
import xbmcgui
import requests

from resources.lib.helper import *
from resources.lib.tmdb import *
from resources.lib.season import *

########################

class TMDBEpisodes(TMDBSeasons):
    def __init__(self,call_request):
        self.episode = call_request['episode']
        super().__init__(call_request)

        self.result['thumb']= self.result.pop('posters')
        self.result['crew'] = self.get_crew()


    def get_details(self):
        li = list()
        episode_data = dict()
        try:
            for episode in self.details['episodes']:
                if episode.get('episode_number') == int(self.episode):
                    episode_data = episode
                    break

            self.details['name'] = episode_data.get('name') or self.details['name']
            self.details['air_date'] = episode_data.get('air_date') or self.details['air_date']
            self.details['overview'] = episode_data.get('overview') or self.details['overview']
            self.details['poster_path'] = episode_data.get('still_path') or self.details['poster_path']
            self.details['TotalEpisodes'] = len(self.details.get('episodes'))
            self.details['episode_number'] = episode_data.get('episode_number')
            self.details['vote_average'] = episode_data.get('vote_average')
            self.details['vote_count'] = episode_data.get('vote_count')
            self.crew = episode_data.get('crew') if episode_data.get('crew') else ''

            self.details.pop('episodes')
        except: pass

        list_item = tmdb_handle_episode(self.details,self.tvshow_details,full_info=True)
        li.append(list_item)

        return li

    def get_gueststars(self):
        li = list()

        try:
            episode_data = dict()
            for episode in self.details['episodes']:
                if episode.get('episode_number') == int(self.episode):
                    episode_data = episode
                    break
            for item in episode_data['guest_stars']:
                if item['character']:
                    item['label2'] = item['character']
                    list_item = tmdb_handle_credits(item)
                    li.append(list_item)
        except: pass

        return li

    def get_images(self):
        cache_key = 'images_%s_season_%s_episode_%s' %(self.tmdb_id, self.season, self.episode)
        images = get_cache(cache_key)
        li = list()

        if not images:
            images = tmdb_query(action='tv',
                                call=self.tmdb_id,
                                get='season/%s' % self.season,
                                get2='episode/%s' % self.episode,
                                get3='images',
                                params={'include_image_language': '%s,en,null' % DEFAULT_LANGUAGE}
                                )
            write_cache(cache_key,images)

        for item in images['stills']:
            list_item = tmdb_handle_images(item)
            li.append(list_item)

        return li

    def get_crew(self):
        li_clean_crew = list()
        li_crew_duplicate_handler_id = list()
        li = list()

        ''' Filter crew and merge duplicate crew members if they were responsible for different jobs
        '''
        for item in self.crew:
            if item['job'] in ['Creator', 'Director', 'Producer', 'Screenplay', 'Writer', 'Original Music Composer', 'Novel', 'Storyboard', 'Executive Producer', 'Comic Book']:
                if item['id'] not in li_crew_duplicate_handler_id:
                    li_clean_crew.append(item)
                    li_crew_duplicate_handler_id.append(item['id'])
                else:
                    for duplicate in li_clean_crew:
                        if duplicate['id'] == item['id']:
                            duplicate['job'] = duplicate['job'] + ' / ' + item['job']

        ''' Sort crew output based on department
        '''
        for item in li_clean_crew:
            if item['department'] == 'Directing':
                item['label2'] = item.get('job', '')
                list_item = tmdb_handle_credits(item)
                li.append(list_item)

        for item in li_clean_crew:
            if item['department'] == 'Writing':
                item['label2'] = item.get('job', '')
                list_item = tmdb_handle_credits(item)
                li.append(list_item)

        for item in li_clean_crew:
            if item['department'] == 'Production':
                item['label2'] = item.get('job', '')
                list_item = tmdb_handle_credits(item)
                li.append(list_item)

        for item in li_clean_crew:
            if item['department'] == 'Sound':
                item['job'] = 'Music Composer' if item['job'] == 'Original Music Composer' else item['job']
                item['label2'] = item.get('job', '')
                list_item = tmdb_handle_credits(item)
                li.append(list_item)

        return li
