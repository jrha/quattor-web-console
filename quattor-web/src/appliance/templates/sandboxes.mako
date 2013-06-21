<%inherit file="/base.mako"/>
<div class='page-header'><h1>Sandboxes</h1></div>
<div class='row'>
<%
if c.sandboxes:
    context.write("<table class='table'>\n")
    context.write("<thead>\n")
    context.write("<tr><th>Sandbox</th><th>Upstream Branch</th><th>Uncommitted Changes</th></tr>\n")
    context.write("</thead>\n")
    context.write("<tbody>\n")
    for (sandbox, details) in c.sandboxes.iteritems():
        context.write("<tr>")

        context.write("<td>%s</td>" % ("/".join(sandbox.split("/")[-2:])))

        context.write("<td>")
        context.write("%s " % (details['branch']))
        if 'position' in details:
            p = int(details['position'])
            if p > 0:
                context.write("<span class='badge badge-success' title='%d commits ahead of upstream branch'>+%d</span>\n" % (p, p))
            else:
                context.write("<span class='badge badge-error' title='%d commits behind upstream branch'>-%d</span>\n" % (p, p))
        else:
            context.write("<span class='badge' title='Up to date with upstream branch'>0</span>")
        context.write("</td>")

        context.write("<td>")
        if 'changes' in details:
            context.write("<dl class='dl-horizontal'>\n")
            for state, file in details['changes']:
                context.write("<dt>%s</dt><dd>%s</dd>\n" % (state, file))
            context.write("</dl>\n")
        else:
            context.write("&nbsp;")
        context.write("</td>")

        context.write("</tr>\n")
    context.write("</tbody>\n")
    context.write("</table>\n")
%>
</div>
