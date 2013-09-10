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
import pyrax.exceptions as exc

class LibLoadBalancers(object):
    '''
    pyraxshell load-balancers library
    '''
    
    # ########################################
    # LOAD-BALANCERS

    def get_loadbalancer_by_id(self, _id):
        '''
        return Cloud load-balancer instance specified by id
        '''
        clb = pyrax.cloud_loadbalancers
        try:
            return [lb for lb in clb.list() if lb.id == int(_id)][0]
        except IndexError:
            logging.error('cannot find Cloud loadbalancer with id:%s' % _id)
            return None
        except:
            logging.error('error searching Cloud loadbalancer by id:%s' % _id)
            return None
