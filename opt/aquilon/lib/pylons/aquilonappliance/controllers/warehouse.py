import logging
from subprocess import Popen, PIPE
import couchdb

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from aquilonappliance.lib.base import BaseController, render

log = logging.getLogger(__name__)

class WarehouseController(BaseController):

    def index(self):
        couch = couchdb.Server()
        db = couch["profiles"]
        c.base = request.environ["HTTP_HOST"]
        c.base = c.base.replace(":" + request.environ["SERVER_PORT"], "")
        return render('/warehouse/status.mako')


    def upload(self):
        cmd = ["/opt/aquilon/bin/upload-profiles"]
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        (c.stdout, c.stderr) = p.communicate();
        if c.stderr == "":
             redirect('/')
        return render('/warehouse/upload-failed.mako')

