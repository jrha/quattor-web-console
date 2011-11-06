<%inherit file="/base.mako"/>

<h2>Log for ${c.title}</h2>
<pre class='log'>
<%
for line in c.log:
    context.write(line)
%>
</pre>
