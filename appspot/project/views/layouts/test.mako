<%!
    """
        Appswell Default Mako Template

        NOTES
    """
    from config import core as c

%>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>appswell-core test: ${self.subtitle()}</title>

    <meta name="verify-v1" content="${c.GOOGLE_WEBTOOL_META}" />
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <link href="/css/default.css" rel="stylesheet" type="text/css" />
    <link href="/css/test.css" rel="stylesheet" type="text/css" />
    ${self.header()}
</head>

<body>
<div id="layout-demo" class="page">

<div id="metabar">
    <a class="left" href="/test">tests</a>
    <a class="right" href="/">home</a>
    <div class="clear"></div>
</div>

<div id="content">
    ${__flash__}
    ${self.body()}
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
    var pageTracker = _gat._getTracker("${c.GOOGLE_GA_CODE}");
    pageTracker._trackPageview();
    } catch(err) {}</script>
</body>
</html>
