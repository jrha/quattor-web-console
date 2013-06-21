<%inherit file="/base.mako"/>

<div class='page-header'><h1>Logging</h1></div>
<h2>Tail of ${c.title} log</h2>
<pre style='overflow-x: auto; word-wrap: normal; white-space: pre;'><%
for line in c.log:
    context.write(line)
%></pre>
