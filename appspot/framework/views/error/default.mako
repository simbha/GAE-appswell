<%inherit file="/error.mako"/>

<%def name="header()">
    ${head_content}
</%def>

<%!
    # python code here
    from pprint import pformat
    from cgi import escape
    
    show_sys_path = False
%>

<div class="appswell-presents" id="appswell-presents-404">

    <h2>Page Unavailable</h2>
    <h5>Sorry, there has been an unexpected error.</h5>
    <!-- error: ${str(error_type)} -->

    % if is_dev_server:
    <div class="dev_server_detail">
        <h3>${escape(str(error_type))}</h3>
        <h4>traceback</h4>
        <pre>${trace}</pre>

        % if show_sys_path:
        <h4>sys.path</h4>
        <pre>${pformat(syspath)}</pre>
        % endif
    </div>
    % endif
</div>
