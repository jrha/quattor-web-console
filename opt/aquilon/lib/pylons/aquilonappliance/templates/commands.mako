<%inherit file="/base.mako"/>

<h2>Aquilon Objects</h2>
<table>
<%
for obj in sorted(c.objects.keys()):
    context.write("<tr><th>" + obj + "</th><td>")
    if "add" in c.objects[obj]:
        context.write("<a href='form/add_%s'>ADD</a> " % obj)
    if "del" in c.objects[obj]:
        context.write("<a href='form/del_%s'>DEL</a> " % obj)
    if "show" in c.objects[obj]:
        context.write("<a href='form/show_%s'>SHOW</a> " % obj)
    if "search" in c.objects[obj]:
        context.write("<a href='form/search_%s'>SEARCH</a> " % obj)
    if "update" in c.objects[obj]:
        context.write("<a href='form/update_%s'>UPDATE</a> " % obj)
    context.write("</td></tr>\n")
%>
</table>

<h2>Aquilon Commands</h2>
<table>
<%
for command in sorted(c.commands):
    context.write("<tr><td><a href='form/%s'>%s:</a> %s</td></tr>" % (command, command, c.commands[command]))
%>
</table>
 
