<%inherit file="/base.mako"/>

<h2>Welcome!</h2>
<p>Welcome to the Aquilon Virtual Appliance. This appliance allows you 
to try out Aquilon with minimal pain. 

<p>In order to get started, there is a small number of defaults
that we will need to configure.   Once we've got the basic
information we can make the Aquilon appliance available and you
can start populating host information either manually or by
migrating from an existing Quattor installation. If you do not
already have a Quattor installation then leave the quattor
profile URL blank.
<p>
The organization code should be a short alphanumeric tag. If your
organization is "Sprockets, Incorporated" then it might be an
idea to use an organization code of "sprockets". This organization
code is used to bind together the hierarchy of datacenters and
locations in which you have hosts. You can add other organizations
later if you wish - what we want here is the default organization
to make things easier later.

<p>
<form method='POST' action='/reset' class='cmxform'>
<fieldset>
<legend>Basic Aquilon Configuration</legend>
<ol>
<li><label for='org'><b>Organization code</b></label><input value='${c.org}' size='48' id='org' name='org'/></li>
<li><label for='orgtext'><b>Organization full name</b></label><input value='${c.orgtext}' size='48' id='orgtext' name='orgtext'/></li>
<li><label for='profiles'><b>Existing Quattor URL</b></label><input value='${c.profiles}' size='48' id='profiles' name='profiles'/></li>
</ol>
<input type='submit' id='submit' value='Submit'>
</fieldset>
<form>
