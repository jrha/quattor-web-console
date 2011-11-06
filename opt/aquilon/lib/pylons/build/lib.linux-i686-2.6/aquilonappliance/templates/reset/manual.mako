<%inherit file="/base.mako"/>

<h2>Congratulations!</h2>

<p>This virtual appliance has been given a clean install.
For your next steps, you'll need to configure the DNS domains,
the networks and the geography (where your server rooms are located).

<h2>Remote Access</h2>
<p>If you want to use this appliance remotely, there are a few
options:
<ul>
<li>The <a href="/">appliance web interface</a> provides (very) limited functionality.
<li>You can ssh onto the box. The "cdb" user should have been configured when the virtual appliance was installed and you will have the password. Won't you?
<li>You can configure the appliance for network access via the "aq-client" package (not yet available). In order to configure the "aq-client", you will need to configure cross-realm trust (preferably one-way trust for your own safety). To do this you will need to create a principal krbtgt/${c.realm}@YOURREALM within your kerberos infrastructure.
</ul>

<p>If you wish to use the web interface, you'll probably want to do the following:
<ol>
<li><a href='/form/add_archetype?_return=/reset/manual'>Add a template archetype</a>
<li><a href='/form/add_personality?_return=/reset/manual'>Add a template personality</a>
<li><a href='/form/add_os?_return=/reset/manual'>Add an operating system</a>
<li><a href='/form/add_network?_return=/reset/manual'>Add a network</a>
<li><a href='/form/add_dns_domain?_return=/reset/manual'>Add a DNS domain</a>
<li><a href='/form/add_hub?_return=/reset/manual'>Add a hub</a>
<li><a href='/form/add_continent?_return=/reset/manual'>Add a continent</a>
<li><a href='/form/add_country?_return=/reset/manual'>Add a country</a>
<li><a href='/form/add_city?_return=/reset/manual'>Add a city</a>
<li><a href='/form/add_building?_return=/reset/manual'>Add a building</a>
<li><a href='/form/add_rack?_return=/reset/manual'>Add a rack</a>
<li><a href='/form/add_machine?_return=/reset/manual'>Add a machine</a>
<li><a href='/form/add_interface?_return=/reset/manual'>Add a network interface to that machine</a>
<li><a href='/form/add_host?_return=/reset/manual'>Add a host configuration to your machine</a>
</ol>



<a href='/'>View the Appliance</a>
