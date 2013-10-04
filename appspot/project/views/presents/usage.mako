<%inherit file="/default.mako"/>

<%def name="header()">
    ${head_content}
</%def>

<%!
    # python code here
%>

<div class="appswell-demo" id="appswell-demo-content">

    <h2>appswell-core usage</h2>

    <div class="section" id="overview">
        <h4>Overview</h4>
        The <b>appswell-core</b> project is a stripped-down drop-in version of
        the Appswell framework. It is designed for rapid application development
        on the Google App Engine platform for Python.
    </div>

    <div class="section" id="installation">
        <h4>Installation</h4>
        Well, if you've gotten this far, you've probably succeeded in downloading
        the Appswell package, installing it, and launching the App Engine dev
        server. But in the event that has not happened yet:

        <h5>1. Download the Google App Engine Code for Python</h5>
        Find the code here:
        <a href="http://code.google.com/appengine/downloads.html#Google_App_Engine_SDK_for_Python">
        http://code.google.com/appengine/downloads.html</a>

        <h5>2. Download or Check Appswell Code</h5>
        Find the code here: <a href="http://code.google.com/p/appswell/">
        http://code.google.com/p/appswell/</a>

        <h5>3. Copy code to your project directory</h5>
        Your directory will look something like this when down.
        <pre>/home/user/projects/my-project
|-- appspot
|   |-- config
|   |-- controllers
|   |-- models
|   |-- public
|   |-- tests
|   |-- views
|   |-- app.yaml
|   |-- dispatch.py
|   |-- etc...
|-- google_core (symbolic link)</pre>

        <tt>google_core</tt> should either link to the App Engine code you
        downloaded from Google or be the code itself.

        <h5>4. Start App Engine Dev Server</h5>
        Run the following command, making the appropriate adjustments for project
        path:
        <pre>$ /home/user/projects/my-project/google_core/dev_appserver.py --port=3000 --datastore_path=/tmp/my-project-datastore.txt --history_path=/tmp/my-project-history.txt /home/user/projects/my-project/appspot</pre>
        Your site would then be accessible at: http://localhost:3000/<br />
        <br />
        For ideas on scripting this command see the
        <a href="http://code.google.com/p/appswell/source/browse/run.sh-dist">
        Appswell run shell</a>. For more information on the dev server, see the
        <a href="http://code.google.com/appengine/docs/python/tools/devserver.html">
        Google documentation</a>.
    </div>

    <div class="section" id="configuration">
        <h4>Configuration</h4>
        Project configuration is handled within the <tt>config</tt> directory.
        Rename or copy <tt>core.py-dist</tt> to <tt>core.py</tt>.<br />
        <br />
        Most major
        settings can be included in the <tt>core.py</tt> and then imported into
        controller like so:

        <pre>import config</pre>

        Resource connections (e.g. to the datastore) are handled automatically
        by the App Engine framework.
    </div>

    <div class="section" id="configuration">
        <h4>Tests</h4>
        Tests are available here: <a href="/test">tests</a><br />
        <br />
        You can add additional tests by copying the <a href="/test/unit/template">
        unit template test</a> (or any other test) into one of the test
        directories and editing it.<br />
        <br />
        The tests use the Python unittest module. Currently they cannot be run
        from the command line and must be run from the browser.
    </div>

    <div class="section" id="additional">
        <h4>Additional Information</h4>
        For additional information or examples of more advanced usage of the
        Appswell framework, see the <a href="http://appswell.appspot.com/">
        Appswell</a> website.
    </div>

</div>
