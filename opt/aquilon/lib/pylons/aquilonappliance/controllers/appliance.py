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
import csv
from xml.etree import ElementTree as ETree

#from aquilon.config import Config

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from aquilonappliance.lib.base import BaseController, render

log = logging.getLogger(__name__)

realm_re = re.compile('(\s*default_realm\s*=\s*)([a-zA-Z.]*)')

# So many hacks, so little time.

# This should really be in input.xml, but we'll just
# provide "overlay" information until that time.
lookup = {
    'archetype': {'cmd':'show_archetype','fmt':'csv'},
    'personality': {'cmd':'show_personality','fmt':'csv'},
    'osname': {'cmd':'show_os','fmt':'csv'},
    'model': {'cmd':'show_model','fmt':'csv'},
    'hub': {'cmd':'show_hub','fmt':'csv', 'label':7,'value':1},
    'organization': {'cmd':'show_organization','fmt':'csv','label':7,'value':1},
    'continent': {'cmd':'show_continent','fmt':'csv', 'label':7,'value':1},
    'city': {'cmd':'show_city','fmt':'csv', 'label':7,'value':1},
    'building': {'cmd':'show_building','fmt':'csv', 'label':7,'value':1},
    'country': {'cmd':'show_country','fmt':'csv', 'label':7,'value':1},
    'rack': {'cmd':'show_rack','fmt':'csv', 'label':7,'value':1},
    'dns_domain': {'cmd':'show_dns_domain','fmt':'csv'},
    'principal': {'cmd':'show_principal','fmt':'csv'},
    'hostname': {'cmd':'show_host','fmt':'csv'},
    'machine': {'cmd':'show_machine','fmt':''},
    'vendor': {'cmd':'show_vendor','fmt':'csv'},
    'cpuname': {'cmd':'show_cpu','fmt':'csv'},
}

def space_used(dir, units):
    total = 0
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        try:
            st = os.stat(path)
        except:
            pass
        total += st.st_size
        if isdir(path) and not islink(path):
            try:
                total += space_used(path, units)
            except:
                pass
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
    env["PATH"] = "/opt/aquilon/bin:/usr/local/bin:/usr/bin:/bin"
    args = ["/opt/aquilon/bin/aq"]
    args.extend(cmd)
    # close all web file descriptors!
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, close_fds=True)
    (stdout, stderr) = p.communicate();
    return (stdout, stderr)

