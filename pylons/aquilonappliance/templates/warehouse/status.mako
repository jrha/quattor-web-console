<%inherit file="/base.mako"/>

Welcome to the datawarehouse. Look at the <a href='http://${c.base}:5984/_utils/database.html?profiles'>profiles</a>!

<form method='POST' action='upload'>
<input type='submit' value='Sync Datawarehouse'>
</form>
