<%inherit file="/base.mako"/>

<h2>Broker Status</h2>
<%
context.write("<dl class='dl-horizontal'>\n")
for i in c.broker:
    if i:
        columns = i.split(":", 1)
        if len(columns) > 1:
            key = columns[0]
            value = columns[1]

            if "is running" in value:
                value = "<span class='label label-success'>%s</span>" % (value)
            elif "is not running" in value:
                value = "<span class='label label-important'>%s</span>" % (value)

            context.write("<dt>%s</dt><dd>%s</dd>\n" % (key, value))
        else:
            context.write("<dt><i class='icon-info-sign'></i></dt><dd>" + columns[0] + "</dd>\n")
context.write("</dl>\n")
%>
<%
if hasattr(c, "brokererr"):
    if c.brokererr and len(c.brokererr) > 0:
        context.write("<pre class='text-error'>")
        context.write("<br>".join(c.brokererr))
        context.write("</pre>")
%>

<a href='/appliance/log/aqd'>Broker logs</a>

<h2>Space Usage</h2>
<div class='row'>
<div class='span4'>
<dl class='dl-horizontal'>
<%

space_items = c.space.items()

space_items = sorted(space_items, key=lambda item: item[0]) 

for (label, value) in space_items:
    context.write("<dt>%s</dt><dd>%d MB</dd>\n" % (label, value))
%>
</dl>
</div>
<div class='span8'>
<div id="spaceused" style="width:300px;height:300px;"></div>
</div>
</div>

<script type="text/javascript">
$(function () {
    var data = [
<%
colors = ['#049cdb','#46a546','#9d261d','#ffc40d','#f89406','#c3325f','#7a43b6']
i = 0
for (label, value) in space_items:
    color = colors[i % len(colors)]
    context.write("{ label: \"%s\", data: %d, color: '%s'}," % (label, value, color))
    i += 1
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
