<%inherit file="/base.mako"/>
<h1>Kerberos Configuration</h1>
<form method="get" action='krb5configure'>
<table>
<tr><th>Realm</th><td><input name='realm' size=40 value='${c.realm}'></td></tr>
<tr><td></td><td><input type='submit' value='Change Realm'></td></tr>
</table>
</form>
