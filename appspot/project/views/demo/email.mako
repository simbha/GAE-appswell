<%inherit file="/default.mako"/>

<%def name="header()">
    ${head_content}
</%def>

<%!
    # python code here
%>

<div class="appswell-demo" id="appswell-demo-email">

    <div class="controller_menu">
        <h3>menu</h3>
        <ul>
            ${menu}
        </ul>
    </div>

    <h2>Email</h2>
    
    % if feedback:
        <h5>${feedback}</h5>
    % endif
    
    % if show_form:
        <div class="email_form">
        <form method="post" action="/demo/email">
            <p>To send an email to the Google Account with which you are logged
            in, hit the button below:</p>
        
            <input type="submit" name="send_email" value="send test email" />
        
            <p>Email will be sent to: <strong>${user_email}</strong></p>
        
            <h5>Text of email that will be sent:</h5>
            <pre>${email_message}</pre>
        </form>
        </div>
    % endif

</div>