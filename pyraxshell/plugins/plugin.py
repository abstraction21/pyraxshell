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

import cmd
import logging
from configuration import Configuration
from sessions import Sessions
from globals import *  # @UnusedWildImport

name = 'none'


class Plugin(cmd.Cmd):
    '''
    Plugin base class
    '''
    
    prompt = "RS %s>" % name    # default prompt
    
    def __init__(self):
        '''
        Constructor
        '''
        cmd.Cmd.__init__(self)
        self.cfg = Configuration.Instance()  # @UndefinedVariable
        # current command
        self.cmd = None
        self.arg = None
        self.line = None
    
    def emptyline(self):
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
        if self.lastcmd:
            self.lastcmd = ""
            return self.onecmd('\n')
    
    def parseline(self, line):
        '''
        override 'cmd.Cmd.parseline' to store cmd, arg and line
        '''
        self.cmd, self.arg, self.line = cmd.Cmd.parseline(self, line)
        return self.cmd, self.arg, self.line

    def preloop(self):
        '''
        override preloop and verify if user is authenticated
        '''
        cmd.Cmd.preloop(self)
        logging.debug("preloop")
        import plugins.libauth
        if not plugins.libauth.LibAuth().is_authenticated():
            logging.warn('please, authenticate yourself before continuing')
    
    def do_EOF(self, line):
        '''
        just press CTRL-D to quit this menu
        '''
        print
        return True
    
    def do_dir(self, line):
        '''
        list alias
        '''
        return self.do_list(line)

    def do_exit(self, line):
        '''
        EOF alias
        '''
        return self.do_EOF(line)
    
    def do_list(self, line):
        '''
        default list method (this needs to be here to define aliases: ls, ll, dir)
        '''
    
    def do_ll(self, line):
        '''
        list alias
        '''
        return self.do_list(line)
    
    def do_ls(self, line):
        '''
        list alias
        '''
        return self.do_list(line)
    
    def do_quit(self, line):
        '''
        EOF alias
        '''
        return self.do_EOF(line)

    def r(self, retcode, msg, log_level):
        '''
        record Session command input/output to 'commands' table, and
        logging message facility
        '''
        logging.debug("[IN] %s" % self.cmd)
        logging.debug("[OUT] %s, log_level:%d" % (msg, log_level))
        interactive = Configuration.Instance().interactive  # @UndefinedVariable
        if log_level == DEBUG:
            logging.debug(msg)
            if not interactive:
                msg += "0|%s" % msg
        if log_level == INFO:
            logging.info(msg)
            if not interactive:
                msg += "0|%s" % msg
        if log_level == WARN:
            logging.warn(msg)
            if not interactive:
                msg += "0|%s" % msg
        if log_level == ERROR:
            logging.error(msg)
            if not interactive:
                msg += "1|%s" % msg
        if log_level == CRITICAL:  # @UndefinedVariable
            logging.critical(msg)
            if not interactive:
                msg += "1|%s" % msg
        Sessions.Instance().insert_table_commands(self.cmd, msg, retcode, # @UndefinedVariable
                                                  log_level)
