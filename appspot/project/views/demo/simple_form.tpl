<div class="appswell-demo" id="appswell-demo-simpleform">

<div class="controller_menu">
<h3>menu</h3>
<ul>
{{ menu|safe }}
</ul>
</div>

<h2>simple form demo</h2>
<p>input a favorite website</p>
<form method="POST" action="/demo/simple_form">
    <table>
        {{ simple_form|safe }}
    </table>
    <input type="submit" name="simple_form_submit" value="submit" />
</form>

<br />

<h4>introspect</h4>
<pre>
{{ data|safe }}
</pre>

<br />

<h4>datastore (last 5 items)</h4>
<pre>
{{ datastore|safe }}
</pre>

</div>