<!DOCTYPE html>
<html lang="en">
<head>
<title>Quattor Web Console</title>
<script language="javascript" type="text/javascript" src="/flot/jquery.js"></script>
<script language="javascript" type="text/javascript" src="/flot/jquery.flot.js"></script>
<script language="javascript" type="text/javascript" src="/flot/jquery.flot.pie.js"></script>
<link rel='stylesheet' type='text/css' href='/bootstrap/css/bootstrap.min.css'>
<link rel='stylesheet' type='text/css' href='/bootstrap/css/bootstrap-responsive.min.css'>
<style type="text/css">
  @import url(http://fonts.googleapis.com/css?family=Lato:400);
  body {
    padding-top: 64px;
    font-family: 'Lato', 'Helvetica', sans-serif;
}
</style>
</head>
<body>
<div class="navbar navbar-inverse navbar-fixed-top">
  <div class="navbar-inner">
    <div class="container">
      <a class="brand" href="/"><img src="/images/quattor_logo_navbar.png" width="94" height="23" alt="quattor logo"/></a>
      <div class="nav-collapse collapse">
        <ul class="nav">
          <li><a href="/commands">Commands</a></li>
        </ul>
      </div>
    </div>
  </div>
</div>
<div class="container">
${next.body()}
</div>
</body>
</html>
