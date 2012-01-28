<%inherit file="/base.mako"/>

<h2>${c.cmd}</h2>
<p>
${c.text}
<p>
<form method='POST' action='/form/${c.cmd}' class='cmxform'>
<%
for line in c.form:
    context.write(line + "\n")
%>
</form>
