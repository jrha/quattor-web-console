<%inherit file="/base.mako"/>

<div class='page-header'><h1>Results</h1></div>
<%
is_stdout = ""
if not c.stdout:
    c.stdout = "None"
    is_stdout = "muted"

is_stderr = "text-error"
if not c.stderr:
    c.stderr = "None"
    is_stderr = "muted"
%>

<h2>${c.cmd.replace("_", " ")}</h2>
<div class="row">
<p class="span1">Error</p><span class="span11"><pre class='${is_stderr}'>${c.stderr}</pre></span>
</div>
<div class="row">
<p class="span1">Output</p><span class="span11"><pre class='${is_stdout}'>${c.stdout}</pre></span>
</div>
