<%inherit file="/base.mako"/>

<h2>Tail of ${c.title} log</h2>
<pre><%
for line in c.log:
    context.write(line)
%></pre>
