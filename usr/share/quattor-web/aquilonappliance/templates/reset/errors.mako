<%inherit file="/base.mako"/>

<h2>Hmm... Not so good...</h2>

There were errors in performing a reset on the appliance:
<%
context.write("<pre class='errors'>")
for err in c.errors:
    context.write(err)
context.write("</pre class='errors'>")
%>

It's possible that you can still continue. If you'd like to, then go
ahead and <a href='/reset/manual'>access the appliance</a>. 
Alternatively, <a href='/reset'>try the reset again</a>.

