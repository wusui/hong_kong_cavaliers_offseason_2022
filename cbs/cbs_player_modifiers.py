#!/usr/bin/python
# Copyright (c) 2022 Warren Usui
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Offseason data collector -- Fix records to have name/pos/team correct
"""

def fix_dict_rec(record, field, conv_func):
    """
    Operation to work on one individual.  Remove a field and apply the
    conv_func to that field.  Reinsert that converted data back into
    the record

    @param {dict} -- old record for a player
    @param {field} -- record index to change
    @param {conv_func} -- function that transforms field to what we want

    @return {dict} -- updated record with new fields (name, pos, team)
    """
    return dict(filter(rem_field(field), list(record.items()))
            ) | conv_func(record[field])

def rem_field(field):
    """
    Find the right field in the record (data extracted from this field
    will be added back in)

    @param {tuple} dict index, value pair where the index value must
                   match the field value.
    @param {boolean} returns True or False (True if this is the right field)
    """
    def _remove_field(f_tuple):
        if f_tuple[0] == field:
            return False
        return True
    return _remove_field

def conv_name(old_field):
    """
    Get last half of old_field and return lits of entries (this should end
    up being the player's name, position, and team

    @param {String} -- old_field.  Text info as one string.
    @return {dict} -- data interpreted from old_field displayed as a dict.
    """
    return parse_name_pos_team(halve_list(old_field.split()))

def halve_list(olist):
    """
    Return the last half of a list

    @param {list} -- olist original list
    @return {list} -- last half of olist
    """
    return olist[len(olist) // 2:]

def parse_name_pos_team(nfields):
    """
    Extract position, name, and team from the original text

    @param {list} -- {nfields} list of words in old text
    @return {dict} -- new dictionary with name, pos, and team fields
    """
    return {"name": ' '.join(nfields[0: len(nfields) // 2]),
            "pos": nfields[-2], "team": nfields[-1]}

def cbs_fixnames(raw_roto_data):
    """
    Wrapper of list of records that uses map to run fix_dict_rec
    on all entries

    @param {dict} raw_roto_data -- list of raw records
    @return {dict} -- new list with fields modified
    """
    return list(map(_fixnames2('Player')(conv_name), raw_roto_data))

def _fixnames2(idfield):
    def _fixnames3(convfunc):
        def _fixnames4(rec_data):
            """
            Call fix_dict_rec for each record
            """
            return fix_dict_rec(rec_data, idfield, convfunc)
        return _fixnames4
    return _fixnames3
