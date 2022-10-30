#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Create CBS json file of player statistics
"""
from cbs.cbs_url_counter import cbs_url_counter, cbs_get_stat_url
from cbs.cbs_player_modifiers import cbs_fixnames
from common.get_raw_data import get_json_data

if __name__ == "__main__":
    get_json_data(
        {'get_stat_url': cbs_get_stat_url,
         'url_counter': cbs_url_counter,
         'fixnames': cbs_fixnames,
         'table_number': 0,
         'batting_stats': ['Player', 'AB', 'R', 'H', 'HR', 'RBI', 'SB'],
         'pitching_stats': ['Player', 'IP', 'W', 'SV', 'H', 'ER', 'BB', 'SO'],
         'file_prefix': "cbs"}
    )
