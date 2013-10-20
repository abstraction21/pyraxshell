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

import logging
import pyrax
import signal
import sys

import version
from db import DB
from configuration import Configuration
from globals import CONFIG_FILE, HOME_DIR, VERSION_FILE  # @UnusedImport
from log import start_logging
from notifier import Notifier
from pyraxshell import Cmd_Pyraxshell
from sessions import Sessions
from utility import check_dir_home, terminate_threads


def main():
    # check '~/.pyraxshell' and config files exist, create them if missing
    if not check_dir_home():
        print ("This is the first time 'pyraxshell' runs, please, configure "
               "'%s' according to your needs" % CONFIG_FILE)
        #create db
        DB()
        Sessions.Instance().create_table_sessions()  # @UndefinedVariable
        Sessions.Instance().create_table_commands()  # @UndefinedVariable
        # create default configuration file
        Configuration.Instance()  # @UndefinedVariable
        sys.exit(0)
    
    # ########################################
    # VERSION CHECK
    if not version.check_version_file():
        sys.exit(1)
    
    # ########################################
    # LOGGING
    start_logging()
    logging.debug('starting')
    
    # ########################################
    # CONFIGURATION
    cfg = Configuration.Instance()  # @UndefinedVariable
    # first read config file 
    cfg.parse_config_file()
    # override settings with CLI params
    cfg.parse_cli(sys.argv)
    logging.debug("configuration: %s" % cfg)
    
    # set user's log level if specified 
    if not Configuration.Instance().log_level == None:  # @UndefinedVariable
        l = logging.getLogger()
        for h in l.handlers:
            h.setLevel(cfg.log_level)
    
    # ########################################
    # START SESSION
    Sessions.Instance().start_session()  # @UndefinedVariable
#     Sessions.Instance().insert_table_commands('IN', 'OUT')  # @UndefinedVariable
    
    # ########################################
    # DO STUFF
    # handle configuration
    if cfg.pyrax_http_debug == True:
        pyrax.set_http_debug(True)
    if cfg.pyrax_no_verify_ssl == True:
        # see: https://github.com/rackspace/pyrax/issues/187
        pyrax.set_setting("verify_ssl", False)
    # start notifier
    Notifier().start()
    # main loop
    Cmd_Pyraxshell().cmdloop()


def signal_handler(signal, frame):
    '''
    handle signals (i.e.: SIGINT, SIGTERM), and stop threads 
    '''
    terminate_threads()
    sys.exit(0)


if __name__ == '__main__':
    # register SIGINT and SIGTERM handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    main()
