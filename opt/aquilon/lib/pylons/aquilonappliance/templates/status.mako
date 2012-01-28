<%inherit file="/base.mako"/>

<h2>Broker Status</h2>
<%
if len(c.broker) == 1:
    context.write("<p>" + c.broker[0])
else:
  context.write("<table>")
  for i in c.broker:
    columns = i.split(":", 1)
    if len(columns) > 1:
        context.write("<tr><th>" + columns[0] + "</th><td>" + 
                       columns[1] + "</td></tr>")
    else:
        context.write("<tr><th>" + columns[0] + "</th></tr>")
  context.write("</table>")
%>
<%
if len(c.brokererr) > 0:
    context.write("<pre class='errors'>")
    context.write("<br>".join(c.brokererr))
    context.write("</pre>")
%>

See also the <a href='/appliance/log/aqd'>broker logs</a>

<h2>Datawarehouse Status</h2>
<p>
<a href='http://${c.base}:5984/_utils/database.html?profiles'>View the datawarehouse</a>
<p>
See also the <a href='/appliance/log/warehouse'>datawarehouse logs</a>
<p>
<table>
<%
for i in c.warehouse:
  columns = i.split(":", 1)
  if len(columns) > 1:
      context.write("<tr><th>" + columns[0] + "</th><td>" + 
                     columns[1] + "</td></tr>")
  else:
      context.write("<tr><th>" + columns[0] + "</th></tr>")
%>
</table>
<form method='POST' action='/warehouse/update'>
<input type='submit' value='Sync Datawarehouse'>
</form>


<h2>Appliance Utilization</h2>
<p>Total managed space is ${c.totalspace}${c.units_as_text}

    <div id="spaceused" style="width:300px;height:300px;"></div>

<script type="text/javascript">
$(function () {
    var data = [
<%
for (label, value) in c.space.items():
    context.write("{ label: \"%s\", data: %d}," % (label, value))
%>
    ];
    $.plot($("#spaceused"), data, { 
               series: { 
                  pie: { 
                    show: true,
                  }
               },
               legend: {
                   show: false
               }
           });
});
</script>
