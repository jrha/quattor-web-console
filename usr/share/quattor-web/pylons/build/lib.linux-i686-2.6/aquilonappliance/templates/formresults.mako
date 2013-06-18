<%inherit file="/base.mako"/>

<h2>${c.cmd}</h2>
<p>
<pre class='errors'>${c.stderr}</pre>
<pre>${c.stdout}</pre>
