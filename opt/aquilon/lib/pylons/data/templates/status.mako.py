# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1316637139.676095
_template_filename='/home/cdb/aquilon-appliance/aquilonappliance/templates/status.mako'
_template_uri='/status.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        len = context.get('len', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<html>\n<head>\n<title>Aquilon Appliance Status</title>\n    <script language="javascript" type="text/javascript" src="/flot/jquery.js"></script>\n    <script language="javascript" type="text/javascript" src="/flot/jquery.flot.js"></script>\n\n</head>\n<body>\n<table>\n')
        # SOURCE LINE 10

        for i in c.broker:
          columns = i.split(":")
          if len(columns) > 1:
              context.write("<tr><td>" + columns[0] + "</td><td>" + 
                             columns[1] + "</td></tr>")
          else:
              context.write("<tr><th>" + columns[0] + "</th></tr>")
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['i','columns'] if __M_key in __M_locals_builtin_stored]))
        # SOURCE LINE 18
        __M_writer(u'\n</table>\n\n    <div id="placeholder" style="width:600px;height:300px;"></div>\n\n<script type="text/javascript">\n$(function () {\n    var d1 = [];\n    for (var i = 0; i < 14; i += 0.5)\n        d1.push([i, Math.sin(i)]);\n\n    var d2 = [[0, 3], [4, 8], [8, 5], [9, 13]];\n\n    // a null signifies separate line segments\n    var d3 = [[0, 12], [7, 12], null, [7, 2.5], [12, 2.5]];\n    \n    $.plot($("#placeholder"), [ d1, d2, d3 ]);\n});\n</script>\n\n</body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


