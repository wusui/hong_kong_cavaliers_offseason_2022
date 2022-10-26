#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Offseason data collector -- scrape statistics

Note: get_json_data creates the stats.json file

"""
import json
import pandas as pd
from url_counter import url_counter, get_stat_url
from table_modifiers import shorten_headers, pare_frame
from player_modifiers import fixnames

def _get_raw_url_data(plyr_type):
    """
    Curry plyr_type and return link to inner function that performs a
    pandas read of the html file corresponding to the page_number passed
    to _get_url_data
    """
    def _get_url_data(page_no):
        """
        Read the html file for the page number specified.  Return the first
        table found in the DataFrame.
        """
        return pd.read_html(get_stat_url(plyr_type, str(page_no)))[0]
    return _get_url_data

def get_raw_data(plyr_type):
    """
    Use map to call _get_url_data (inner class with curried plyr_type parameter

    @param {String} plyr_type Either "batting" or "pitching"
    @return {list} DataFrames containing statistics
    """
    return list(map(_get_raw_url_data(plyr_type),
               list(range(1, url_counter(plyr_type)))))

def get_ptype_stats(ptype):
    """
    Get statistics with shortened column names

    @param {String} ptype Either "batting" or "pitching"
    @return {list} Dataframes containing stats with shortened column names
    """
    return shorten_headers(pd.concat(get_raw_data(ptype), ignore_index=True))

def get_full_stat_records():
    """
    Get statistics

    @return {list} a two item list -- batting and pitching DataFrames
    """
    return list(map(get_ptype_stats, ["batting", "pitching"]))

def roto_details(stats):
    """
    Clean up rotisserie stats

    @param {list} two full DataFrame (batting and pitching)
    @return {list} two rotisserie stat DataFrames (batting and pitching)
    """
    return [
        pare_frame(stats[0],
                   ['Player', 'AB', 'R', 'H', 'HR', 'RBI', 'SB']),
        pare_frame(stats[1],
                   ['Player', 'IP', 'W', 'SV', 'H', 'ER', 'BB', 'SO'])
    ]

def get_roto_stats():
    """
    Get statistics for rotisserie league

    @return {list} list of two pandas dataframes (batting and pitching)
    """
    return roto_details(get_full_stat_records())

def _conv_to_dict(dataframe):
    """
    Map routine to convert data frame to dict
    """
    return dataframe.to_dict('records')

def get_raw_roto_dict():
    """
    Get dict of statistics for rotisserie league

    @return {list} two lists (batter and pitcher) of individual data as
                   dictionary records
    """
    return list(map(_conv_to_dict, get_roto_stats()))

def get_all_data():
    """
    Get dict of statistics for rotisserie league (wrapper of get_raw_roto_dict
    that fixes names, team, and position data).

    @return {list} two lists (batter and pitcher) of individual data as
                   dictionary records
    """
    return list(map(fixnames, get_raw_roto_dict()))

def get_json_data():
    """
    Initialize stats.json
    """
    with open("stats.json", "w", encoding="utf8") as OFD:
        json.dump(get_all_data(), OFD)
