# -*- coding: utf-8 -*-

# This file is part of pyraxshell.
#
# pyraxshell is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyraxshell is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyraxshell. If not, see <http://www.gnu.org/licenses/>.

'''
Created on 8 Jul 2013

@author: soldasimo
'''
import os.path
import logging  # @UnusedImport
import logging.config

def print_dict(d, indent=0, indent_string = "--"):
    '''recursively print nested dictionaries''' 
    for k,v in d.items():
        if type(v) is not dict:
            print "%s%s --> %s" % ((indent_string * indent), k, v)
        else:
            print "%s%s:" % ((indent_string * indent), k)
            print_dict(v, indent+1)

def logging_start():
    this_dir, this_filename = os.path.split(__file__)  # @UnusedVariable
    log_config_file_locations = map(lambda i: os.path.join(this_dir, i),
                                    ['./logging.conf', './conf/logging.conf',
                                     '../conf/logging.conf'])
    log_config_file = None    
    for f in log_config_file_locations:
        if os.path.exists(os.path.expanduser(f)):
            log_config_file = f
            logging.config.fileConfig(log_config_file)
            logging.debug("found log config file: %s" % f)
    if log_config_file == None:
        logging.warn('could not find log config file (default locations: \'%s\')'
                     % log_config_file_locations)

def kvstring_to_dict(kvs):
    '''
    transform a key-value-string to dictionary
    key-value separator can be ':' or '=', even mixed!
    
    return None in case of error
    
    i.e.: "k0:v0 k1:v1 ... ki:vi" ==> {'k0':'v0','k1':'v1','ki':'vi'}
    '''
    logging.debug(kvs)
    d_out = {}
    kvs = kvs.replace('=', ':')
    try:
        for token in kvs.split():
            kv = token.split(':')
            d_out[kv[0]] = kv[1]
    except:
        logging.error('cannot parse key-value-string')
    return d_out

def is_ipv4(address):
    '''
    check if address is valid IP v4
    '''
    import socket
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False
