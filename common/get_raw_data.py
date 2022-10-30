#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Offseason data collector -- scrape statistics

Note: get_json_data creates the stats json file

"""
import json
import requests
import pandas as pd
from common.table_modifiers import shorten_headers, pare_frame

def _comment_filter(html_text):
    """
    Filter out comments
    """
    return html_text.replace("<!--", "").replace("--!>", "")

def _url_filter(url_text):
    """
    Use requests to get text
    """
    return _comment_filter(requests.get(url_text).text)

def _get_raw_url_data(packet):
    def _inner_raw_url_data(plyr_type):
        """
        Curry plyr_type and return link to inner function that performs a
        pandas read of the html file corresponding to the page_number passed
        to _get_url_data
        """
        def _get_url_data(page_no):
            """
            Read the html file for the page number specified.
            Return the first table found in the DataFrame.
            """
            return pd.read_html(_url_filter(packet['get_stat_url'](
                                plyr_type,
                                str(page_no))))[packet['table_number']]
        return _get_url_data
    return _inner_raw_url_data

def get_raw_data(packet):
    """
    Curry packet
    """
    def _inner_raw_data(plyr_type):
        """
        Use map to call _get_url_data (inner class with curried
        plyr_type parameter

        @param {String} plyr_type Either "batting" or "pitching"
        @return {list} DataFrames containing statistics
        """
        return list(map(_get_raw_url_data(packet)(plyr_type),
               list(range(1, packet['url_counter'](plyr_type)))))
    return _inner_raw_data

def get_ptype_stats(packet):
    """
    Curry packet
    """
    def _inner_stats(ptype):
        """
        Get statistics with shortened column names

        @param {String} ptype Either "batting" or "pitching"
        @return {list} Dataframes containing stats with shortened
                       column names
        """
        return shorten_headers(pd.concat(get_raw_data(packet)(ptype),
                                         ignore_index=True))
    return _inner_stats

def get_full_stat_records(packet):
    """
    Get statistics

    @return {list} a two item list -- batting and pitching DataFrames
    """
    return list(map(get_ptype_stats(packet), ["batting", "pitching"]))

def roto_details(stats, packet):
    """
    Clean up rotisserie stats

    @param {list} two full DataFrame (batting and pitching)
    @return {list} two rotisserie stat DataFrames (batting and pitching)
    """
    return [
        pare_frame(stats[0], packet["batting_stats"]),
        pare_frame(stats[1], packet["pitching_stats"])
    ]

def get_roto_stats(packet):
    """
    Get statistics for rotisserie league

    @return {list} list of two pandas dataframes (batting and pitching)
    """
    return roto_details(get_full_stat_records(packet), packet)

def _conv_to_dict(dataframe):
    """
    Map routine to convert data frame to dict
    """
    return dataframe.to_dict('records')

def get_raw_roto_dict(packet):
    """
    Get dict of statistics for rotisserie league

    @return {list} two lists (batter and pitcher) of individual data as
                   dictionary records
    """
    return list(map(_conv_to_dict, get_roto_stats(packet)))

def get_all_data(packet):
    """
    Get dict of statistics for rotisserie league (wrapper of get_raw_roto
    dict that fixes names, team, and position data).

    @return {list} two lists (batter and pitcher) of individual data as
                   dictionary records
    """
    return list(map(packet['fixnames'], get_raw_roto_dict(packet)))

def get_json_data(packet):
    """
    Initialize json
    """
    with open('.'.join([packet["file_prefix"], "stats.json"]),
              "w", encoding="utf8") as ofd:
        json.dump(get_all_data(packet), ofd)
