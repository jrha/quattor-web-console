import logging
import subprocess
import shutil
import re
import couchdb
import ConfigParser
import urllib
import time
from os.path import *
import os
import errno
import json

#from aquilon.config import Config

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from aquilonappliance.lib.base import BaseController, render

log = logging.getLogger(__name__)

realm_re = re.compile('(\s*default_realm\s*=\s*)([a-zA-Z.]*)')

# So many hacks, so little time.

def tail(filename, count=24):
    stdin, stdout = os.popen2("tail -n %s %s" % (count, filename))
    stdin.close()
    lines = stdout.readlines()
    stdout.close()
    return lines

def space_used(dir, units):
    total = 0
    cmd = ["du", "-s", "-b", dir]
    total = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True).communicate()[0]
    total = int(total.split()[0])
    return total/units

def get_realm():
    fd = open("/etc/krb5.conf")
    realm = "UNKNOWN"
    for line in fd.readlines():
        m = realm_re.match(line)
        if m is not None:
            realm = m.group(2)
    fd.close()
    return realm

def htmlify(input):
    return input


def aq(cmd):
    env = dict()
    env["KRB5CCNAME"] = "FILE:/var/spool/tickets/cdb"
    env["PATH"] = "/usr/local/aquilon/pythonenv/bin:/opt/aquilon/bin:/usr/local/bin:/usr/bin:/bin"
    args = ["/opt/aquilon/bin/aq"]
    args.extend(cmd)
    args.append("--noauth")
    # close all web file descriptors!
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, close_fds=True)
    (stdout, stderr) = p.communicate();
    return (stdout, stderr)

class ApplianceController(BaseController):

    def index(self):
        # Return a rendered template
        return render('/index.mako')

    def log(self, log):
        if log == 'aqd':
            c.title = "Aquilon Broker"
            logfile = "/var/log/aqd.log"
        elif log == 'pylons':
            c.title = "Web Interface"
            logfile = "/var/quattor/logs/pylons/current"
        elif log == 'warehouse':
            c.title = "Datawarehouse"
            logfile = "/usr/local/var/log/couchdb/couch.log"
        else:
            c.log = log
            return render('/badlog.mako')

        c.log = tail(logfile)
        return render('/log.mako')

    def krb5display(self):
        c.realm = get_realm()
        return render('/kerberos-setup.mako')

    def krb5configure(self):
        cfg = ConfigParser.ConfigParser()
        cfg.read(["/opt/aquilon/etc/aqd.conf.defaults", "/etc/aqd.conf"])

        cmd = ["/opt/aquilon/bin/change_realm", request.params['realm']]
        env = dict()
        env["KRB5CCNAME"] = "FILE:/var/spool/tickets/cdb"
        status = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                  env=env, close_fds=True).communicate()[0];
        if status == 0:
             return redirect('krb5display')
        return render('/krbupdate-failed.mako')

    def status(self):
        cfg = ConfigParser.ConfigParser()
        cfg.read(["/opt/aquilon/etc/aqd.conf.defaults", "/etc/aqd.conf"])

        c.base = request.environ["HTTP_HOST"]
        c.base = c.base.replace(":" + request.environ["SERVER_PORT"], "")

        # Get the broker status
        d = Daemontool("aqd")
        stat = d.status()
        if stat == 200:
            c.broker = ["Daemon: aqd broker is running"]
            (stdout, stderr) = aq(["status"])
            c.brokererr = []
            if stdout:
                c.broker.extend(stdout.split("\n"));
            if stderr:
                c.brokererr.extend(stderr.split("\n"));

            (stdout, stderr) = aq(["show_host", "--all"])
            if stdout:
                c.broker.append("Managed hosts:%s" % len(stdout.split("\n")));
            if stderr:
                c.brokererr.extend(stderr.split("\n"));
            c.brokererr = []
        else:
            c.broker = ["Daemon: aqd broker is not running"]

        # And the warehouse status
        warehouse_bin = "/opt/aquilon/bin/warehouse"
        if os.path.exists(warehouse_bin):
            cmd = [warehouse_bin, "status"]
            status = subprocess.Popen(cmd, stdout=subprocess.PIPE, close_fds=True).communicate()[0];
            c.warehouse = status.split("\n");

        units = 1024*1024 # MiB
        c.units_as_text = "MiB"

        c.space = dict()

        # Look at the disk space used
        if os.path.isdir("/var/lib/pgsql/"):
            c.space["PostgreSQL"] = space_used("/var/lib/pgsql/", units)
        if os.path.isdir("/var/lib/couchdb/"):
            c.space["CouchDB"] = space_used("/var/lib/couchdb", units)
        c.space["Logs"] = space_used("/var/log", units)
        c.space["Domains"] = space_used(cfg.get("broker", "domainsdir"), units)
        c.space["Plenary"] = space_used(cfg.get("broker", "plenarydir"), units)
        c.space["Sandboxes"] = space_used(cfg.get("broker", "templatesdir"), units)
        c.space["Git King"] = space_used(cfg.get("broker", "kingdir"), units)
        c.space["Profiles"] = space_used(cfg.get("broker", "profilesdir"), units)

        return render('/status.mako')

    def sandboxes(self):
        # If we can, check how the sandboxes are doing
        if os.path.exists("/opt/aquilon/bin/sandbox_status_json"):
            c.sandboxes = json.loads(subprocess.Popen(["/opt/aquilon/bin/sandbox_status_json"], stdout=subprocess.PIPE, close_fds=True).communicate()[0])

        return render('/sandboxes.mako')

    def about(self):
        return render('/credits.mako')

class Daemontool:
    def __init__(self, name=None):
        self.name = name
        self.base = "/etc/init.d"

    def status(self):
        if not os.path.exists("%s/%s" % (self.base, self.name)):
            return 404
        cmd = ["%s/%s" % (self.base, self.name), "status"]
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True).communicate()[0];
        if "is running" in out:
            return 200
        return 500
