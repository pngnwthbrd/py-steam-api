import sys
import requests
import logging
import json
from pysteamapi import constants
from pysteamapi.config import cfg

class Steam:
    __vanityurl = None
    __steamid = None
    _uri_get_friendslist = {
        'url': 'http://api.steampowered.com/ISteamUser' \
                '/GetFriendList/v0001/',
        'params': {
            'key': constants.STEAM_API_KEY,
            'steamid': None, # get from config or arguments
            'relationship': 'friend'
        }
    }
    _uri_get__steamid = {
        'url': 'http://api.steampowered.com/ISteamUser' \
                '/ResolveVanityURL/v0001/',
        'params': {
            'key': constants.STEAM_API_KEY,
            'vanityurl': None, # get from config or arguments
        }
    }
    _uri_get_wishlist = {
        'url': 'https://store.steampowered.com/wishlist' \
                '/profiles/{steamid}/wishlistdata'
    }
    _uri_get_profile_summary = {
        'url': 'http://api.steampowered.com/ISteamUser' \
                '/GetPlayerSummaries/v0002/',
        'params': {
            'key': constants.STEAM_API_KEY,
            'steamids': None # get from argument
        }
    }

    def __init__(self, steamid = None, vanityurl = None):
        error = 0
        if cfg['steam']['steamid'] is None and cfg['steam']['vanityurl'] is None:
            error += 1
        else:
            self.__vanityurl = cfg['steam']['vanityurl']
            self.__steamid = cfg['steam']['steamid']

        if steamid is None and vanityurl is None:
            error +-1
        else:
            self.__vanityurl = vanityurl
            self.__steamid = steamid

        if error >= 2:
            print('steamid and vanityurl unknown' \
                        ' - One of both must be assigned')

            sys.exit()

        self._vanityurl_to_steamid()


    def get_friendslist(self):
        # manipulate params
        self._uri_get_friendslist['params']['steamid'] = self.__steamid
        # get friends list as json response
        r = requests.get(self._uri_get_friendslist['url'],
                         self._uri_get_friendslist['params'])

        friendslist = json.JSONDecoder().decode(r.text)

        return friendslist['friendslist']

    def get_wishlist(self):
        # get wishlist json response
        r = requests.get(self._uri_get_wishlist['url']
                                .replace('{steamid}', str(self.__steamid)))

        wishlist = json.JSONDecoder().decode(r.text)

        return wishlist

    # @param steamids can be comma delimited
    def get_profile_summary(self, steamids):
        # manipulate params
        self._uri_get_profile_summary['params']['steamids'] = steamids
        # get profile summary json response
        r = requests.get(self._uri_get_profile_summary['url'],
                         self._uri_get_profile_summary['params'])

        profile_summary = json.JSONDecoder().decode(r.text)

        return profile_summary['response']['players']

    def _vanityurl_to_steamid(self):
        # get steamid from vanityurl if vanityurl is set
        if self.__vanityurl is not None:
            self.__steamid = self._get_steamid_by_vanityurl()

    def _get_steamid_by_vanityurl(self):
        # TODO: check the None case
        if self.__vanityurl is None:
            pass

        # manipulate params
        self._uri_get__steamid['params']['vanityurl'] = self.__vanityurl
        # get steamid json response
        r = requests.get(self._uri_get__steamid['url'],
                         self._uri_get__steamid['params'])

        steamid = json.JSONDecoder().decode(r.text)

        return steamid['response']['steamid']

    @property
    def steamid(self):
        return self.__steamid

    @steamid.setter
    def steamid(self, steamid):
        self.__steamid = steamid

    @property
    def vanityurl(self):
        return self.__vanityurl

    @vanityurl.setter
    def vanityurl(self, vanityurl):
        self.__vanityurl = vanityurl
        # update current steamid
        self._vanityurl_to_steamid()
