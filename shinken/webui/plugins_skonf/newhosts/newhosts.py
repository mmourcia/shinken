#!/usr/bin/env python
#Copyright (C) 2009-2011 :
#    Gabes Jean, naparuba@gmail.com
#    Gerhard Lausser, Gerhard.Lausser@consol.de
#    Gregory Starck, g.starck@gmail.com
#    Hartmut Goebel, h.goebel@goebel-consult.de
#    Andreas Karfusehr, andreas@karfusehr.de
#
#This file is part of Shinken.
#
#Shinken is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Shinken is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Shinken.  If not, see <http://www.gnu.org/licenses/>.

import time
import random

from shinken.webui.bottle import redirect
from shinken.util import to_bool


# Ask for a random init
random.seed(time.time())


### Will be populated by the UI with it's own value
app = None

# Our page. If the useer call /dummy/TOTO arg1 will be TOTO.
# if it's /dummy/, it will be 'nothing'
def get_newhosts():
    # First we look for the user sid
    # so we bail out if it's a false one
    user = app.get_user_auth()

    if not user:
        pass
        #redirect("/user/login")
        #return

    # we return values for the template (view). But beware, theses values are the
    # only one the tempalte will have, so we must give it an app link and the
    # user we are loggued with (it's a contact object in fact)
    return {'app' : app, 'user' : user}



def get_launch():
    print "Got forms in /newhosts/launch page"
    names = app.request.forms.get('names', '')
    use_nmap = to_bool(app.request.forms.get('use_nmap', '0'))
    use_vmware = to_bool(app.request.forms.get('use_vmware', '0'))
    
    print "Got in request form"
    print names
    print 'nmap?', use_nmap
    print 'vmware?', use_vmware

    # We are putting a ask ask in the database
    i = random.randint(1, 65535)
    scan_ask = {'_id' : i, 'names' : names, 'use_nmap' : use_nmap, 'use_vmware' : use_vmware, 'state' : 'pending', 'creation' : int(time.time())}
    print "Saving", scan_ask, "in", app.db.scans
    r = app.db.scans.save(scan_ask)
    # We just want the id as string, not the object
    print "We create the scan", i
    app.ask_new_scan(i)

    return {'app' : app}



def get_scans():
    print "Got scans"
    return {'app' : app}


def get_results():
    print "Looking for hosts in pending aprouval"
    cur = app.db.discovered_hosts.find({})
    pending_hosts = [h for h in cur]

    print "And in progress scans"
    cur = app.db.scans.find({})
    scans = [s for s in cur]
    for s in scans:
        print "SCAN", s

    return {'app' : app, 'pending_hosts' : pending_hosts, 'scans' : scans}



def post_validatehost():
    print "Got forms in /newhosts/validatehost call"
    _id = app.request.forms.get('_id', 'unknown-host')
    tags = app.request.forms.get('tags', '')
    host_name = app.request.forms.get('host_name', None)

    print "DUMP FORMS", app.request.forms
    print "Got in request form", _id, host_name, tags
    if not host_name:
        print "BAD HOST NAME for post_validatehost bail out"
        return None

    host = {'_id' : _id, 'host_name' : host_name, 'use' : tags}
    print "Saving", host, "in", app.db.hosts
    r = app.db.hosts.save(host)
    print "result", r

    # Now we can remove the one in the discovered part
    print "And deleting the discovered host"
    r = app.db.discovered_hosts.remove({'_id' : _id})
    print "result", r

    return None



# This is the dict teh webui will try to "load".
#  *here we register one page with both adresses /dummy/:arg1 and /dummy/, both addresses
#   will call the function get_page.
#  * we say taht for this page, we are using the template file dummy (so view/dummy.tpl)
#  * we said this page got some static stuffs. So the webui will match /static/dummy/ to
#    the dummy/htdocs/ directory. Bewere : it will take the plugin name to match.
#  * optional : you can add 'method' : 'POST' so this adress will be only available for
#    POST calls. By default it's GET. Look at the lookup module for sample about this.
pages = {get_newhosts : { 'routes' : ['/newhosts'], 'view' : 'newhosts', 'static' : True},
         get_launch : { 'routes' : ['/newhosts/launch'], 'view' : 'newhosts_launch', 'static' : True, 'method' : 'POST'},
         get_scans : { 'routes' : ['/newhosts/scans'], 'view' : 'newhosts_scans', 'static' : True},
         get_results : { 'routes' : ['/newhosts/results'], 'view' : 'newhosts_results', 'static' : True},
         post_validatehost : { 'routes' : ['/newhosts/validatehost'], 'view' : None, 'method' : 'POST'},
         }
