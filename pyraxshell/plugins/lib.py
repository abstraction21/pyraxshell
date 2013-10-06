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

from utility import l


class Lib():
    
    def r(self, retcode, msg, log_level):
        '''
        record Session command input/output to 'commands' table, and
        logging message facility
        '''
        l('', retcode, msg, log_level)
#         Sessions.Instance().insert_table_commands('' # @UndefinedVariable
#                                                   , msg, retcode, log_level)
