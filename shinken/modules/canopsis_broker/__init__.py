#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2009-2012:
#    Gabes Jean, naparuba@gmail.com
#    Gerhard Lausser, Gerhard.Lausser@consol.de
#    Gregory Starck, g.starck@gmail.com
#    Hartmut Goebel, h.goebel@goebel-consult.de
#	 David GUENAULT, dguenault@monitoring-fr.org
#
# This file is part of Shinken.
#
# Shinken is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinken is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Shinken.  If not, see <http://www.gnu.org/licenses/>.


import sys
#from kombu import BrokerConnection, Exchange, Queue
from shinken.log import logger


#called by the plugin manager to get a instance
def get_instance(mod_conf):

    try:
        from canopsis_broker import Canopsis_broker
    except ImportError , exp:
        logger.Warning("The plugin type %s is unavailable : %s" % (properties['type'], exp))
        return None

    logger.info("Get a canopsis instance for plugin %s" % mod_conf.get_name())

    instance = Canopsis_broker(mod_conf)

    return instance