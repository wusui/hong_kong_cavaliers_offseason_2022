#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Offseason data collector -- shorten header
"""
from functools import reduce

def fix_column_head(oldh, field):
    """
    Add to list consisting of (old_long_entry, short_entry) tuples.
    When this is made a dict, format is right for a dataFrame rename
    parameter.

    @param {list} oldh Previous header information
    @return {list} list of tuples usable by dataFrame rename call
    """
    return oldh + [(field, field.split(' ')[0])]

def shorten_headers(dframe):
    """
    Shorten column headings to first word in heading.

    @param dframe {DataFrame} pandas dataFrame with long headers
    @return {DataFrame} DataFrame with headers reduced
    """
    return dframe.rename(
        columns=dict(reduce(fix_column_head,
                            dframe.columns.tolist(), []))
    )

def _keep_stats(keepers):
    """
    Curry keeper list and use _drop_stats to find stats to remove
    """
    def _drop_stats(each_stat):
        """
        True if stat is not in keeper list
        """
        return each_stat not in keepers
    return _drop_stats

def pare_stats(dframe, keep_list):
    """
    Get list of column headings to drop

    @param dframe {DataFrame} pandas dataframe with extra columns
    @param keep_list {list} column stats that we will keep
    @return list of column stats that we will drop
    """
    return list(filter(_keep_stats(keep_list), dframe.columns.tolist()))

def pare_frame(dframe, keep_list):
    """
    Return a DataFrame with columns not in the keeper list removed

    @param dframe {DataFrame} pandas dataframe with extra columns
    @param keep_list {list} column stats that we will keep
    @return new dataFrame with some columns removed
    """
    return dframe.drop(pare_stats(dframe, keep_list), axis=1)
