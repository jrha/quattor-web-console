<%inherit file="/base.mako"/>
<div class='page-header'><h1>Kerberos Configuration</h1></div>
<form method="get" action='krb5configure'>
<table>
<tr><th>Realm</th><td><input name='realm' size=40 value='${c.realm}'></td></tr>
<tr><td></td><td><input type='submit' value='Change Realm'></td></tr>
</table>
</form>
