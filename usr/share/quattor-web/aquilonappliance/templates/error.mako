<%inherit file="/base.mako"/>

<div class='page-header'><h1>Error</h1></div>

<%
context.write("<p>%s</p>\n" % (str(c.resp).splitlines()[0]))
%>
