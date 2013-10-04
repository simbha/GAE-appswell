<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>
        Appswell: Google App Engine Prototype
	</title>
    <!-- head title -->
    <!-- title for layout -->

    <meta name="verify-v1" content="5X6kOqxpPxWg9HASv6NtdtkOII7PRn76qvJp3xnd9aM=" />
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
	{{ head_content|safe }}
</head>

<body>  
<div id="layout-demo" class="page">
    
<div id="metabar">
    <a class="left" href="/">home</a>
    <a class="right" href="/demo">demo</a>
    <div class="clear"></div>
</div>

<div id="content">
    {{ flash|safe }}
    {{ controller_output|safe }}
</div>
        
        
<div id="footer">
    <div class="left"><a href="/">appswell.appspot.com</a></div>
    <div class="right"><a href="http://www.klenwell.com/">klenwell.com</a></div>
    <div class="center">
        some rights reserved
    </div>
</div>

</div>
	<!-- {{ debug_output }} -->
    
    <!-- Google Analytics -->
    <script type="text/javascript">
    var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
    document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
    </script>
    <script type="text/javascript">
    try {
    var pageTracker = _gat._getTracker("UA-1122772-10");
    pageTracker._trackPageview();
    } catch(err) {}</script>
</body>
</html>

