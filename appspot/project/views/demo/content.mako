<%inherit file="/default.mako"/>

<%def name="header()">
    ${head_content}
</%def>

<%!
    # python code here
%>

<div class="appswell-demo" id="appswell-demo-content">
    
    <div class="controller_menu">
        <h3>menu</h3>
        <ul>
            ${menu}
        </ul>
    </div>
    
    <h2>${headline}</h2>
    
    % if explanation:
    <p>
        ${explanation}
    </p>
    % endif
    
    <div class="content">
        ${content}
    </div>

</div>