class ApplianceController(BaseController):

    def emitfields(self, cmd, group):
        mandatory = False
        if "mandatory" in group.attrib and group.attrib["mandatory"] == "True":
            mandatory = True

        c.form.append("<fieldset><legend>%s</legend><ol>" % group.attrib["name"])
        gname = group.attrib["name"]
        if "fields" in group.attrib and group.attrib["fields"] == "any":
            label = "<b>%s:</b>" % group.attrib["name"]
            if group.text:
                label += " %s" % group.text
            if mandatory:
                label = label + "<font color='red'>*</font>"
            # Only one-of needs to be specified, so run through children
            # finding all the possibles and make a combobox
            gname_extra = "_input_" + gname
            combo = list()
            for opt in group.getchildren():
                if (opt.tag == "optgroup"):
                    # This is painful - we have some grouped fields
                    # inside our combobox. this breaks - XXX
                    pass
                if opt.text.startswith("[Deprecated]"):
                    pass
                combo.append(opt.attrib['name'])
            c.form.append("<li><label for='%s'>%s</label>" % (gname, label))
            c.form.append("<select id='%s' name='%s'>" % (gname, gname))
            for opt in combo:
                c.form.append("<option>%s</option>" % opt)
            c.form.append("</select>")
            c.form.append("<input id='%s' name='%s' size='38'/></li>" %
                          (gname_extra, gname_extra))
            c.form.append("</ol></fieldset>")
            return

        for opt in group.getchildren():
            if (opt.tag == "optgroup"):
                self.emitfields(cmd, opt)
                continue
            if opt.text.startswith("[Deprecated]"):
                continue
            if "mandatory" in opt.attrib and opt.attrib["mandatory"] == "True":
                mandatory = True
            label = "<b>%s:</b> %s" % (opt.attrib["name"], opt.text)
            name = opt.attrib["name"]
            basename = name
            if name.endswith("name"):
                basename = name[:-4]
            if mandatory:
                label = label + "<font color='red'>*</font>"
            label = "<li><label for='%s'>%s</label>" % (name, label)
            if opt.attrib['type'] == "boolean" or opt.attrib['type'] == 'flag':
                c.form.append("%s<input id='%s' name='%s' type='checkbox' value='1'/></li>" % (label, name, name))
            else:
                field = "%s<input id='%s' name='%s' size='48' value=''/></li>" % (label, name, name)
                if name in lookup and (cmd != "add_%s" % basename):
                    inf = lookup[name]
                    invoke = [inf["cmd"], "--all"]
                    if inf["fmt"] != "":
                        invoke.extend(["--format", inf["fmt"]])
                    (stdout, stderr) = aq(invoke)
                    options = stdout.split("\n")
                    field = ("%s<select id='%s' name='%s'>" % 
                                  (label, name, name))
                    for opt in csv.reader(options):
                        if len(opt) == 0:
                            continue
                        if 'label' in inf:
                            label = opt[inf['label']]
                        else:
                            label = opt[0]
                        if 'value' in inf:
                            value = opt[inf['value']]
                        else:
                            value = opt[0]
                        if label == "":
                            label = value
                        field = field + "<option value='%s'>%s</option>" % (value, label)
                    if not mandatory:
                        field = field + "<option value='' selected='selected'>&lt;unspecified&gt;</select>"
                    field = field + "</select>"

                c.form.append(field)

        c.form.append("</ol></fieldset>")

    def commandindex(self):
        c.objects = dict()
        c.commands = dict()
        description = dict()
        input = open('/opt/aquilon/etc/input.xml')
        etree = ETree.parse(input)
        for cmdnode in etree.getroot().findall("command"):
            name = cmdnode.attrib['name']
            if name == '*':
                continue
            description[name] = cmdnode.text
            objectmatch = re.compile('((?:add)|(?:del)|(?:update)|(?:show)|(?:search))_(.*)')
            m = objectmatch.match(name)
            if m:
                if m.group(2) not in c.objects:
                    c.objects[m.group(2)] = dict()
                c.objects[m.group(2)][m.group(1)] = name
            else:
                c.commands[name] = cmdnode.text

        # After we've partitioned all the commands into CRUD objects and
        # non-crud stuff, we may have guessed some of it wrongly...
        for obj in c.objects.keys():
            if len(c.objects[obj].keys()) < 2:
                origcmd = c.objects[obj].values()[0]
                c.commands[origcmd] = description[origcmd]
                del c.objects[obj]
 
        return render('/commands.mako')


    def index(self):
        # Return a rendered template
        return render('/index.mako')

    def log(self, log):
        if log == 'aqd':
            c.title = "Aquilon Broker"
            logfile = "/var/quattor/logs/aqd.log"
        elif log == 'pylons':
            c.title = "Web Interface"
            logfile = "/var/quattor/logs/pylons/current"
        elif log == 'warehouse':
            c.title = "Datawarehouse"
            logfile = "/usr/local/var/log/couchdb/couch.log"
        else:
            c.log = log
            return render('/badlog.mako')

        c.log = list()
        fp = open(logfile)
        for line in fp.read():
            html = htmlify(line)
            c.log.append(html)
        return render('/log.mako')

    def generate_form(self, cmd):
        c.form = list()
        c.cmd = cmd
        input = open('/opt/aquilon/etc/input.xml')
        etree = ETree.parse(input)
        for cmdnode in etree.getroot().findall("command"):
            if cmdnode.attrib['name'] != cmd:
                continue

            c.text = cmdnode.text
            for group in cmdnode.findall("optgroup"):
                self.emitfields(cmd, group)

        if "_return" in request.params:
            c.form.append("<input type='hidden' name='_return' value='%s'\>" % 
                          request.params["_return"])
        c.form.append("<input type='submit' value='%s'/>" % cmd)

        return render('/form.mako')

    def process_form(self, cmd):
        # turn request object into something to run via an aq command
        c.cmd = cmd
        opttypes = dict()
        input = open('/opt/aquilon/etc/input.xml')
        etree = ETree.parse(input)
        for cmdnode in etree.getroot().findall("command"):
            if cmdnode.attrib['name'] != cmd:
                continue
            c.text = cmdnode.text
            for group in cmdnode.findall("optgroup"):
                self.parse_group(group, opttypes)

        args = list()
        args.append(cmd)
        for key in request.params.keys():
            
            if key in opttypes:
                if opttypes[key] == 'boolean' or opttypes[key] == 'flag':
                    if request.params[key] == "1":
                        args.append("--%s" % key)
                else:
                    if request.params[key] != "":
                        args.append("--%s=%s" % (key, request.params[key]))

            elif key.startswith("_input_"):
                # This is a faked up key that we made!
                m = re.match("_input_(.*)", key)
                selector = m.group(1)
                if selector in request.params:
                    realopt = request.params[selector]
                    if realopt in opttypes and (
                        opttypes[realopt] == 'flag' or
                        opttypes[realopt] == 'boolean'):
                        args.append("--%s" % realopt)
                    else:
                        args.append("--%s=%s" % (realopt,
                                                 request.params[key]))

        (c.stdout, c.stderr) = aq(args)
        if c.stderr == "acquired compile lock\nreleasing compile lock\n":
            c.stderr = ""
        compileoutput = re.compile(".*BUILD SUCCESSFUL.*", re.DOTALL)
        if compileoutput.match(c.stderr):
            c.stdout = c.stderr
            c.stderr = ""
        if c.stderr == "" and "_return" in request.params:
            return redirect(request.params["_return"])
        return render('/formresults.mako')

    def parse_group(self, group, opttypes):
        for option in group.getchildren():
            if option.tag == "optgroup":
                self.parse_group(option, opttypes)
            elif option.tag == "option":
                opttypes[option.attrib["name"]] = option.attrib["type"]

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
        # XXX: this should use cfg, but the ConfigParser doesn't work right...
        if not os.path.exists("/var/quattor/aquilondb/aquilon.db"):
            return redirect("/reset")

        c.base = request.environ["HTTP_HOST"]
        c.base = c.base.replace(":" + request.environ["SERVER_PORT"], "")

        # Get the broker status
        d = Daemontool("aqd", "/opt/aquilon/etc/sv/aqd")
        stat = d.status()
        if stat == 200:
            (stdout, stderr) = aq(["status"])
            c.broker = []
            c.brokererr = []
            if stdout:
                c.broker = stdout.split("\n");
            if stderr:
                c.brokererr = stderr.split("\n");
        else:
            c.broker = ["The broker is not running"]

        # And the warehouse status
        cmd = ["/opt/aquilon/bin/warehouse", "status"]
        status = subprocess.Popen(cmd, stdout=subprocess.PIPE, close_fds=True).communicate()[0];
        c.warehouse = status.split("\n");

        # Look at the disk space used
        disk = os.statvfs("/var")
        units = 1024*1024 # MiB
        c.units_as_text = "MiB"
        c.space = dict()
        c.space["free"] = (disk.f_bsize * disk.f_bavail)/units
        c.space["aqdb"] = space_used(cfg.get("database", "dbdir"), units)
        c.space["warehouse"] = space_used("/var/lib/couchdb", units)
        c.space["logs"] = space_used("/var/log", units) + \
                          space_used(cfg.get("DEFAULT", "logdir"), units)
        c.space["templates"] = space_used(cfg.get("broker", "domainsdir"), units) + \
                               space_used(cfg.get("broker", "templatesdir"), units) + \
                               space_used(cfg.get("broker", "kingdir"), units)
        c.space["profiles"] = space_used(cfg.get("broker", "profilesdir"), units) + \
                              space_used(cfg.get("broker", "depsdir"), units) + \
                              space_used(cfg.get("broker", "hostsdir"), units)
        c.totalspace = 0
        for (key, value) in c.space.items():
            c.totalspace += value

        return render('/status.mako')

    def about(self):
        return render('/credits.mako')

    def reset_form(self):
        c.profiles = ''
        c.org = ''
        c.orgtext = ''
        return render('/reset/start.mako');

    def reset_apply(self):
        # make sure that aq is not running before we start breaking things
        d = Daemontool("aqd", "/opt/aquilon/etc/sv/aqd")
        d.stop()

        errors = list()

        # copy in place a new aqd.conf with the default_org filled in
        cfg = ConfigParser.ConfigParser()
        cfg.read(["/opt/aquilon/etc/aqd.conf.defaults", "/opt/aquilon/etc/appliance.conf"])
        cfg.set("broker", "default_organization", request.params["org"])
        fp = open("/etc/aqd.conf", "w")
        cfg.write(fp)
        fp.close()

        try:
            os.unlink(cfg.get("broker", "logfile"))
        except OSError as e:
            if e.errno not in [errno.ENOENT]:
                errors.append("Errors from cleaning aqd logfile: %s" % e)
            pass

        db = cfg.get("database_sqlite", "dbfile")
        try:
            os.unlink(db)
        except OSError as e:
            if e.errno not in [errno.ENOENT]:
                errors.append("Errors from cleaning sqlite aqdb: %s" % e)
            pass

        try:
            shutil.rmtree(cfg.get("broker", "profilesdir"))
        except OSError as e:
            if e.errno not in [errno.ENOENT]:
                errors.append("Errors from rmtree profiles: %s" % e)
            pass

        os.mkdir(cfg.get("broker", "profilesdir"))

        env = dict()
        env["KRB5CCNAME"] = "FILE:/var/spool/tickets/cdb"
        env["PYTHONPATH"] = "/opt/aquilon/lib/python2.6/"
        env["PATH"] = "/opt/aquilon/bin:/usr/sbin:/usr/bin:/bin:/python2.6/"
        shutil.copy("/opt/aquilon/etc/minimal.dump", "/tmp/bootstrap.dump")
        realm = get_realm()
        principal = "cdb/aqd.aquilon.example.com"
        fd = open("/tmp/bootstrap.dump", "a")
        fd.write("Realm(name=\"%s\")\n" % realm)
        fd.write("UserPrincipal(name=\"%s\", role=Role(name=\"aqd_admin\"), "
                 "realm=Realm(name=\"%s\"))\n" % (principal, realm))
        fd.write("UserPrincipal(name=\"%s\", role=Role(name=\"aqd_admin\"), "
                 "realm=Realm(name=\"%s\"))\n" % ("cdb", realm))
        fd.write("Domain(name=\"prod\", owner=UserPrincipal(name=\"%s\"),"
                 "compiler=\"/opt/aquilon/lib/panc/panc-prod.jar\")\n" %
                  principal)
        fd.write("Company(name=\"%s\", fullname=\"%s\")\n" % 
                 (request.params["org"], request.params["orgtext"]))
        fd.close()
        cmd = ["/opt/aquilon/util/build_db.py", "-p", "/tmp/bootstrap.dump"]
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, close_fds=True,
                               env=env).communicate()[1];
        # XXX: checkout out/return status of above popen
        if out != "":
            err = False
            for line in out.split("\n"):
                if line.startswith("ERR"):
                    err = True
            if err:
                errors.append("Errors from building bootstrap db: %s" % out)

        d.start()
        # XXX: Wait to see that we get a good broker log entry

        # XXX: We want to do this, but it hangs for some reason...
        #args = ["add_organization", "--organization", request.params["org"]]
        #if "orgtext" in request.params and request.params["orgtext"] != "":
        #    args.extend(["--fullname", request.params["orgtext"]])
        #(stdout, stderr) = aq(args)
        #if stderr != "":
        #    errors.append("Errors from adding organization: %s" % stderr)

        # XXX: This bit should be made "ajaxy":
        # validate in the client before submit!
        profiles = ""
        if 'profiles' in request.params:
            profiles = request.params['profiles']
        while len(profiles) > 0 and profiles.endswith('/'):
            profiles = profiles[0:-1]
        if profiles != "":
            try:
                urllib.urlopen("%s/profiles-info.xml" % profiles)
            except:
                return render("/reset-bad-profiles.mako")
            # Okay, so we can bootstrap!
            return redirect("reset/bootstrap")
        if len(errors) > 0:
            c.errors = errors
            return render("/reset/errors.mako")
        return redirect("reset/manual")

    def reset_manual(self):
        c.realm = get_realm()
        return render('/reset/manual.mako')

    def reset_bootstrap(self):
        return render('/reset/bootstrap.mako')

class Daemontool:
    def __init__(self, name=None, source=None):
        self.name = name
        self.source = source
        self.base = "/etc/service"
        self.bin = "/usr/bin"

    def status(self):
        if not os.path.isdir("%s/%s" % (self.base, self.name)):
            return 404
        cmd = ["sudo", "%s/svstat" % self.bin, "%s/%s" % (self.base, self.name)]
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, close_fds=True).communicate()[0];
        if out.startswith("%s/%s: down" % (self.base, self.name)):
            return 500
        return 200

    def start(self):
        if not os.path.isdir("%s/%s" % (self.base, self.name)):
            os.symlink(self.source, "%s/%s" % (self.base, self.name))
        cmd = ["sudo", "%s/svc" % self.bin, "-u", "%s/%s" % (self.base, self.name)]
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, close_fds=True,
                               stderr=subprocess.PIPE).communicate()[0];
        
    def stop(self):
        cmd = ["sudo", "%s/svc" % self.bin, "-d", "%s/%s" % (self.base, self.name)]
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, close_fds=True,
                               stderr=subprocess.PIPE).communicate()[0];
        

