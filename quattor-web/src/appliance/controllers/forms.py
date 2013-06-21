import logging
import subprocess
import shutil
import re
import ConfigParser
import urllib
from os.path import *
import os
import csv
from xml.etree import ElementTree as ETree

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

def aq(cmd):
    env = dict()
    #env["KRB5CCNAME"] = "FILE:/var/spool/tickets/cdb"
    env["PATH"] = "/usr/local/aquilon/pythonenv/bin:/opt/aquilon/bin:/usr/local/bin:/usr/bin:/bin"
    args = ["/opt/aquilon/bin/aq"]
    args.extend(cmd)
    args.append("--noauth")
    # close all web file descriptors!
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, close_fds=True)
    (stdout, stderr) = p.communicate();
    return (stdout, stderr)

class FormsController(BaseController):

    def index(self):
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

    def emitfields(self, cmd, group):
        mandatory = False
        if "mandatory" in group.attrib and group.attrib["mandatory"] == "True":
            mandatory = True

        c.form.append("<fieldset><legend>%s</legend><ol>" % group.attrib["name"].replace("_opts", ""))
        gname = group.attrib["name"]
        if "fields" in group.attrib and group.attrib["fields"] == "any":
            label = "<b>%s:</b>" % group.attrib["name"]
            if group.text:
                label += " %s" % group.text
            if mandatory:
                label = label + "<span class='badge badge-important'>mandatory</span>"
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
            c.form.append("<input id='%s' name='%s' size='38' type='text' /></li>" %
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
                label = label + " <span class='badge badge-important'>mandatory</span>"
            label = "<li><label for='%s'>%s</label>" % (name, label)
            if opt.attrib['type'] == "boolean" or opt.attrib['type'] == 'flag':
                c.form.append("%s<input id='%s' name='%s' type='checkbox' value='1'/></li>" % (label, name, name))
            else:
                field = "%s<input id='%s' name='%s' size='48' value='' type='text' placeholder='%s' /></li>" % (label, name, name, basename)
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

    def generate_form(self, cmd):
        c.form = list()
        c.cmd = cmd
        c.documentation = None
        if os.path.exists("/opt/aquilon/doc/html/%s.html" % cmd):
            c.documentation = "/aqdocs/%s.html" % cmd
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
        c.form.append("<input type='submit' value='%s' class='btn btn-primary' />" % cmd.replace("_", " "))

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

