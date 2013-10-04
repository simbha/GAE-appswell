<%inherit file="/default.mako"/>

<%def name="header()">
    ${head_content}
</%def>

<%!
    # python code here
    google_code_changlog = 'http://code.google.com/p/appswell/source/list'
%>

<div class="appswell-presents" id="appswell-presents-changelog">

    <h2>Changelog</h2>
    <br />
    <ul>
        <li>
            <a href="https://trello.com/board/appswell/512936a9127b7248110032a0">
                Trello Board</a>
        </li>
        <li>
            <a href="${google_code_changlog}">Google Code Project Changelog</a>
        </li>   
    </ul>
    
</div>
