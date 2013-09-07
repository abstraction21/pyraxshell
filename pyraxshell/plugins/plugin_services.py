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
from utility import kvstring_to_dict

import pprint
import pyrax
from prettytable import PrettyTable

name = 'services'

def injectme(c):
    setattr(c, 'do_services', do_services)
    logging.debug('%s injected' % __file__)
#     
#     logging.debug('c.get_names(): %s' % c.get_names())

def do_services(*args):
#     logging.debug("line: %s" % line)
    Cmd_Services().cmdloop()

class Cmd_Services(cmd.Cmd):
    """
    pyraxshell - Services plugin 
    """
    prompt = "H %s>" % name    # default prompt
    
    def do_exit(self,*args):
        return True

    def do_test(self, line):
        '''
        provide credentials and authenticate
        '''
        logging.debug("TEST PLUGIN -- do_test")
        logging.debug("line: %s" % line)
    
    def do_EOF(self, line):
        print
        return True

    def preloop(self):
        cmd.Cmd.preloop(self)
        logging.debug("preloop")
        import plugins.libauth
        if not plugins.libauth.LibAuth().is_authenticated():
            logging.warn('please, authenticate yourself before continuing')

    # ########################################
    # ENDPOINTS
    def do_endpoints(self, line):
        '''
        list endponts
        
        raw            print raw JSON response
        '''
        logging.debug("line: %s" % line)
        d_kv = kvstring_to_dict(line)
        logging.debug("kvs: %s" % d_kv)
        # default values
        (raw) = (False)
        # parsing parameters
        if 'raw' in d_kv.keys():
            raw = True
        if not raw:
            pt = PrettyTable(['service', 'name', 'endpoints'])
            for k,v in pyrax.identity.services.items():
#                 print "service: %s" % k
#                 print "\tname: %s" % v['name']
#                 print "\tendpoints: %s" % v['endpoints']
                ep = ''
                for k1,v1 in v['endpoints'].items():
#                     print "\t\t%s --> %s" % (k1, v1)
                    ep += "\n".join("%s: %s --> %s" % (k1, k2, v2)
                                    for k2,v2 in v1.items())
                pt.add_row([k, v['name'], ep])
            pt.align['service'] = 'l'
            pt.align['name'] = 'l'
            pt.align['endpoints'] = 'l'
            print pt
        else:
            pprint.pprint(pyrax.identity.services)
    
    def do_list(self, line):
        '''
        list services
        '''
        logging.info("\n".join([s for s in pyrax.services]))
