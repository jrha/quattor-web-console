<%inherit file="/base.mako"/>
<div class='page-header'><h1>Commands</h1></div>
<h2>Objects</h2>
<dl class="dl-horizontal">
<%
for obj in sorted(c.objects.keys()):
    context.write("<dt>" + obj.replace("_", " ") + "</dt><dd>")
    if "add" in c.objects[obj]:
        context.write("<a class='btn btn-small btn-success' href='form/add_%s' title='Add'><i class='icon-plus icon-white'></i> Add</a> " % obj)
    else:
        context.write("<span class='btn btn-small btn-success disabled'><i class='icon-plus icon-white'></i> Add</span> ")

    if "del" in c.objects[obj]:
        context.write("<a class='btn btn-small btn-danger' href='form/del_%s' title='Delete'><i class='icon-remove icon-white'></i> Delete</a> " % obj)
    else:
        context.write("<span class='btn btn-small btn-danger disabled'><i class='icon-remove icon-white'></i> Delete</span> ")

    if "show" in c.objects[obj]:
        context.write("<a class='btn btn-small btn' href='form/show_%s' title='Show'><i class='icon-eye-open'></i> Show</a> " % obj)

    if "update" in c.objects[obj]:
        context.write("<a class='btn btn-small btn-warning' href='form/update_%s' title='Update'><i class='icon-edit icon-white'></i> Update</a> " % obj)

    if "search" in c.objects[obj]:
        context.write("<a class='btn btn-small' href='form/search_%s' title='Search'><i class='icon-search'></i> Search</a> " % obj)

    context.write("</dd>\n")
%>
</dl>

<h2>Broker</h2>
<%
for command in sorted(c.commands):
    label = command.replace("_", " ")
    context.write("<div class='well well-small container'>")
    context.write("<div class='row'>")
    context.write("<span class='span2'><a class='btn btn-small btn-inverse btn-block' href='form/%s'>%s</a></span><span class='span10'>%s</span>" % (command, label, c.commands[command]))
    context.write("</div>")
    context.write("</div>")
%>
 
