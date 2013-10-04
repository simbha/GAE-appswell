<%inherit file="/test.mako"/>

<%def name="header()">
    ${head_content}
</%def>

<%def name="subtitle()">
    ${module}
</%def>

<%
    from pprint import pformat
    from cgi import escape
    import logging

    suite_class = successful and 'pass' or 'fail'
    suite_summary = '%s of %s test%s passed' % (tests_passed, total_tests,
        total_tests != 1 and 's' or '')
    ##notes_index = sorted(test_notes, key=test_notes.get)
%>

<div class="appswell-test" id="appswell-test-template">

    <h2>test module: ${module}</h2>

    <h2 class="suite_result ${suite_class}">
        ${suite_class} &raquo; ${suite_summary}
    </h2>

    <div id="tests">
        <h3>Tests</h3>
        <table class="listing" id="test_results">
            <tr class="header"><th>result</th><th>test</th><th>time</th><th>notes</th></tr>
        % for test in test_results:
            <%
                result = test_results[test][0].lower()
                duration = '%.4f' % (test_results[test][2])
                description = test_results[test][5]
            %>
            <tr class="results ${result}">
                <td class="result">${result}</td>
                <td class="test">${test}</td>
                <td class="duration">${duration}</td>
                <td class="description">${description}</td>
            </tr>
            % if result != 'pass':
            <tr class="trace ${result}">
                <td class="result" colspan="4">
                    <pre>${test_results[test][1]}</pre>
                </td>
            </tr>
            % endif
        % endfor
        </table>
    </div>

    <div id="logs">
        <h3>Log</h3>
        <table class="listing" id="test_log">
            <tr class="header"><th>time</th><th>test</th><th>file</th><th>note</th></tr>
        % for note in test_notes:
            <%
                stamp = note[0]
                message = note[1]
                trace = note[2]
                caller = trace[-2][2]
                file = trace[-2][0].replace(project_root, '')
                file_page = '%s:%s' % (file, trace[-2][1])
                timestamp = '%02d:%02d:%02d.%d' % (stamp.hour, stamp.minute,
                    stamp.second, round(stamp.microsecond/1000.0))
            %>
            <tr class="results ${result}">
                <td class="timestamp">${timestamp}</td>
                <td class="caller">${caller}</td>
                <td class="file">${file_page}</td>
                <td class="note">${escape(message)}</td>
            </tr>
        % endfor
        </table>

        ## debug
        ##<pre style="font-size:7px;">${pformat([t[0] for t in test_notes])}</pre>
    </div>

    <h6 class="footer">script complete in ${'%.4f' % completed_in} s</h6>

    <br />
    <h5>return to <a href="/test">index</a></h5>

</div>
