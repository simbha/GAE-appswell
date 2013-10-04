<%inherit file="/test.mako"/>

<%def name="header()">
    ${head_content}
</%def>

<%def name="subtitle()">
    Index
</%def>

<%

%>

<div class="appswell-test" id="appswell-test-index">

    <h2>Appswell Tests Index</h2>

    % for group in groups:

        <h3>${group}</h3>
        <ul>

        % for test in groups[group]:
            <%
                link = test
                label = test.split('/')[-1]
            %>
            <li><a href="${link}">${label}</a></li>
        % endfor

        </ul>

    % endfor

</div>
