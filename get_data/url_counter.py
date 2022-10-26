#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Offseason data collector -- find maximum number for url stat pages
"""
from bs4 import BeautifulSoup
import requests

def get_stat_url(player_type, page_no):
    """
    Get the url of the stats page referred to by the parameters

    @param {String} player_type Either "batting" or "pitching"
    @param {String} page_no Page number passed after equal sign in URL
    @return {String} stat page url
    """
    return ''.join([
        "https://www.cbssports.com/mlb/stats/player/",
        player_type,
        "/mlb/regular/all-pos/all/?page=",
        page_no
    ])

def url_counter(player_type):
    """
    Find number of pages for this player type (returns the number one value
    beyond the last valid page which would be the right number to use for
    range function calls with ranges starting at 1).

    @param {String} player_type Either "batting" or "pitching"
    @return {Integer} first invalid page number found sequentially
    """
    return _get_set_of_urls(get_stat_url(player_type, ''), 1)

def _get_set_of_urls(url_pattern, page_no):
    """
    Recursively search for a page that does not have a table
    """
    if _has_no_table(f'{url_pattern}{page_no}'):
        return page_no
    return _get_set_of_urls(url_pattern, page_no + 1)

def _has_no_table(url_name):
    """
    Return true if no tables can be found in this url
    """
    if ''.join(BeautifulSoup(requests.get(url_name).text,
            "html.parser").findAll(text=True)).find('Sorry, no results') > 0:
        return True
    return False
