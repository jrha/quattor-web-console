<%inherit file="/base.mako"/>

<h2>
<%
cmd = c.cmd.replace("_", " ")
if c.documentation:
    context.write("<a href='%s'>%s</a>" % (c.documentation, cmd))
else:
    context.write(cmd)
%>
</h2>
<%
for line in c.text.split(".")[:-1]:
    context.write("<p>%s.</p>\n" % line.replace("\n","").strip())
%>
<form method='POST' action='/form/${c.cmd}' class='cmxform'>
<%
for line in c.form:
    context.write(line + "\n")
%>
</form>
