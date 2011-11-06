#!/usr/bin/python -u
import sys
sys.path.append("/opt/aquilon/lib/python2.6")

import paste.deploy
wsgi_app = paste.deploy.loadapp('config:/opt/aquilon/etc/production.ini')
serve = paste.deploy.loadserver('config:/opt/aquilon/etc/production.ini')
serve(wsgi_app)
