<%inherit file="/default.mako"/>

<%def name="header()">
    ${head_content}
</%def>

<%!
    # python code here
%>

<div class="appswell-demo" id="appswell-demo-recaptcha">

    <div class="controller_menu">
        <h3>menu</h3>
        <ul>
            ${menu}
        </ul>
    </div>

    <h2>recaptcha example</h2>
    <p>complete the recaptcha below and the <a href="/demo/model">SimpleLog
    model</a> will be updated</p>

    <form method="POST" action="/demo/recaptcha">
        ${recaptcha_html}
        <input type="submit" name="simple_form_submit" value="submit" />
    </form>

</div>