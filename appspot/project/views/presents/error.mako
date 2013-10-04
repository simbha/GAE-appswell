<%inherit file="/default.mako"/>

<%def name="header()">
    ${head_content}
</%def>

<%!
    # python code here
    from pprint import pformat
    from cgi import escape

    google_code_issue_site='http://code.google.com/p/appswell/issues/list'
%>

<div class="appswell-presents" id="appswell-presents-404">

    <h2>Page Unavailable</h2>
    <h5>If you believe this page has been reached in error, please open a
        ticket on the <a href="${google_code_issue_site}">Appswell Google Code
        project site</a>.</h5>
    <br />
    <h5>[Error: ${str(error_type)}]</h5>
    <!-- error: ${str(error_type)} -->

    % if is_dev_server:
    <div class="dev_server_detail">
        <h3>${escape(str(error_type))}</h3>
        <h4>traceback</h4>
        <pre>${trace}</pre>

        <h4>sys.path</h4>
        <pre>${pformat(syspath)}</pre>
    </div>
    % endif
</div>
