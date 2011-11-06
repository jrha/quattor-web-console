# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1316726059.65451
_template_filename='/home/cdb/aquilon-appliance/aquilonappliance/templates/kerberos-setup.mako'
_template_uri='/kerberos-setup.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = []


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n<h1>Kerberos Configuration</h1>\n<form method="get" action=\'krb5configure\'>\n<table>\n<tr><th>Realm</th><td><input name=\'realm\' size=40 value=\'')
        # SOURCE LINE 5
        __M_writer(escape(c.realm))
        __M_writer(u"'></td></tr>\n<tr><td></td><td><input type='submit' value='Change Realm'></td></tr>\n</table>\n</form>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


