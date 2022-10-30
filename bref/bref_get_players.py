#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Create Baseball Reference json file of player statistics
"""
from common.get_raw_data import get_json_data

def bref_get_stat_url(player_type, page_no):
    """
    Get the url of the stats page referred to by the parameters

    @param {String} player_type Either "batting" or "pitching"
    @param {String} page_no Ignored
    @return {String} stat page url
    """
    if not page_no:
        return ''
    return ''.join([
        "https://www.baseball-reference.com/leagues/majors/2022-standard-",
        player_type,
        ".shtml"
    ])

def bref_fixnames(raw_roto_data):
    """
    Do nothing as a filter
    """
    return raw_roto_data

def bref_url_counter(player_type):
    """
    Keep common code happy by giving next page number after 1
    """
    if not player_type:
        return 2
    return 2

if __name__ == "__main__":
    get_json_data(
        {'get_stat_url': bref_get_stat_url,
         'url_counter': bref_url_counter,
         'fixnames': bref_fixnames,
         'table_number': 1,
         'batting_stats': ['Name', 'Tm', 'AB', 'R', 'H', 'HR', 'RBI', 'SB'],
         'pitching_stats': ['Name', 'Tm', 'W', 'SV', 'IP', 'H',
                            'ER', 'BB', 'SO'],
         'file_prefix': "baseball_reference"}
    )
