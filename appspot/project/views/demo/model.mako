<%inherit file="/default.mako"/>

<%def name="header()">
    ${head_content}
</%def>

<%!
    # python code here
    from datetime import datetime
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
%>

<div class="appswell-demo" id="appswell-demo-model">

    <div class="controller_menu">
        <h3>menu</h3>
        <ul>
            ${menu}
        </ul>
    </div>

    <h2>SimpleLog Records</h2>
    <p>Log can be updated at the <a href="/demo/recaptcha">ReCaptcha
       example</a>.</p>

    <h3 class="logs">Last ${num_records} Log Entries</h3>
    <table id="simplelog_records">
        <tr><th>created</th><th>type</th><th>keyword</th><th>message</th></tr>
        % if not RecentLogs:
            <tr><td colspan="4">no records found</td></tr>
        % else:
            % for Log in RecentLogs:
            <tr>
                <td>${Log.created.strftime("%Y-%m-%d %H:%M:%S")}</td>
                <td>${Log.type}</td>
                <td>${Log.keyword}</td>
                <td>${Log.message}</td>
            </tr>
            % endfor
        % endif
    </table>
    <br />
    <h6>current time: ${current_time}</h6>

</div>