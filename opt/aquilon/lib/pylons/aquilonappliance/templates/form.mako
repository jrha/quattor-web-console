<%inherit file="/base.mako"/>

<h2>
<%
if c.documentation:
    context.write("<a href='%s'>%s</a>" % (c.documentation, c.cmd))
else:
    context.write(c.cmd)
%>
</h2>
<p>
${c.text}
<p>
<form method='POST' action='/form/${c.cmd}' class='cmxform'>
<%
for line in c.form:
    context.write(line + "\n")
%>
</form>
